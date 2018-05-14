#!/usr/bin/python3


import requests
import http.cookiejar
import urllib.request
from selenium import webdriver

filename = 'FileCookieJar_test.txt'
def test_url():
    #初始化session类
    se = requests.session()
    print(se.cookies.get_dict())

    r = requests.get('https://www.baidu.com')
    new_cookies = r.cookies
    print(r.cookies.get_dict())


def save_cookie():
    pass




if __name__=='__main__':
    test_url()