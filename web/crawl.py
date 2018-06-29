#!/usr/bin/python3

import io
import formatter
from html.parser import HTMLParser
import  http.client
import os
import sys
import urllib
from  urllib.parse import urlparse

class Retriever(object):
    '''
    当一个类需要创建大量实例时，可以通过__slots__声明实例所需要的属性,
    例如，class Foo(object): __slots__ = ['foo']。
    这样做带来以下优点：
    更快的属性访问速度,减少内存消耗
    '''
    __slots__ = ('url','file')
    def __init__(self,url):
        self.url,self.file  = self.get_file(url)
    def get_file(self,url,default='index.html'):
        'Create useable local filename from URL'
        parsed = urlparse((url))
        host = parsed.netloc.split('@')[-1].split(':')[0]
        filepath = '%s%s'%(host,parsed.path)
        if not os.path.splitext(parsed.path)[1]:
            filepath = os.path.join(filepath,default)
        linkdir = os.path.dirname(filepath)
        if not os.path.isdir(linkdir):
            if os.path.exists(linkdir):
                os.unlink(linkdir)
            os.makedirs(linkdir)
        return url,filepath

    def download(self):
        'Download URL '