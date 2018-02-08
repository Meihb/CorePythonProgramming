#!/usr/local/bin/python3

from socket import *
from time import ctime

HOST = '122.112.248.56'
PORT = 21568
BUFSIZE = 1024
ADDR = (HOST, PORT)

udpClient= socket(AF_INET,SOCK_DGRAM)#udp是无连接的!

while True:
    data = input('>')
    if not data or data.encode('utf-8')=='exit':
        break
    udpClient.sendto(data.encode('utf-8'),ADDR)
    recvData,addr = udpClient.recvfrom(BUFSIZE)
    if not recvData:
        break
    print(recvData.decode('utf-8'))
udpClient.close()
