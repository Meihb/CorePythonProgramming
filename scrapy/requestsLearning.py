#!/usr/bin/python3

import requests, time

'''
r = requests.get('https://api.github.com/events',params={'key':'11'})
print(r.url)
#response.text与response.content区别是,text会根据当前encoding属性自动解码,content是二级制字节流
print(r.text)
print(r.encoding)
print(r.content.decode('utf-8'))
#切换编码
r.encoding = 'gbk'
#状态码
print(r.status_code)
#内置json
print(r.json())
'''
# 原始套接字
# r = requests.get('https://api.github.com/events',stream = True)
# print(r.raw.read(10))


# post请求
# r = requests.post('http://httpbin.org/post',
#                   data={'name':'meihb','key1':('as','bc')},
#                   headers = {'User-Agent':'new_user'},
#                   params = {'ame':'bolink'}
#                   )
# print(r.text)

# Cookie
# 获取cookie
# r = requests.get( 'http://example.com/some/cookie/setting/url')
# for cookie in r.cookies:
#     print(cookie)
# print(r.cookies)
# 设置cookie
# r = requests.get('http://httpbin.org/cookies',cookies ={'cookie_name':'12'})
# print(r.text)

# Cookie对象
jar = requests.cookies.RequestsCookieJar()
jar.set('test_cookie1', 'yum1', domain='httpbin.org', path='/cookies')
jar.set('test_cookie2', 'yum2', domain='httpbin.org', path='/cookies')
r = requests.get('http://httpbin.org/cookies', cookies=jar)
print(r.text)
cookies = r.cookies
print(cookies)
print('; '.join(['='.join(item) for item in cookies.items()]))
