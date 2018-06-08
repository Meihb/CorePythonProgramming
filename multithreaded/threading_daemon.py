from threading import Thread
import time
def foo():
    print(123)
    time.sleep(1)
    print("end123")

def bar():
    print(456)
    time.sleep(3)
    print("end456")


if __name__=='__main__':
    t1 = Thread(target=foo)
    t2 = Thread(target=bar)

    t1.daemon = True  # 守护化,会等待主线程运行完毕才回收，更换ti、t2,结果不同
    t1.start()
    t2.start()
    print(2)
    print("main-------")