# if __name__ == "__main__":
#     from urllib import request
#     #访问网址
#     url = 'http://122.112.248.56/showremoteAddr.php'
#     url = 'https://api.bilibili.com/x/v2/reply?type=1&sort=0&oid=10120347&pn=1'
#     #这是代理IP
#     proxy ={'https': 'https://113.121.243.153:47386', 'http': 'http://113.121.243.153:47386'}
#
#     # proxy=None
#     #创建ProxyHandler
#     proxy_support = request.ProxyHandler(proxy)
#     #创建Opener
#     opener = request.build_opener(proxy_support)
#     #添加User Angent
#     # opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
#     #安装OPener
#     request.install_opener(opener)
#     #使用自己安装好的Opener
#     response = request.urlopen(url)
#     #读取相应信息并解码
#     html = response.read().decode("utf-8")
#     #打印信息
#     print(html)


import sys
import time
import hashlib
import requests
import urllib.request
import ssl

# import grequests
ssl._create_default_https_context = ssl._create_unverified_context  # 关闭ssl证书验证
_version = sys.version_info

is_python3 = (_version[0] == 3)

orderno = "ZF20184206305g2nCdV"
secret = "7a3eb1b3b91b4b44ae774e6f96152da1"

ip = "forward.xdaili.cn"
port = "80"

ip_port = ip + ":" + port

timestamp = str(int(time.time()))  # 计算时间戳
string = ""
string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

if is_python3:
    string = string.encode()

md5_string = hashlib.md5(string).hexdigest()  # 计算sign
sign = md5_string.upper()  # 转换成大写
auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp

proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
headers = {"Proxy-Authorization": auth}

proxy_support = urllib.request.ProxyHandler(proxy)
#     #创建Opener
opener = urllib.request.build_opener(proxy_support)
#     #添加User Angent
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'),
                     ("Proxy-Authorization",auth)]
# opener.addheaders = headers
#     #安装OPener
urllib.request.install_opener(opener)
#     #使用自己安装好的Opener
# url = "http://122.112.248.56/showremoteAddr.php"
url = 'https://api.bilibili.com/x/v2/reply?oid=4590790&pn=1&type=1&sort=0&psize=20'
request = urllib.request.Request(url)

open = urllib.request.urlopen(request)
jscontent = open.read()
print(jscontent.decode('utf-8'))

# r = urllib.request.get("https://www.tianyancha.com/company/2602017365", headers=headers, proxies=proxy, verify=False,
#                        allow_redirects=False)
# print(r.status_code)
# print(r.content)
# print(r.status_code)
# if r.status_code == 302 or r.status_code == 301:
#     loc = r.headers['Location']
#     url_f = "http://122.112.248.56/showremoteAddr.php" + loc
#     print(loc)
#     r = requests.get(url_f, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
#     print(r.status_code)
#     print(r.text)
