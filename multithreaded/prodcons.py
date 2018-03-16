#!/usr/local/bin/python3

from random import randint
from time import sleep
from queue import Queue
from myThread import MyThread


def writeQ(queue):
    print('producing object for Q...')
    queue.put('xxx',True)
    print('size now is ',queue.qsize())

def readQ(queue):
    val = queue.get(True)
    print('consumed pbject from Q...','size now is ',queue.qsize())

def writer(queue,loops):
    for i in  range(loops):
        writeQ(queue)
        sleep(randint(2,5))

def reader(queue,loops):
    for i in range(loops):
        readQ(queue)
        sleep(randint(2,5))

funcs = [writer,reader]
nfuncs = range(len(funcs))
print(nfuncs)
def main():
    nloops = randint(2,5)
    q = Queue(32)
    threads = []

    for index in nfuncs:
        t = MyThread(funcs[index],(q,nloops),funcs[index].__name__)
        threads.append(t)
    for i in nfuncs:
        threads[i].start()
    for i in nfuncs:
        threads[i].join()

    print('All Done')

if __name__=='__main__':
    main()