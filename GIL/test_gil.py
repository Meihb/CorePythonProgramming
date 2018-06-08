import os, time

'''
每一个python程序都会产生一个独立的进程
'''


def test_sleep():
    print(os.getpid())
    time.sleep(1000)


if __name__=='__main__':
    test_sleep()