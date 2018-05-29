#!/usr/bin/python3
#coding utf8

import  redis

r = redis.Redis(host='118.25.41.135',port=6379,password='mhbredis')
print(r.ping())
