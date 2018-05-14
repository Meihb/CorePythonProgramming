#!/usr/bin/python3
from selenium import webdriver
import myBaiduIndex
from requests import cookies
import requests

myCookies = myBaiduIndex.prep_cookies()

jar = cookies.RequestsCookieJar()

for mycookie in myCookies:
    mycookie.pop('httpOnly')
    if 'expiry' in mycookie:
        mycookie.pop('expiry')
    jar.set(**mycookie)

# chromeDriver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
# browser = webdriver.Chrome(chromeDriver)
# browser.add_cookie(jar)
# browser.get('http://index.baidu.com/?tpl=trend&word=s')
r = requests.get('http://index.baidu.com/?tpl=trend&word=s',cookies=jar)
print(r.text)
print(r.headers)
print(r.cookies)
# print(jar)