#/usr/local/bin/python3
import threading
from time import ctime,sleep
import _thread

def loop0():
    print('start loop 0 at ',ctime())
    sleep(4)
    print('loop 0 done at',ctime())

def loop1():
    print('start loop 1 at ',ctime())
    sleep(2)
    print('loop 1 done at',ctime())

def main():
    print('start at ',ctime())
    _thread.start_new_thread(loop0,())
    _thread.start_new_thread(loop1,())
    sleep(5)
    print('done at ',ctime())

if __name__=='__main__':
    main()
