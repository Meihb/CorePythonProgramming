#!/usr/local/bin/python3
from atexit import register
from random import randrange
from threading import Thread, current_thread
from time import ctime, sleep
from threading import Lock, RLock


class CleanOutPutSet(set):
    def __init__(self):
        set.__init__(self)
        self.name = 'mhb'

    def __str__(self):
        return ','.join(x for x in self)


# randrange随机数生成函数
# range 生成可迭代的 自增列
loops = (randrange(2, 5) for x in range(randrange(3, 7)))
remaining = CleanOutPutSet()
lock = RLock()


# def loop(nsec):
#     myname = current_thread().name
#     lock.acquire()
#     remaining.add(myname)
#     print('[%s] started %s' % (ctime(), myname))
#     lock.release()
#
#     sleep(nsec)
#     lock.acquire()
#     remaining.remove(myname)
#     print('[%s] completed %s occuping %d secs' % (ctime(), myname, nsec))
#     print('(remaining:%s)' % (remaining or 'NONE'))
#     lock.release()


#使用上下文管理器 获取/释放锁
def loop(nsec):
    myname = current_thread().name
    with lock:
        remaining.add(myname)
        print('[%s] started %s' % (ctime(), myname))

    sleep(nsec)
    with lock:
        remaining.remove(myname)
        print('[%s] completed %s occuping %d secs' % (ctime(), myname, nsec))
        print('(remaining:%s)' % (remaining or 'NONE'))

def _main():
    for pause in loops:
        Thread(target=loop, args=(pause,)).start()


@register
def _atexit():
    print('all DONE at:', ctime())


_main()


def decorater(func):
    def prefixName(*args, **kwargs):
        print('decoreted!')
        func(*args, **kwargs)

    return prefixName
