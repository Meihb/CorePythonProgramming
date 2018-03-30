import asyncio
import random


def fib(n):
    index, a, b = 0, 0, 1
    while index < n:
        sleep_cnt = yield b
        print('Waiting  ', sleep_cnt)
        a, b = b, a + b
        index += 1
    print('Done')
    return b


generator = fib(20)
generator.send(None)
while True:
    try:
        temp = random.randrange(2, 5)
        print('number is',temp)
        key = generator.send(random.randrange(2, 5))
    except StopIteration:
        break
    print('number is ',key)

