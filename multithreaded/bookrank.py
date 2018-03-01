#!/usr/local/bin/python3

from atexit import register
from re import  compile
from threading import Thread
from time import ctime
from urllib.request import  urlopen

REGEX = compile('#([\d,]+) in Books')
AMZN = 'https://amazon.cn/dp'
ISBNs = {
    '0132269937':'Core Python',
    '0132356139':'Python Web Development with Django',
    '0137143419':'Python Fundamentals'
}

def getRanking(isbn):
    page = urlopen('%s%s'%(AMZN,isbn))
    data = page.read()
    page.close()
    print(data)
    return REGEX.findall(data)[0]

def _showRanking(isbn):#单下划线函数表示只能被本模块代码调用
    print ('-%r ranked %s'%(ISBNs[isbn],getRanking(isbn)))

def _main():
    print('At %s on Amazon...'%ctime())
    for isbn in ISBNs:
        _showRanking(isbn)

@register
def _atexit():
    print('all DONE at :',ctime())

if __name__=='__main__':
    _main()