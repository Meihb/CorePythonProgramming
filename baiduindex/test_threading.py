import myBaiduIndex
# coding=utf-8
import threading, time, random,os


def thread_proc(i):
    print('start %s' % i)
    time.sleep(random.random() * 3)
    print('end %s' % i)


class scanner(threading.Thread):
    '''
    event.isSet()：返回event的状态值；
    event.wait()：如果 event.isSet()==False将阻塞线程；
    event.set()： 设置event的状态值为True，所有阻塞池的线程激活进入就绪状态， 等待操作系统调度；
    event.clear()：恢复event的状态值为False。
    '''
    tlist = []  # 用来存储队列的线程
    maxthreads = 5  # int(sys.argv[2])最大的并发数量，测试下系统最大支持1000多个
    evnt = threading.Event()  # 用事件来让超过最大线程设置的并发程序等待
    lck = threading.Lock()  # 线程锁

    def __init__(self, target, args):
        threading.Thread.__init__(self)
        self._target = target
        self._args = args

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except Exception as e:
            print(e)
        # 以下用来将完成的线程移除线程队列
        scanner.lck.acquire()
        print(scanner.tlist)
        scanner.tlist.remove(self)
        # 如果移除此完成的队列线程数刚好达到max-1，则说明有线程在等待执行，那么我们释放event，让等待事件执行
        if len(scanner.tlist) == scanner.maxthreads - 1:
            scanner.evnt.set()
            scanner.evnt.clear()
        scanner.lck.release()

    def newthread(target, args):
        '''

        :param  function  call:
        :param args:
        :return:
        '''
        scanner.lck.acquire()  # 上锁
        sc = scanner(target,args)
        scanner.tlist.append(sc)
        scanner.lck.release()  # 解锁
        sc.start()

    # 将新线程方法定义为静态变量，供调用
    newthread = staticmethod(newthread)


def runscan():
    for i in range(0, 20):
        scanner.lck.acquire()
        # 如果目前线程队列超过了设定的上线则等待。
        if len(scanner.tlist) >= scanner.maxthreads:
            scanner.lck.release()
            scanner.evnt.wait()  # scanner.evnt.set()遇到set事件则等待结束
        else:
            scanner.lck.release()
        scanner.newthread(thread_proc, args=(i,))

    for t in scanner.tlist:
        t.join()  # join的操作使得后面的程序等待线程的执行完成才继续


def process_local_threading(conn,cur):
    '''
    处理图像识别
    :return:
    '''
    print('current process {0}'.format(os.getpid()))
    time_start = int(time.time())

    cur.execute(
        'SELECT id,dir,refer_date_begin,width,margin_left,word FROM  `baidu_index` WHERE recognitions>10000  ORDER BY id ASC limit 1000 ')

    '''多线程处理,1000条记录耗时'''
    while True:
        info = cur.fetchone()
        if not info:
            break
        else:
            print('got info %s'%info)
            id = info['id']
            dir = info['dir']
            refer_date = info['refer_date_begin']
            width = info['width']
            margin_left = info['margin_left']
            scanner.lck.acquire()
            # 如果目前线程队列超过了设定的上线则等待。
            if len(scanner.tlist) >= scanner.maxthreads:
                scanner.lck.release()
                scanner.evnt.wait()  # scanner.evnt.set()遇到set事件则等待结束
            else:
                scanner.lck.release()
            scanner.newthread(target=myBaiduIndex.single_joint, args=(dir, refer_date, width, margin_left, id,id))
            # t = threading.Thread(target=myBaiduIndex.single_joint,args=(dir, refer_date, width, margin_left, id,conn,cur))
            # threading_list.append(t)
    for t in scanner.tlist:
        t.join()  # join的操作使得后面的程序等待线程的执行完成才继续

    time_end = int(time.time())
    print('lasts %s' % (time_end - time_start))
    print('All Done')

if __name__ == "__main__":
    # conn,cur = myBaiduIndex.mysqlConn()
    # process_local_threading(conn,cur)
    runscan()


# if __name__=='__main__':
#     conn,cur = myBaiduIndex.mysqlConn()
#     myBaiduIndex.process_local(conn,cur)
