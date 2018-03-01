from urllib import request
from atexit import register
import re

# REGEX = compile('')
URL = 'http://fanyi.baidu.com#en/zh'
word = input('Please input the english word:')
if __name__ == "__main__":
    response = request.urlopen("http://fanyi.baidu.com#en/zh")
    html = response.read().decode()
    print(html)
