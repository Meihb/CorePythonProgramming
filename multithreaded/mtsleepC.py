#/usr/local/bin/python3
# -*- coding:utf-8 -*-


import threading
from time import ctime,sleep

loops = [4,2]
def loop(nloop,nsec):
    print('start loop %s at %s'%(nloop,ctime()))
    sleep(nsec)
    print('loop %s done at %s'%(nloop,ctime()))



def main():
    print('start at ',ctime())
    nloops  = range(len(loops))
    threads = []
    for i in nloops:
        t = threading.Thread(target=loop,args=(i,loops[i]))
        threads.append(t)

    for i in threads:
        i.start()#start threads

    for i in  threads:
        i.join()#wait for all threads to finish


    print('done at ',ctime())

if __name__=='__main__':
    main()
