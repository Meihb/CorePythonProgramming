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
# if __name__ == "__main__":
#     response = request.urlopen("http://index.baidu.com/?tpl=trend&word=%CC%B0%CD%E6%C0%B6%D4%C2")
#     html = response.read()
#     print(html)


def MyGenerator():
    value = yield 1
    yield value
    return 'done'

gen = MyGenerator()
print(next(gen))
print(gen.send(' I am Value'))


def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)#send(None) = next()
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

# c = consumer()
# produce(c)

import  time
tss1 = '2013-10-10 23:40:00'
tm = time.strptime(tss1, '%Y-%m-%d %H:%M:%S')

import urllib
from urllib import parse
url = 'www.baidu.com'
word = '贪玩蓝月'



# print(parse.urlencode({'word':word}))
print('http://index.baidu.com/?tpl=trend&%s'%(parse.urlencode({'word':word.encode('gb2312')})))
