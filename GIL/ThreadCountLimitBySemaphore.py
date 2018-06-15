#!/usr/bin/python3

from threading import Event, Thread, Lock,Semaphore
import threading, random, time,traceback


def thread_proc(i):
    print(' start  %s  %s' % (threading.current_thread().getName(), time.strftime("%Y-%m-%d %H:%m:%S")))
    time.sleep(random.random() * 3)
    print(' end  %s  %s' % (threading.current_thread().getName(), time.strftime("%Y-%m-%d %H:%I:%S")))

class scanner(Thread):
    sm = Semaphore(5)#最大线程数

    def __init__(self,target,args):
        Thread.__init__(self)
        self._target = target
        self._args = args

    def run(self):
        try:
            self._target(*self._args)
        except Exception as e:
            traceback.print_exc()
            print(e)
        scanner.sm.release()





def test():
    for i in  range(0,30):
        print('\033[0;37;44m before is %s \033[0m   '%(time.strftime('%Y-%m-%d %H:%M:%S'),))
        scanner.sm.acquire()
        print('\033[44m end is %s\033[0m  '%(time.strftime('%Y-%m-%d %H:%M:%S'),))
        sc = scanner(target=thread_proc,args=(i,))
        sc.start()

if __name__=='__main__':
    test()
