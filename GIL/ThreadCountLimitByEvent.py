#!/usr/bin/python3

from threading import Event, Thread, Lock
import threading, random, time


def thread_proc(i):
    print(' start  %s  %s' % (threading.current_thread().getName(), time.strftime("%Y-%m-%d %H:%I:%S")))
    time.sleep(random.random() * 3)
    print(' end  %s  %s' % (threading.current_thread().getName(), time.strftime("%Y-%m-%d %H:%I:%S")))


class scanner(Thread):
    event = Event()
    lck = Lock()
    tlist = []
    MaxThreads = 5

    def __init__(self, target, args):
        Thread.__init__(self)
        self._target = target
        self._args = args

    def run(self):
        try:
            self._target(*self._args)
        except Exception as e:
            print(e)
        scanner.lck.acquire()
        scanner.tlist.remove(self)  # 移除当前已完成的线程任务

        if len(scanner.tlist) == scanner.MaxThreads - 1:  # 当前线程队列不满,可再次开启新任务
            scanner.event.set()
            # time.sleep(2)#其实我个人认为在这个地方是有bug的,若此处运行不顺,可能会导致放出多个线程任务
            # scanner.event.clear()
        else:
            pass
        scanner.lck.release()

    def addThread(self):
        scanner.lck.acquire()
        scanner.tlist.append(self)
        self.start()
        scanner.lck.release()


def test():
    for i in range(0, 100):
        scanner.lck.acquire()
        if len(scanner.tlist) >= scanner.MaxThreads:
            scanner.lck.release()
            scanner.event.wait()#若当前线程数已达最大值,阻塞当前代码,阻止其任务发布
            scanner.event.clear()
        else:
            scanner.lck.release()
        sc = scanner(target=thread_proc, args=(i,))
        sc.addThread()


if __name__=='__main__':
    test()