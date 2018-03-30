import time
import asyncio

async def do_some_work(x):
    print('Waiting:%ds'%x)
    await  asyncio.sleep(x)#await=yield from，调用一个协程