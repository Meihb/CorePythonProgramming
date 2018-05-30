import redisConn
import multiprocessing

def _run_proc(i,*args):

     print(i)
     print(args)


if __name__=='__main__':
     myQueue = redisConn.myRedisQueue()
     pool = multiprocessing.Pool(5)

     for i in range(0,5):
          pool.apply_async(func=_run_proc,args=(i,i+2))
     pool.close()
     pool.join()
     print('All Done')