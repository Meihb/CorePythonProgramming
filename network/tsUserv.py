#!/usr/local/bin/python3

from socket import *
from time import ctime

HOST = '0.0.0.0'
PORT = 21568
BUFSIZE = 1024
ADDR = (HOST, PORT)

udpServer = socket(AF_INET,SOCK_DGRAM)
udpServer.bind(ADDR)

while True:
    print('waiting for message...')
    data,addr = udpServer.recvfrom(BUFSIZE)
    print(type(b'[%s] %s'%(ctime().encode('utf-8'),data)))
    udpServer.sendto(b'[%s] %s'%(ctime().encode('utf-8'),data),addr)

    print('received from and returned to :',addr)
udpServer.close()