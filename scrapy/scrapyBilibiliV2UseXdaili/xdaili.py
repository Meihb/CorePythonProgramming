import sys
import time
import hashlib
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context  # 关闭ssl证书验证
requests.packages.urllib3.disable_warnings()
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
print(sign)
auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp

print(auth)
proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
headers = {"Proxy-Authorization": auth}

url = 'https://api.bilibili.com/x/v2/reply?oid=4590790&pn=1&type=1&sort=0&psize=20'
r = requests.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
print(r.status_code)
print(r.content)
print(r.status_code)


# r = requests.get("https://www.tianyancha.com/company/2602017365", headers=headers, proxies=proxy, verify=False,allow_redirects=False)
# print(r.status_code)
# print(r.content)
# print(r.status_code)
# if r.status_code == 302 or r.status_code == 301 :
#     loc = r.headers['Location']
#     url_f = "https://www.tianyancha.com" + loc
#     print(loc)
#     r = requests.get(url_f, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
#     print(r.status_code)
#     print(r.text)
