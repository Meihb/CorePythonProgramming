from threading import Condition,Thread
import  time,os,threading,random


def thread_proc(i):
    print(' start  %s  %s' % (threading.current_thread().getName(), time.strftime("%Y-%m-%d %H:%I:%S")))
    time.sleep(random.random() * 3)
    print(' end  %s  %s' % (threading.current_thread().getName(), time.strftime("%Y-%m-%d %H:%I:%S")))



class scanner(Thread):
    cond = Condition()
    tlst = []
    maxthreads = 5
    def __init__(self,target,args):
        Thread.__init__(self)
        self._target = target
        self._args = args


    def run(self):
        try:
            self._target(*self._args)
        except:
            pass
        scanner.cond.acquire()
        scanner.tlst.remove(self)
        if len(scanner.tlst)>=scanner.maxthreads-1:
            scanner.cond.notify(1)
        scanner.cond.release()





if __name__=='__main__':
    for i in range(0,20):
        sc = scanner(target=thread_proc, args=(i,))
        scanner.cond.acquire()
        if len(scanner.tlst)>=scanner.maxthreads:
            scanner.cond.wait()#完全可以用wait_for(return event.status)实现cond和event的互通
            scanner.tlst.append(sc)
            sc.start()

        else:
            scanner.tlst.append(sc)
            sc.start()
        scanner.cond.release()