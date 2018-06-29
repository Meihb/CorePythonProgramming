import urllib
help(urllib)
from urllib.parse import  *

'''urllib.parse.urlparse 将URL字符串拆分成组件'''
url_s = 'http://meihb:123456@www.baidu.com/s;22?word=111&time=13#key'
url_tuple = urlparse(url_s)
print(url_tuple)
'''urllib.parse.urlunparse与之相反'''
print(urlunparse(url_tuple))


import  urllib.request,urllib.error,urllib.parse

LOGIN = 'wesley'
PASSWD = "you'llNeverGuess"
URL = 'http://localhost'
REALM='Secure Archive'
