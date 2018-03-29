#!/usr/local/bin/python3

import asyncio
import time

now = lambda: time.time()


async def do_some_work(x,awaitFlag=False):#async定义一个协程对象
    print('Start at :',time.ctime())
    if awaitFlag:
        await  asyncio.sleep(x)
    print ('Done at:',time.ctime())
    return ('work %s Done' )%(x,)

def callBack(future):
    print('Callback:',future.result())

start = now()
coroutine = do_some_work(2,True)
coroutine2 = do_some_work(4,True)
Loop = asyncio.get_event_loop()

# task = asyncio.ensure_future(coroutine) #第二种生成task方式
task = Loop.create_task(coroutine)
task.add_done_callback(callBack)

task2 = Loop.create_task(coroutine2)
task2.add_done_callback(callBack)
print(task)
Loop.run_until_complete(task)
Loop.run_until_complete(task2)
print(task)


print('TIME:',now()-start)

