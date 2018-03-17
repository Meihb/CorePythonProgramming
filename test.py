#/usr/local/bin/python3

def son():
    text = input('speak:')
    if text=='exit':
        return
    else:
        print('B{}'.format(text))

# son()

from urllib import request
from atexit import register
import re

# REGEX = compile('')
if __name__ == "__main__":
    response = request.urlopen("http://fanyi.baidu.com#en/zh")
    html = response.read().decode()
    print(html,'')
