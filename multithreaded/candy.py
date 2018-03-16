#!/usr/local/bin.python3

from atexit import register
from random import randrange
from threading import BoundedSemaphore,RLock,Thread
from time import ctime,sleep

lock = RLock()#操作锁
MAX = 5
candytray= BoundedSemaphore(MAX)

def refill():
    with lock:
        print('Refilling candy...')
        try:
            candytray.release()
        except ValueError:
            print('full,skipping')
        else:
            print('OK')

def buy():
    with lock:
        print('Buying candy...')
        if candytray.acquire(False):
            print('ok')
        else:
            print('empty,skipping')

def producer(loops):
    for i in range(loops):
        refill()
        sleep(randrange(3))

def consumer(loops):
    for i in range(loops):
        buy()
        sleep(randrange(3))

def main():
    print('starting at',ctime())
    nloops = randrange(2,6)
    print('THE CANDY MACHINE (full with %d bars)!'%(MAX,))

    Thread(target=consumer,args=(randrange(nloops,nloops+MAX+2),)).start()#buyer
    Thread(target=producer,args=(nloops,)).start()#consumer

@register
def _atexit():
    print('All Done at',ctime())

if __name__=='__main__':
    main()


