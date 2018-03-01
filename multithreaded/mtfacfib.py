from myThread import MyThread
from time import ctime,sleep

def fib(x):#斐波那契数列
    sleep(0.01)
    if x<2:return 1
    return (fib(x-2)+fib(x-1))
def fac(x):#阶乘
    sleep(0.1)
    if x<2:return 1
    return fac(x-1)*x
def sum(x):#累加
    sleep(0.1)
    if x<2:return 1
    return x+sum(x-1)

funcs = [fib,fac,sum]
n=12
def main():
    nfuncs = range(len(funcs))

    print('SINGLE THREAD')
    for i in nfuncs:
        print('starting %s at %s'%(funcs[i].__name__,ctime()))
        print(funcs[i](n))
        print(funcs[i].__name__,'finished at ',ctime())

    print('MULTIPLE THREADS')
    threads = []
    for i in nfuncs:#初始化线程,存入list中
        t = MyThread(funcs[i],(n,),funcs[i].__name__)
        threads.append(t)

    for i in  nfuncs:#同时开启各线程
        threads[i].start()

    for i in  nfuncs:#挂起主线程
        threads[i].join()
        print(threads[i].getResult())

    print('all Done')

if __name__=='__main__':
    main()
