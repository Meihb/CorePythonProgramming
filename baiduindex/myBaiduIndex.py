#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from PIL import Image
import requests
import time, datetime
import re
import urllib
import pytesseract
import traceback
import os
import pymysql, multiprocessing
import redisConn

save_path = r'D:\download\baiduINdex' + time.strftime('%Y-%m-%d %H%M')

chromeDriver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'  # chromedriver路径
tesseract_exe = r'D:\software\dev\Tesseract-OCR\tesseract.exe'  # tesseract.exe路径
bd_account = '13851020274'  # 百度账号
# bd_account='19921625136'
bd_pwd = 'mhb12121992'  # 百度密码

bd_url = 'http://index.baidu.com/?tpl=trend'


class Throttle():
    '''
    add a delay between downloads to the same domain
    '''

    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urllib.parse.urlparse(url).netloc
        # print(domain.netloc)
        print(self.domains)
        if self.domains.get(domain):
            last_access_interval = self.delay - (time.time() - self.domains.get(domain))
            print(last_access_interval)
            if last_access_interval > 0:
                print('sleep for %ss' % (last_access_interval))
                time.sleep(int(last_access_interval))
        else:
            pass
        self.domains[domain] = time.time()


class WordNotPrepared(Exception):
    def __init__(self, err='word not prepared'):
        Exception.__init__(self, err)
        self.word = word


def mysqlConn():
    host = '118.25.41.135'
    port = 3306
    user = 'dwts'
    pwd = 'dwts'
    # 创建连接
    conn = pymysql.connect(host=host, user=user, passwd=pwd, port=port, charset='utf8mb4', db='dwts')

    # 建立游标,修改默认元组数据为字典类型
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn, cur


conn, cur = mysqlConn()


# type 1 input;2 import 初始化关键词
def get_keywords(type=1, *args):
    keywords = []
    if type == 1:
        keyword = input('请输入关键词:').encode('utf-8')
        keywords.append(keyword)
    elif type == 2:
        pass
        # todo
    else:
        raise Exception('Invalid type to initiate keywords')
    return keywords


# 获取cookies
def prep_cookies():
    browser = webdriver.Chrome(chromeDriver)
    browser.get('http://index.baidu.com/?tpl=trend')  # 接下来需等待chrome启动和页面加载,如果不等待，下面的语句会出现找不到元素的错误
    # time.sleep(5)#强制等待,最简单的等待方法,强制等待,浪费资源,且不知何时才能正确执行,则命中率低
    # browser.implicitly_wait(10)#隐性等待,设置最长等待时间,若页面所有资源在时间内完成加载,则停止等待,较高的时间利用率,但是是否需要页面全部加载的问题浮现
    # time.sleep(60)
    try:  # 显性等待,通过until/until_not 实现自定义的目标
        WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.ID, 'TANGRAM__PSP_4__userName')))
        # WebDriverWait(browser, 10, 0.5).until(lambda driver: driver.find_element_by_class_name('lb'))
        browser.find_element_by_id('TANGRAM__PSP_4__userName').clear()
        browser.find_element_by_id('TANGRAM__PSP_4__userName').send_keys(bd_account)
        browser.find_element_by_id('TANGRAM__PSP_4__password').clear()
        browser.find_element_by_id('TANGRAM__PSP_4__password').send_keys(bd_pwd)

        browser.find_element_by_id('TANGRAM__PSP_4__submit').submit()  # 确认登录

        if browser.find_element_by_id('TANGRAM__PSP_4__verifyCodeImg'):
            # 存在验证码，手动填写
            time.sleep(9)

        time.sleep(3)  # 添加延迟以保证cookie获取完全
        cookies = browser.get_cookies()
        new_cookies = ''
        for cookie in cookies:
            new_cookies += cookie['name'] + '=' + cookie['value'] + ';'
        new_cookies = new_cookies[:-1]  # 去掉末尾;

        print(cookies)
        # exit()
        return new_cookies, browser
    except  NoSuchElementException as e:
        print('111' + e.msg)
        exit()
    except StaleElementReferenceException as e:
        print('222' + e.msg)
        exit()
    except TimeoutException as e:
        print('333' + e.msg)
        exit()


# chrome 启动!
def webdriver_generate():  # 自动化测试工具。它支持各种浏览器，包括 Chrome，Safari，Firefox 等主流界面式浏览器，如果你在这些浏览器里面安装一个 Selenium 的插件，那么便可以方便地实现Web界面的测试。换句话说叫 Selenium 支持这些浏览器驱动
    browser = webdriver.Chrome(chromeDriver)
    browser.get('http://index.baidu.com/?tpl=trend&word=s')  # 接下来需等待chrome启动和页面加载,如果不等待，下面的语句会出现找不到元素的错误
    # time.sleep(5)#强制等待,最简单的等待方法,强制等待,浪费资源,且不知何时才能正确执行,则命中率低
    # browser.implicitly_wait(10)#隐性等待,设置最长等待时间,若页面所有资源在时间内完成加载,则停止等待,较高的时间利用率,但是是否需要页面全部加载的问题浮现
    try:  # 显性等待,通过until/until_not 实现自定义的目标
        WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.ID, 'TANGRAM_12__userName')))
        # WebDriverWait(browser, 10, 0.5).until(lambda driver: driver.find_element_by_class_name('lb'))
        browser.find_element_by_id('TANGRAM_12__userName').clear()
        browser.find_element_by_id('TANGRAM_12__userName').send_keys('13851020274')
        browser.find_element_by_id('TANGRAM_12__password').clear()
        browser.find_element_by_id('TANGRAM_12__password').send_keys('mhb12121992')

        browser.find_element_by_id('TANGRAM_12__submit').submit()  # 确认登录
        cookies = browser.get_cookies()
        print(cookies)
        new_cookies = ''
        for cookie in cookies:
            print(cookie)
            new_cookies += cookie['name'] + '=' + cookie['value'] + ';'
        new_cookies = new_cookies[:-1]  # 去掉末尾;
        print(type(cookies))
        # exit()
        time.sleep(2)
        res = browser.execute_script('return PPval.ppt;')
        print('res is ', res)
        res2 = browser.execute_script('return PPval.res2;')
        print('res2', res2)
        header = {
            # 'Host': 'index.baidu.com',
            # 'Connection': 'keep-alive',
            # 'Accept': '*/*',
            # 'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
            # 'Referer': 'http://index.baidu.com/?tpl=trend&word=%CE%A4%B5%C2',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Cookie': new_cookies

        }
        return header, cookies
    except  NoSuchElementException as e:
        print('111' + e.msg)
        exit()
    except StaleElementReferenceException as e:
        print('222' + e.msg)
        exit()
    except TimeoutException as e:
        print('333' + e.msg)
        exit()
    finally:
        browser.close()


'''获取关键字最大起止日期'''


def get_request_period(word, headers, browser, myThrottle):
    myThrottle.wait('http://index.baidu.com')
    browser.get('http://index.baidu.com/?tpl=trend&%s' % (urllib.parse.urlencode({'word': word.encode('gb2312')})))

    browser.implicitly_wait(3)
    PPval = browser.execute_script('return PPval')
    print(PPval, type(PPval))

    res1 = PPval['ppt']
    res2 = PPval['res2']

    url = 'http://index.baidu.com/Interface/Search/getSubIndex/'

    myThrottle.wait('http://index.baidu.com')
    req = requests.get(url, params={'res': res1, 'res2': res2, 'word': word.encode('utf8'), 'startdate': '2000-01-01',
                                    'enddate': '2020-01-01', 'forecast': 0}, headers=headers)
    print(req.json())
    pc_period = req.json()['data']['pc'][0]['period']
    pc_period = pc_period.split('|')
    return [time.strftime('%Y-%m-%d', time.strptime(x, '%Y%m%d')) for x in pc_period], res1, res2
    # pc_period[0] = time.strftime(time.strptime(pc_period[0],'%Y%m%d'))
    # return pc_period


'''
获取关键字数据,保存原始图片，百度指数从20110101开始,在'全部'模式下,每周统计一次,前期可有数据缺失,需根据数据长度计算初始值
'''


def get_request(word, startdate, enddate, headers, word_path, browser, myThrottle, redis_name):
    '''

    :param word:
    :param startdate:
    :param enddate:
    :param headers:
    :param word_path:
    :param browser:
    :return:
    '''
    myRedis = redisConn.myRedisQueue('118.25.41.135', 6379, 'mhbredis', db=5)
    save_path = word_path
    myThrottle.wait('http://index.baidu.com')
    browser.get('http://index.baidu.com/?tpl=trend&%s' % (urllib.parse.urlencode({'word': word.encode('gb2312')})))
    browser.implicitly_wait(3)

    PPval = browser.execute_script('return PPval')
    print(PPval, type(PPval))

    res1 = PPval['ppt']
    res2 = PPval['res2']

    # res1 = browser.execute_script('return PPval.ppt')
    # res2 = browser.execute_script('return PPval.res2')

    url = 'http://index.baidu.com/Interface/Search/getSubIndex/'

    myThrottle.wait('http://index.baidu.com')
    req = requests.get(url, params={'res': res1, 'res2': res2, 'word': word.encode('utf8'), 'startdate': startdate,
                                    'enddate': enddate, 'forecast': 0}, headers=headers)

    if date_comparision(startdate, '2011-01-01') == '2011-01-01':
        print('pc res3 selected')
        res3_list = req.json()['data']['pc'][0]['userIndexes_enc']
        res3_list = res3_list.split(',')
    else:
        print('all res3 selected')
        res3_list = req.json()['data']['all'][0]['userIndexes_enc']
        res3_list = res3_list.split(',')

    print(res3_list)
    print(len(res3_list))
    # exit()

    m = 0
    range_dict = []
    temp_date = startdate
    for res3 in res3_list:
        timestamp = int(time.time())
        try:
            myThrottle.wait('http://index.baidu.com')
            req = requests.get('http://index.baidu.com/Interface/IndexShow/show/',
                               params={'res': res1, 'res2': res2, 'classType': 1, 'res3[]': res3,
                                       'className': 'view-value%s' % (timestamp)}, headers=headers).json()
            print(req)
            response = req['data']['code'][0]
            width = re.findall('width:(.*?)px', response)
            margin_left = re.findall('margin-left:-(.*?)px', response)
            # width = [int(x) for x in width]
            # margin_left = [int(x) for x in margin_left]
            range_dict.append({'width': width, 'margin_left': margin_left})
            img_url = 'http://index.baidu.com' + re.findall('url\("(.*?)"\)', response)[0]
            img_content = requests.get(img_url, headers=headers)
            time.sleep(1.5)
            if img_content.status_code == requests.codes.ok:
                with open('%s\\%s.png' % (save_path, temp_date), 'wb') as file:
                    file.write(img_content.content)

                # row_date = get_row_date()
                # cur.execute(
                #     'INSERT INTO `baidu_index` (dir,word,width,margin_left,img_url,location,time,refer_date_begin,refer_date_end) '
                #     'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                #     [
                #         save_path, word, ','.join(width), ','.join(margin_left), img_url,
                #         r'%s\%s.png' % (save_path, temp_date),
                #         time.strftime('%Y-%m-%d %H:%M:%S'), temp_date, temp_date
                #     ]
                # )
                # conn.commit()
                # dir|refer_date|width|margin_left|now|word
                myRedis.push(redis_name, '%s|%s|%s|%s|%s|%s' % (
                    save_path, temp_date, ','.join(width), ','.join(margin_left), time.strftime('%Y-%m-%d %H:%M:%S'),word))

        except:
            traceback.print_exc()
        else:
            m += 1
            temp_date = time_intverl(temp_date, 24 * 3600)
        # myRedis.quit()
    # conn.commit()


'''
拼接图片
'''


def joint(word):
    cur.execute('SELECT * FROM  `baidu_index` WHERE word=(%s)', [word])
    infos = cur.fetchall()
    for info in infos:
        width = [int(x) for x in info['width'].split(',')]
        margin_left = [int(x) for x in info['margin_left'].split(',')]
        save_dir = info['dir']
        file_path = r'%s\Puzzle%s.png' % (save_dir, int(info['id']))
        try:
            code = Image.open(info['location'])
            hight = code.size[1]
            print(width, margin_left, hight, sum(width))
            target = Image.new('RGB', (sum(width), hight))  # 创建一个原始图,以作底图类似于php的imgcreatefromtruecolor
            for i in range(len(width)):
                print((margin_left[i], 0, margin_left[i] + width[i], hight))
                img = code.crop(
                    (margin_left[i], 0, margin_left[i] + width[i], hight))  # crop((x0,y0,width,height)),裁剪目标图片
                # img.show()
                target.paste(img, (sum(width[0:i]), 0, sum(width[0:i + 1]), hight))
                # target.show()
            target.save(file_path)
            cur.execute("UPDATE `baidu_index` SET resolved_location =%s,recognitions = %s WHERE id=%s",
                        [file_path, img_recognition(save_dir, int(info['id'])), int(info['id'])])
            print('解析成功')
        except:
            traceback.print_exc()
    conn.commit()


def dameonize_joint():
    while True:
        row_info = cur.execute(
            'SELECT id,location FROM baidu_index WHERE process_status = 0 ORDER BY id ASC  LIMIT 1  ')

        try:
            cur.execute('UPDATE `baidu_index` SET process_status = -1 WHERE 1')  # 修改状态
            conn.commit()
        except:
            cur.execute('UPDATE `baidu_index` SET process_status')
            traceback.print_exc()


'''图片识别'''


def img_recognition(save_dir, index):
    pytesseract.pytesseract.tesseract_cmd = tesseract_exe
    jpgzoom = Image.open(r'%s\Puzzle%s.png' % (save_dir, index))
    # print(type(jpgzoom))
    (x, y) = jpgzoom.size
    x_s = 4 * x
    y_s = 4 * y
    out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
    # print(type(out))
    out.save('%s/zoom%s.jpg' % (save_dir, index), quality=95)
    num = pytesseract.image_to_string(out, config="-psm 7")
    if num:
        num = num.replace("'", '').replace('.', '').replace(',', '').replace('?', '7').replace("S", '5').replace(" ",
                                                                                                                 "").replace(
            "E", "8").replace("B", "8").replace("I", "1").replace("$", "8").replace('C', '0')
    else:
        num = ''
    print(num)
    return num


'''获取指定日期之后第一个指定周天(1-7分指周一至周日)'''


def get_weekday(weekday, offsetdate='2011-01-01'):
    timestamp = time.mktime(time.strptime(offsetdate, '%Y-%m-%d'))
    offsetdate = datetime.date.fromtimestamp(timestamp)
    return time.strftime("%Y-%m-%d", time.localtime((weekday - offsetdate.isoweekday()) % 7 * 3600 * 24 + timestamp))


'''时间戳增减计算'''


def time_intverl(start, interval):
    return time.strftime('%Y-%m-%d', time.localtime(time.mktime(time.strptime(start, '%Y-%m-%d')) + int(interval)))


'''百度时间分段生成器'''


def baidu_index_date_generator(begin, end):
    endtimestamp = time.mktime(time.strptime(end, '%Y-%m-%d'))
    while True:
        temp_end = get_weekday(6, begin)
        if (time.mktime(time.strptime(temp_end, '%Y-%m-%d'))) > endtimestamp:  # 计算日期段结尾已超过deadline,结算按照deadline计算,并退出循环
            yield {'start': begin, 'end': end}
            break
        else:
            yield {'start': begin, 'end': temp_end}
            begin = time_intverl(temp_end, 24 * 3600)


def get_row_date():
    global baidu_generator
    try:
        row_date = next(baidu_generator)
    except StopIteration:
        baidu_generator = baidu_index_date_generator('2011-01-01', time_intverl(time.strftime('%Y-%m-%d'), -24 * 3600))
        row_date = next(baidu_generator)
    return row_date


def baidu_index_date_generator_v2(begin, end):
    begin_timestamp = time.mktime(time.strptime(begin, '%Y-%m-%d'))
    end_timestamp = time.mktime(time.strptime(end, '%Y-%m-%d'))

    duration = int((end_timestamp - begin_timestamp) / (3600 * 24))  # 天数
    print(duration)


# 日期比较大小
def date_comparision(date1, date2, mode=1):
    date1_timestamp = int(time.mktime(time.strptime(date1, '%Y-%m-%d')))
    date2_timestamp = int(time.mktime(time.strptime(date2, '%Y-%m-%d')))
    if (max(date1_timestamp, date2_timestamp) == date1_timestamp):
        max_date = date1
        min_date = date2
    else:
        max_date = date2
        min_date = date1
    if mode == 1:  # 比较较大值
        return max_date
    else:
        return min_date


# 每日跨度
def enddate_generator(period_begin, period_end, step=24 * 3600 * 360):
    temp_startdate = period_begin
    while True:
        temp_enddate = time_intverl(temp_startdate, step)
        # print(temp_enddate,start_date)
        if date_comparision(period_end, temp_enddate) == period_end:  # 未到时间の尽头
            yield temp_startdate, temp_enddate
            temp_startdate = time_intverl(temp_enddate, 24 * 3600)
        else:  # now we are ONE!
            yield temp_startdate, period_end
            break


def split_date(start, end):
    '''
    限制start>=pc_start,end<=yesterday,且end>=start
    共四种情况
      start                                                        end                                                                              result
    pc_start<=start<all-start                pc_start<end<all_start                             start-end   +[]
                                                                    all_start<end                                                     start-pc_end + all_start-end
    start>=all_start                            all_start<end                                                           []                     +  start-end
    :param start >2006-06-01:
    :param end:
    :return:
    '''
    # pc_start = '2006-06-01'
    pc_end = '2010-12-31'
    all_start = '2011-01-01'

    pc_result = []
    all_result = []
    if date_comparision(all_start, start) == all_start:  # 起始时间低于all_start
        pc_result.append(start)
        if date_comparision(end, all_start) == all_start:  # 结束时间同样低于all_start
            pc_result.append(end)
        else:  # 结束时间高于all_start
            pc_result.append(pc_end)
            all_result.append(all_start)
            all_result.append(end)
    else:  # 起始时间高于all_start
        all_result.append(start)
        all_result.append(end)
    return pc_result, all_result


def process_request(myThrottle, redis_name):
    '''
    处理网络请求
    :return:
    '''
    cookies_string, browser = prep_cookies()
    headers = {
        'Host': 'index.baidu.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
        'Referer': 'http://index.baidu.com/?tpl=trend&word=%CE%A4%B5%C2',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': cookies_string
    }
    while True:
        cur.execute("SELECT id,word,start,end  FROM baidu_index_words WHERE flag = 0 ORDER BY id ASC  LIMIT 1")
        word_info = cur.fetchall()
        print(word_info)
        if word_info:
            word = word_info[0]['word']
            id = word_info[0]['id']
            print('settle %s' % word)
            word_path = '%s_%s' % (save_path, word)
            if not os.path.exists(word_path):
                os.mkdir(word_path)
            # 据观察,2006-06-01开启,pc趋势具备数据,自2011-01-01之后,移动趋势具备数据,则
            startdate = str(word_info[0]['start'])  # mysql date返回的是个date对象
            enddate = str(word_info[0]['end'])
            try:
                check_authority = get_request_period(word, headers, browser, myThrottle)
                startdate = date_comparision(startdate, '2006-06-01')  # 限定日期至少大于2006-06-01
                enddate = date_comparision(enddate, time_intverl(time.strftime('%Y-%m-%d'), -24 * 3600),
                                           -1)  # 限定日期不大于昨日
                pc_period, all_period = split_date(startdate, enddate)
                print(pc_period, all_period)

                if pc_period:  # PC任务存在
                    print('start pc 任务 from %s to %s' % (pc_period[0], pc_period[1]))
                    pc_generator = enddate_generator(pc_period[0], pc_period[1])
                    while True:
                        try:
                            period_info = next(pc_generator)
                            period_start = period_info[0]
                            period_end = period_info[1]
                            print(period_info)
                            # 处理文件
                            get_request(word, period_start, period_end, headers, word_path, browser, myThrottle,
                                        redis_name)
                        except StopIteration:
                            print('date all done')
                            break
                        except Exception as e:
                            if not isinstance(e, (StopIteration,)):
                                traceback.print_exc()
                                print('we should break')
                                print(e)
                                break
                if all_period:  # 整体任务存在
                    print('start 整体任务  from %s to %s' % (all_period[0], all_period[1]))
                    all_generator = enddate_generator(all_period[0], all_period[1])
                    while True:
                        try:
                            period_info = next(all_generator)
                            period_start = period_info[0]
                            period_end = period_info[1]
                            print(period_info)
                            # 处理文件
                            get_request(word, period_start, period_end, headers, word_path, browser, myThrottle,
                                        redis_name)
                        except StopIteration:
                            print('date all done')
                            break
                        except Exception as e:
                            if not isinstance(e, (StopIteration,)):
                                traceback.print_exc()
                                print('we should break')
                                print(e)
                                break

            except KeyError as e:  # PPval未被定义res1,res2表现为该关键字未被收录,下一个
                traceback.print_exc()
                cur.execute('UPDATE baidu_index_words SET flag = -1,datetime = %s WHERE id = %s ',
                            [time.strftime('%Y-%m-%d %H:%M:%S'), id])  # 未收录
                conn.commit()
            except  Exception as e:
                if not isinstance(e, KeyError):
                    traceback.print_exc()
                    print('we should break')
                    print(e)
                continue
            else:
                '''更新当前关键字 标识'''
                cur.execute('UPDATE baidu_index_words SET flag = 1,datetime = %s WHERE id = %s ',
                            [time.strftime('%Y-%m-%d %H:%M:%S'), id])
                conn.commit()
        else:
            break


def single_joint(dir,refer_date,origin_width,origin_margin_left, word,cur, conn):
    # cur.execute("SELECT * FROM baidu_index WHERE id = %s", [id])
    # row_info = cur.fetchall()[0]
    #
    # print(id, row_info)
    # margin_left = [int(x) for x in row_info['margin_left'].split(',')]
    # width = [int(x) for x in row_info['width'].split(',')]
    # location = row_info['location']
    # dir = row_info['dir']
    # refer_date = row_info['refer_date_begin']

    margin_left = [int(x) for x in origin_margin_left.split(',')]
    width = [int(x) for x in origin_width.split(',')]
    location = r'%s\%s.png'%(dir,refer_date)
    dir = dir
    refer_date = refer_date
    # print(margin_left,width,location,dir,refer_date)
    file_path = '%s\\Puzzle%s.png' % (dir, refer_date)
    try:
        origin_img = Image.open(location)
        w, h = origin_img.size  # 返回当前图片宽,长元组
        target = Image.new('RGB', (sum(width), h))
        # origin_img.show()
        for i in range(len(width)):
            img_crop = origin_img.crop((margin_left[i], 0, width[i] + margin_left[i], h))
            target.paste(img_crop, (sum(width[0:i]), 0, sum(width[0:i + 1]), h))  # 切片运算符是左开右闭
            # target.show()
        # target.show()
        target.save(file_path)

        # image识别
        num = img_recognition(dir, refer_date)
        print('recognition is ' + num)
        # cur.execute('UPDATE  baidu_index SET process_status = 1,recognitions = %s WHERE id = %s',
        #             [int(num), id])
        cur.execute(
            'INSERT INTO `baidu_index` (dir,word,width,margin_left,img_url,location,time,refer_date_begin,refer_date_end,process_status,recognitions) '
            'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            [
                dir, word, origin_width, origin_margin_left, '',
               location,
                time.strftime('%Y-%m-%d %H:%M:%S'), refer_date, refer_date,1,int(num)
            ]
        )
        conn.commit()
        return dir, refer_date
    except Exception as e:
        print(e)


def procss_local(redis_name, dest_name):
    '''
    处理图像识别
    :return:
    '''
    conn, cur = mysqlConn()
    redis_conn = redisConn.myRedisQueue('118.25.41.135', 6379, 'mhbredis', db=5)
    print('this new process has been invoked ,pid as %s' % (os.getpid()))
    time_wait = 10
    while True:
        try:
            info = redis_conn.redis.brpoplpush(redis_name, dest_name, 30)
            print('got info %s', info)
            if info:
                # dir|refer_date|width|margin_left|now
                info = info.split('|')
                dir = info[0]
                refer_date = info[1]
                width = info[2]
                margin_left = info[3]
                word=info[5]
                single_joint(dir,refer_date,width,margin_left, word,cur, conn)
                # pool.apply_async(single_joint,args=(id,))
                # dir, refer_date = single_joint(id)

                time_wait = 10  # 重置等待时间
            else:  # 当前无
                time_wait *= 2
                print('nothing to do')
                time.sleep(time_wait)
        # except
        except Exception as e:
            traceback.print_exc()
            print(e)
            # 把redis pop的值返回
            redis_conn.redis.rpush(redis_name, redis_conn.redis.lpop(dest_name))
        finally:
            if time_wait == 10 * 2 ** 20:
                print('it seems nothing pushed in to deal with')
                break
    # pool.close()
    # pool.join()
    print('All Done')


if __name__ == '__main__':
    myThrottle = Throttle(1)
    myRedis = redisConn.myRedisQueue('118.25.41.135', 6379, 'mhbredis', db=5)
    redis_name = 'baidu_index_queue'
    redis_dest_name = '%s_backup' % (redis_name)

    process_for_request = multiprocessing.Process(target=process_request, args=(myThrottle, redis_name))
    process_for_recognition = multiprocessing.Process(target=procss_local, args=(redis_name, redis_dest_name))
    process_for_request.start()
    process_for_recognition.start()
    process_for_request.join()
    print('end for internet work')
    process_for_recognition.join()
    print('end for local work')

    # cookies_string, browser = prep_cookies()
    # headers = {
    #     'Host': 'index.baidu.com',
    #     'Connection': 'keep-alive',
    #     'Accept': '*/*',
    #     'X-Requested-With': 'XMLHttpRequest',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
    #     'Referer': 'http://index.baidu.com/?tpl=trend&word=%CE%A4%B5%C2',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Accept-Language': 'zh-CN,zh;q=0.9',
    #     'Cookie': cookies_string
    # }
    # while True:
    #     cur.execute("SELECT id,word,start,end  FROM baidu_index_words WHERE flag = 0 ORDER BY id ASC  LIMIT 1")
    #     word_info = cur.fetchall()
    #     print(word_info)
    #     if word_info:
    #         word = word_info[0]['word']
    #         id = word_info[0]['id']
    #         print('settle %s' % word)
    #         word_path = '%s_%s' % (save_path, word)
    #         if not os.path.exists(word_path):
    #             os.mkdir(word_path)
    #         # 据观察,2006-06-01开启,pc趋势具备数据,自2011-01-01之后,移动趋势具备数据,则
    #         startdate = str(word_info[0]['start'])#mysql date返回的是个date对象
    #         enddate = str(word_info[0]['end'])
    #         # baidu_index_date_generator_v2(startdate, enddate)
    #         try:
    #             startdate = date_comparision(startdate,'2006-06-01')#限定日期至少大于2006-06-01
    #             enddate = date_comparision(enddate,time_intverl(time.strftime('%Y-%m-%d'),-24*3600),-1)#限定日期不大于昨日
    #
    #             # period, res1, res2 = get_request_period(word, headers, browser)
    #             # startdate = date_comparision(startdate, period[0], 1)
    #             pc_period,all_period = split_date(startdate,enddate)
    #             print(pc_period,all_period)
    #
    #             enddate_g = enddate_generator(startdate, enddate)
    #             if  pc_period:#PC任务存在
    #                 print('start pc 任务 from %s to %s'%(pc_period[0],pc_period[1]))
    #                 pc_generator = enddate_generator(pc_period[0], pc_period[1])
    #                 while True:
    #                     try:
    #                         period_info = next(pc_generator)
    #                         period_start = period_info[0]
    #                         period_end = period_info[1]
    #                         print(period_info)
    #                         # 处理文件
    #                         get_request(word, period_start, period_end, headers, word_path, browser)
    #                     except StopIteration:
    #                         print('date all done')
    #                         break
    #                     except Exception as e:
    #                         if not isinstance(e, StopIteration):
    #                             traceback.print_exc()
    #                             print('we should break')
    #                             print(e)
    #                             break
    #             if all_period:#整体任务存在
    #                 print('start 整体人物  from %s to %s' % (all_period[0], all_period[1]))
    #                 all_generator = enddate_generator(all_period[0], all_period[1])
    #                 while True:
    #                     try:
    #                         period_info = next(all_generator)
    #                         period_start = period_info[0]
    #                         period_end = period_info[1]
    #                         print(period_info)
    #                         # 处理文件
    #                         get_request(word, period_start, period_end, headers, word_path, browser)
    #                     except StopIteration:
    #                         print('date all done')
    #                         break
    #                     except Exception as e:
    #                         if not isinstance(e, StopIteration):
    #                             traceback.print_exc()
    #                             print('we should break')
    #                             print(e)
    #                             break
    #
    #         except KeyError as e:  # PPval未被定义res1,res2表现为该关键字未被收录,下一个
    #             traceback.print_exc()
    #             cur.execute('UPDATE baidu_index_words SET flag = -1,datetime = %s WHERE id = %s ',
    #                         [time.strftime('%Y-%m-%d %H:%M:%S'), id])  # 未收录
    #             conn.commit()
    #         except  Exception as e:
    #             if not isinstance(e, KeyError):
    #                 traceback.print_exc()
    #                 print('we should break')
    #                 print(e)
    #             continue
    #         else:
    #             '''更新当前关键字 标识'''
    #             cur.execute('UPDATE baidu_index_words SET flag = 1,datetime = %s WHERE id = %s ',
    #                         [time.strftime('%Y-%m-%d %H:%M:%S'), id])
    #             conn.commit()
    #     else:
    #         break

    # browser.close()

    # joint(words[0])
