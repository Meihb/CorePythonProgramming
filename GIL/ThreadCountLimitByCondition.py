from threading import Condition,Thread
import  time,os,threading

class scanner(Thread):
    cond = Condition()
    def __init__(self,target,args):
        Thread.__init__(self)
        self._target = target
        self._args = args


    def run(self):
        pass



if __name__=='__main__':
    pass