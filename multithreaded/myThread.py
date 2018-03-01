#/usr/local/bin/python3

import threading
from time import ctime

class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def getResult(self):
        return self.res

    def run(self):
        print('starting %s at %s'%(self.name,ctime()))
        self.res = self.func(*self.args)
        print(self.name,'finished at %s'%ctime())
