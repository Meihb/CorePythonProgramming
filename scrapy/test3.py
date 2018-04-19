import urllib.request, urllib.parse
import json
import math
import ssl
import pymysql.cursors
import os
import time
import get_proxy_list
import threading


def mysql_configure():  # mysql配置
    conn = pymysql.connect(host='localhost', user='root', passwd='mhb12121992', port=3306, charset='utf8')
    conn.select_db('dwts')
    # conn = pymysql.connect(host='115.182.4.116', user='assess', passwd='Abcd1234', port=3306, charset='utf8')
    # conn.select_db('assess')
    return conn.cursor(), conn


def configureRoot():
    target_root = os.path.expanduser('~') + '\\bilibili_v2'
    if not os.path.exists(target_root):
        os.makedirs(target_root)
    return target_root


def refreshRequesat():
    pass


# 切换代理
def generateRequestProxy():
    global global_proxy_list
    global global_proxy_flag
    global global_proxy_addr
    choose_proxy()
    global_proxy_addr = global_proxy_list.pop()
    if global_proxy_flag:
        # 创建ProxyHandler
        proxy_support = urllib.request.ProxyHandler(global_proxy_addr)
        # 创建Opener
        opener = urllib.request.build_opener(proxy_support)
        # 安装OPener
        urllib.request.install_opener(opener)
        print('proxy started use' + str(global_proxy_addr))


# 模拟request请求
def requestConf(avid, pn):
    params = urllib.parse.urlencode({'oid': int(avid), 'pn': int(pn), 'type': 1, 'sort': 0, 'psize': 20})
    url = 'https://api.bilibili.com/x/v2/reply?%s' % params
    # print(url)
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=head)

    try:
        open = urllib.request.urlopen(request)
        jscontent = open.read()
        return jscontent.decode('utf-8', 'ignore')
    except urllib.request.URLError as e:
        print('oops,looks like we need to change proxy')
        generateRequestProxy()  # 切换代理
        requestConf(avid, pn)

# 保存信息 savetype 1:mysql 2:txt
def saveInfo(uid, uname, message, rtime, avid, pn, rpid, savetype=1):
    if savetype == 1:
        try:
            cur.execute('INSERT INTO bilibili_user_info VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                        [0, uid, uname, message, rtime, avid, pn, rpid])
            conn.commit()
        except  Exception as e:
            print('message is ' + message)
            exit()
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
    return {'uid': mid, 'uname': name, 'message': sign, 'rtime': rtime, 'rpid': rpid}


# 处理单个av号
def procAvid(avid):
    global  global_proxy_addr
    msg = ''
    if  not global_proxy_addr=={}:
        msg = '[!代理使用:%s]' % str(global_proxy_addr)


    print(' %s处理av%s 第一页' % (msg,avid))
    first_page_info = requestConf(avid, 1)
    jsDict = json.loads(first_page_info)
    if jsDict['code'] == 0:
        jsData = jsDict['data']
        jsPages = jsData['page']
        pageMax = math.ceil(jsPages['count'] / jsPages['size'])
        jsReplys = jsData['replies']

        for jsReply in jsReplys:  # 处理第一页数据
            saveInfo(**analyzeJson(jsReply), avid=avid, pn=1)
        for pn in range(2, pageMax + 1):  # 处理后续页面数据
            print('%s处理av%s 第%d页'%(msg,avid,pn))
            poc(avid, pn)


# 获取av号列表
def proc_avids():
    global global_proxy_addr
    global global_proxy_list

    generateRequestProxy()# 生成代理
    target_root = os.path.expanduser('~') + '/哔哩哔哩AV号.txt'
    with open(target_root, 'r') as f:
        for line in f.readlines():  # 逐行获取每一行av号
            try:
                procAvid(int(line))
            except:
                print('change urllib')
                generateRequestProxy()  # 生成代理
                procAvid(int(line))
                # exit()
            finally:
                print('Done')


# 处理数据并保存
def poc(avid, pn):
    jscontent = requestConf(avid, pn)
    jsDict = json.loads(jscontent)
    if jsDict['code'] == 0:
        jsData = jsDict['data']
        jsReplys = jsData['replies']

    for jsReply in jsReplys:
        saveInfo(**analyzeJson(jsReply), avid=avid, pn=pn)


# 获取代理ip列表
def choose_proxy():
    global global_proxy_list
    if len(global_proxy_list) <= 0:
        print('获取代理IP列表')
        for proxy in get_proxy_list.get_result_proxy():
            global_proxy_list.append(proxy)
        print('获取成功' + global_proxy_list.__str__())
        global_proxy_list.append({})
    return global_proxy_list


global_proxy_flag = True  # 全局切换代理标识
global_proxy_list = []  # 全局代理存储list
global_proxy_addr = {}  # 代理实体
global_open = None
global_request = None

ssl._create_default_https_context = ssl._create_unverified_context  # 关闭ssl证书验证
cur, conn = mysql_configure()  # 初始化数据库


proc_avids()  # 开始处理
# procAvid(10150031);
print('Success')
