from threading import Thread, Lock

'''
threading.Lock 不是一个简单的 互斥锁对象,处于threading模块下当期阻塞时, 
他会强迫当前进程交出gil权限
'''
import os, time


def work():
    global n
    temp = n
    time.sleep(0.1)
    n = temp - 1


def work_sequence():
    global n
    lock.acquire()
    temp = n
    n = temp - 1
    lock.release()


if __name__ == '__main__':
    n = 100
    l = []
    lock = Lock()
    for i in range(100):
        p = Thread(target=work_sequence)
        l.append(p)
        p.start()
    for p in l:
        p.join()

    print(n)  # 结果可能为99
