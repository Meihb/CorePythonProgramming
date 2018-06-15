#!/usr/bin/python3

from threading import Thread,Lock,RLock
import os,time,threading

ALock = RLock()
BLock = RLock()

def work1():
    ALock.acquire()
    print('\033[41m%s get Alock\033[0m'%(threading.current_thread()))
    time.sleep(1)
    BLock.acquire()

    BLock.release()
    ALock.release()
def work2():
    BLock.acquire()
    print('\033[41m%s get Block\033[0m'%(threading.current_thread()))
    time.sleep(1)
    ALock.acquire()

    ALock.release()
    BLock.release()

if __name__=='__main__':
    t1 = Thread(target=work1)
    t2 = Thread(target=work2)

    t1.start()
    t2.start()

