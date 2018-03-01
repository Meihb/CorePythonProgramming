#/usr/local/bin/python3
# -*- coding:utf-8 -*-


import threading
from time import ctime,sleep
import _thread

loops = [4,2]
def loop(nloop,nsec,lock):
    print('start loop %s at %s'%(nloop,ctime()))
    sleep(nsec)
    print('loop %s done at %s'%(nloop,ctime()))
    lock.release()



def main():
    print('start at ',ctime())
    locks = []
    nloops  = range(len(loops))
    for i in loops:
        lock = _thread.allocate_lock()
        lock.acquire()
        locks.append(lock)

    for i in nloops:
        _thread.start_new_thread(loop,(i,loops[i],locks[i]))

    for i in nloops:
        while locks[i].locked():#使用while循环等待当前锁release,while的区别
            pass
    print('done at ',ctime())

if __name__=='__main__':
    main()
