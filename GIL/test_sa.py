#!/usr/bin/python3

from threading import  Thread,Semaphore
import threading,time,random

def func():
    sm.acquire()#每acquire一次返回当前计数器值,,semaphore计数器值减-,当计数器为0时,acquire会阻塞当前进程
    print('%s get sm '%(threading.current_thread().getName()))
    time.sleep(random.random()*3)
    sm.release()
    print('%s release sm ' % (threading.current_thread().getName()))




if __name__=='__main__':
    sm = Semaphore(5)
    for i in range(10):
        t = Thread(target=func)
        t.start()




