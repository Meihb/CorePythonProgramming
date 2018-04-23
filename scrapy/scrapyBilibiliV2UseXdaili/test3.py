import urllib.request, urllib.parse
import requests
import json
import math
import ssl
import pymysql.cursors
import os
import time
import get_proxy_list
import sys
import time
import hashlib
import requests
import random
import threading


def mysql_configure():  # mysql配置
    conn = pymysql.connect(host='122.112.248.56', user='dwts', passwd='12121992', port=3306, charset='utf8mb4')
    conn.select_db('dwts')
    # conn = pymysql.connect(host='115.182.4.116', user='assess', passwd='Abcd1234', port=3306, charset='utf8')
    # conn.select_db('assess')
    return conn.cursor(), conn


def configureRoot():
    target_root = os.path.expanduser('~') + '\\bilibili_v2'
    if not os.path.exists(target_root):
        os.makedirs(target_root)
    return target_root


# 使用x代理
def generateRequestProxyV2():
    _version = sys.version_info

    is_python3 = (_version[0] == 3)

    orderno = "ZF20184206305g2nCdV"
    secret = "7a3eb1b3b91b4b44ae774e6f96152da1"
    ip = "forward.xdaili.cn"
    port = "80"
    ip_port = ip + ":" + port
    timestamp = str(int(time.time()))  # 计算时间戳
    string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

    if is_python3:
        string = string.encode()
    md5_string = hashlib.md5(string).hexdigest()  # 计算sign
    sign = md5_string.upper()  # 转换成大写
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    headers = {"Proxy-Authorization": auth}

    return headers, proxy
    # r = requests.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False)


# 切换代理
def generateRequestProxy():
    global global_proxy_list
    global global_proxy_flag
    global global_proxy_addr

    if global_proxy_flag:
        choose_proxy()
        global_proxy_addr = global_proxy_list.pop()
        # 创建ProxyHandler
        proxy_support = urllib.request.ProxyHandler(global_proxy_addr)
        # 创建Opener
        opener = urllib.request.build_opener(proxy_support)
        # 安装OPener
        urllib.request.install_opener(opener)
        print('proxy started use' + str(global_proxy_addr))


# 模拟request请求
def requestConf(avid, pn):
    global global_proxy_flag
    # time.sleep(random.randint(1, 3))

    time.sleep(random.randint(300, 600)/1000)
    if global_proxy_flag:
        headers, proxy = generateRequestProxyV2()
    else:
        headers = {}
        proxy = {}
    params = urllib.parse.urlencode({'oid': int(avid), 'pn': int(pn), 'type': 1, 'sort': 0, 'psize': 20})
    url = 'https://api.bilibili.com/x/v2/reply?%s' % params
    print(url)

    try:
        jscontent = requests.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
        # print(jscontent.content.decode('utf-8','ignore'))
        return jscontent.content.decode('utf-8', 'ignore')
    except Exception:
        raise


# 保存信息 savetype 1:mysql 2:txt
def saveInfo(uid, uname, message, rtime, avid, pn, rpid, up_id, user_sex, user_level, user_vip, savetype=1):
    if savetype == 1:
        try:
            cur.execute(
                'INSERT INTO bilibili_comment '
                '(id,av,up_id,comment,user_id,user_name,user_level,user_vip,user_sex,part_date,reply_id,page_num) '
                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                [0, avid, up_id, message, uid, uname, user_level, user_vip, user_sex,
                 time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(rtime)), rpid, pn])
        except  Exception as e:
            print('message is ' + message)
            raise
    elif savetype == 2:
        target_root = configureRoot()
        target_file = '%s\\%s.txt' % (target_root, avid)
        with open(target_file, 'a', encoding='utf-8') as f:  # uid  replyid pn
            f.write(
                str(uid) + '\t' + str(rpid) + '\t' + str(pn) + '\t' + str(uname) + '\t' + time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.localtime(
                        rtime)) + '\t' + str(
                    message).replace('\n', ' ') + '\n')

    else:
        print('invalid type to save')


# 处理json数据
def analyzeJson(jsData):
    mid = jsData['member']['mid']
    name = jsData['member']['uname']
    sign = jsData['content']['message']
    rtime = jsData['ctime']
    rpid = jsData['rpid']
    u_level = jsData['member']['level_info']['current_level']
    u_vip = jsData['member']['vip']['vipType']
    gender = jsData['member']['sex']

    return {'uid': mid, 'uname': name, 'message': sign, 'rtime': rtime, 'rpid': rpid, 'user_sex': gender,
            'user_level': u_level, 'user_vip': u_vip}


def jsonDecodeHtml(page_info):
    jsDict = json.loads(page_info)
    return jsDict


# 处理单个av号
def procAvid(avid):
    global global_proxy_addr
    msg = ''
    if not global_proxy_addr == {}:
        msg = '[!代理使用:%s]' % str(global_proxy_addr)

    print(' %s处理av%s 第一页' % (msg, avid))
    first_page_info = requestConf(avid, 1)
    jsDict = jsonDecodeHtml(first_page_info)
    if jsDict['code'] == 0:
        jsData = jsDict['data']
        jsPages = jsData['page']
        pageMax = math.ceil(jsPages['count'] / jsPages['size'])
        jsReplys = jsData['replies']
        uper_id = jsData['upper']['mid']  # up主人id

        for jsReply in jsReplys:  # 处理第一页数据
            saveInfo(**analyzeJson(jsReply), avid=avid, pn=1, up_id=uper_id)
        for pn in range(2, pageMax + 1):  # 处理后续页面数据
            print('%s处理av%s 第%d页' % (msg, avid, pn))
            poc(avid, pn)


def getNextAvid():  # 获取第一个未处理的avid
    cur.execute("SELECT avid  FROM bilibili_av_list WHERE  pro_flag = 0 ORDER BY  id Asc Limit 1")
    result = cur.fetchall()

    if result:
        return result[0][0]
    else:
        return None


def switchFlag(avid):#改变标识
    cur.execute("UPDATE  bilibili_av_list  set pro_flag = 1,proc_date_time = NOW() WHERE  avid  = %s ", [avid])
    conn.commit()


# 获取av号列表
def proc_avids():
    global global_proxy_addr
    global global_proxy_list
    global global_proxy_flag

    av_id = getNextAvid()
    print(av_id)
    while av_id:  # 存在待处理avid
        try:
            procAvid(int(av_id))
            print('commit av%s 数据到mysql' % av_id)
            switchFlag(av_id)
            print('保存成功')
            proc_avids()
        except Exception as e:
            print('Exception occurs ' + e.__str__())
            print('change urllib')
            print('rollback  av%s 数据到mysql' % av_id)
            conn.rollback()
            if global_proxy_flag:
                generateRequestProxyV2()  # 生成代理
                print('用新代理处理av%s' % av_id)
                procAvid(int(av_id))
            else:
                print('运行到av%s被限制,无法继续' % av_id)
                exit()


# generateRequestProxyV2()  # 生成代理
# target_root = os.path.expanduser('~') + '/哔哩哔哩AV号.txt'
# with open(target_root, 'r') as f:
#     for line in f.readlines():  # 逐行获取每一行av号
#         try:
#             procAvid(int(line))
#             print('commit av%s 数据到mysql' % line)
#             conn.commit()
#             print('保存成功')
#         except Exception as e:
#             print('Exception occurs ' + e.__str__())
#             print('change urllib')
#             print('rollback  av%s 数据到mysql' % line)
#             conn.rollback()
#             if global_proxy_flag:
#                 generateRequestProxyV2()  # 生成代理
#                 print('用新代理处理av%s' % line)
#                 procAvid(int(line))
#             else:
#                 print('运行到av%s被限制,无法继续' % line)
#                 exit()


# 处理数据并保存
def poc(avid, pn):
    jscontent = requestConf(avid, pn)
    jsDict = jsonDecodeHtml(jscontent)
    if jsDict['code'] == 0:
        jsData = jsDict['data']
        jsReplys = jsData['replies']
        uper_id = jsData['upper']['mid']  # up主人id
        for jsReply in jsReplys:
            saveInfo(**analyzeJson(jsReply), avid=avid, pn=pn, up_id=uper_id)


# 获取代理ip列表
def choose_proxy():
    global global_proxy_list
    if len(global_proxy_list) <= 0:
        print('获取代理IP列表')
        for proxy in get_proxy_list.get_result_proxy():
            global_proxy_list.append(proxy)
        global_proxy_list.append({})

    print('获取成功' + global_proxy_list.__str__())
    return global_proxy_list


global_proxy_switch = time.time()  # 切换时间记录，>0当前正在使用代理,<0当前未使用代理
global_proxy_flag = False  # 全局切换代理标识
global_proxy_list = []  # 全局代理存储list
global_proxy_addr = {}  # 代理实体
global_open = None
global_request = None

ssl._create_default_https_context = ssl._create_unverified_context  # 关闭ssl证书验证
requests.packages.urllib3.disable_warnings()
cur, conn = mysql_configure()  # 初始化数据库

proc_avids()  # 开始处理
# procAvid(10150031)
print('Success')
