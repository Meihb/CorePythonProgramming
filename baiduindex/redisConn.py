#!/usr/bin/python3
#coding utf8

import  redis


class myRedisQueue(object):
    '''
    redis默认db数量为0-15,可在redis.conf中配置databases 16修改
    '''
    def __init__(self,host,port,pwd,db=1):
        object.__init__(self)
        self.redis = redis.Redis(host=host,port=port,password=pwd,db=db)


    def push(self,name,value):
        return self.redis.lpush(name,value)

    def pop(self,name):
        return self.redis.rpush(name)


if __name__=='__main__':
    # print(myRedisQueue)
    myQueue = myRedisQueue('118.25.41.135',6379,'mhbredis')
    i = 0
    while True:
        if i<10*365*1000:
            myQueue.push('test',i)
            i +=1
        else:
            break
    print(myQueue.redis.dbsize())