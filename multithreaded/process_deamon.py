from multiprocessing import Process
import time
def foo():
    print(123)
    time.sleep(1)
    print("end123")

def bar():
    print(456)
    time.sleep(3)
    print("end456")

'''
** = 进程/线程
守护** 的生存时间取决于主**的运行结束时间,对主进程来说,自己代码块结束即运行结束、对于主线程代码块运行结束尚需等待非守护子线程运行结束才算运行结束
'''

if __name__=='__main__':
    p1 = Process(target=foo)
    p2 = Process(target=bar)

    p1.daemon = True  # 守护化,会等待主线程运行完毕才回收，更换ti、t2,结果不同
    p1.start()
    p2.start()
    print(2)
    print("main-------")