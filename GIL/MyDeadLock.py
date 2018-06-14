#!/usr/bin/python3

from threading import Thread,Lock,RLock
import os,time,threading

ALock = Lock()
BLock = Lock()

def work1():
    ALock.acquire()
    print('\033[41;%s get Alock'%(threading.))
    time.sleep(1)
    BLock.acquire()

    ALock.release()
    BLock.release()
def