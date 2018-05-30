#!/usr/bin/python3
#coding utf8

import  redis


class myRedisQueue(object):
    '''
    redis默认db数量为0-15,可在redis.conf中配置databases 16修改,密码在命令行中为 auth
    '''
    def __init__(self,host,port,pwd,db=1):
        object.__init__(self)
        self.redis = redis.Redis(host=host,port=port,password=pwd,db=db)
        self.redis.delete('back')


    def push(self,name,value):
        return self.redis.lpush(name,value)

    def pop(self,name,backname='back'):
        self.redis.brpoplpush(name,backname)
        return self.redis.rpop(name)

    def rollback(self,name,backname='back'):
        return self.redis.rpush(name,self.redis.lpop(backname))


if __name__=='__main__':
    # print(myRedisQueue)
    myQueue = myRedisQueue('118.25.41.135',6379,'mhbredis',db=0)

