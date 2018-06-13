import os, time,dis
from threading import Thread

'''
每一个python程序都会产生一个独立的进程
'''


def test_sleep():
    print(os.getpid())
    time.sleep(1000)


def countdown(n):
    while n > 0:
        # print(n)
        n -= 1


def get_duration(callfunc):
    def wrapper(*args, **kwargs):
        print('start measuring time length')
        time1 = time.time()
        result = callfunc(*args, **kwargs)
        time2 = time.time()
        print('costs %s s' % (int(time2) - int(time1)))
        return result

    return wrapper


@get_duration
def test_count_1(COUNT):
    countdown(COUNT)


@get_duration
def test_count_2(COUNT):
    t1 = Thread(target=countdown, args=(COUNT // 2,))
    t2 = Thread(target=countdown, args=(COUNT // 2,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()




if __name__ == '__main__':
    COUNT = 100000000
    # print(COUNT // 2, COUNT / 2)  # //返回整数除法结果,/浮点数除法结果
    # test_count_1(COUNT)
    # test_count_2(COUNT)

    dis.dis(countdown)