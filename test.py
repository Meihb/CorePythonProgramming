#/usr/local/bin/python3

import tkinter

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
    response = request.urlopen("http://index.baidu.com/?tpl=trend&word=%CC%B0%CD%E6%C0%B6%D4%C2")
    html = response.read()
    print(html)
