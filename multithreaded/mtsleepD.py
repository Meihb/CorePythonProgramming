#/usr/local/bin/python3
# -*- coding:utf-8 -*-


import threading
from time import ctime,sleep

loops = [4,2]

class ThreadFunc(object):
    def __init__(self,func,args,name=''):
        self.name = name
        self.func = func
        self.args = args
    def __call__(self,*args):#允许对实例仿照func调用
        if args:
            true_args = args
        else:
            true_args = self.args
        self.func(*true_args)

def loop(nloop,nsec):
    print('start loop %s at %s'%(nloop,ctime()))
    sleep(nsec)
    print('loop %s done at %s'%(nloop,ctime()))



def main():
    print('start at ',ctime())
    nloops  = range(len(loops))
    threads = []
    for i in nloops:
        tf = ThreadFunc(loop,(i,loops[i]),loop.__name__)
        t = threading.Thread(target=tf,args=(i,2*loops[i]))
        threads.append(t)

    for i in threads:
        i.start()#start threads

    for i in  threads:
        i.join()#wait for all threads to finish


    print('done at ',ctime())


if __name__=='__main__':
    main()
