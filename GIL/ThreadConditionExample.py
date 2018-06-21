from threading import  Condition
import  time,os,threading

import threading


def run(n):
    con.acquire()
    con.wait()
    print("run the thread: %s" % n)
    con.release()


if __name__ == '__main__':

    con = threading.Condition()
    for i in range(10):
        t = threading.Thread(target=run, args=(i,))
        t.start()

    while True:
        inp = input('>>>')
        if inp == 'q':
            break
        con.acquire()
        con.notify(int(inp))#排名靠前的int个线程被取消阻塞
        con.release()