#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from PIL import Image
import requests
import time
import re
import urllib
import pytesseract
import traceback
from http import cookiejar

save_path = r'D:\download\baiduINdex'
chromeDriver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'  # chromedriver路径
tesseract_exe = r'D:\software\dev\Tesseract-OCR\tesseract.exe'  # tesseract.exe路径
bd_account = '13851020274'  # 百度账号
bd_pwd = 'mhb12121992'  # 百度密码

bd_url = 'http://index.baidu.com/?tpl=trend'


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
    try:  # 显性等待,通过until/until_not 实现自定义的目标
        WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.ID, 'TANGRAM__PSP_4__userName')))
        # WebDriverWait(browser, 10, 0.5).until(lambda driver: driver.find_element_by_class_name('lb'))
        browser.find_element_by_id('TANGRAM__PSP_4__userName').clear()
        browser.find_element_by_id('TANGRAM__PSP_4__userName').send_keys('13851020274')
        browser.find_element_by_id('TANGRAM__PSP_4__password').clear()
        browser.find_element_by_id('TANGRAM__PSP_4__password').send_keys('mhb12121992')

        browser.find_element_by_id('TANGRAM__PSP_4__submit').submit()  # 确认登录

        time.sleep(2)#添加延迟以保证cookie获取完全
        cookies = browser.get_cookies()
        new_cookies = ''
        for cookie in cookies:
            new_cookies += cookie['name'] + '=' + cookie['value'] + ';'
        new_cookies = new_cookies[:-1]  # 去掉末尾;
        return new_cookies,browser
    except  NoSuchElementException as e:
        print('111' + e.msg)
        exit()
    except StaleElementReferenceException as e:
        print('222' + e.msg)
        exit()
    except TimeoutException as e:
        print('333' + e.msg)
        exit()

#存储cookies
def save_cookies(cookies):
    filename = 'FileCookieJar.txt'
    with open(filename) as f:
        pass

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


def get_request(word, startdate, enddate):
    cookies_string,browser = prep_cookies()
    headers = {
        'Host':'index.baidu.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Cookie':cookies_string
    }
    # browser.add_cookie(cookies)
    browser.get('http://index.baidu.com/?tpl=trend&word=%s'%(word))
    # url = 'http://index.baidu.com/Interface/Search/getSubIndex/?res={}&res2={}&type=0&startdate={}&enddate={}&forecast=0&word={}'.format(
    #     res, res2, startdate, enddate, word)
    # req = requests.get(url, headers=headers)
    # print(req)


if __name__ == '__main__':
    words = ['s','百年孤独','rng']
    cookies_string,browser = prep_cookies()
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
    browser.get('http://index.baidu.com/?tpl=trend&word=%s'%(words[0]))



