#/usr/local/bin/python3

from socket import *
from time import  ctime



HOST = '127.0.0.1'
PORT = 21567
ADDR = (HOST,PORT)

while True:
    tcpCliSock = socket(AF_INET,SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    data = input('>')
    if not data or data.encode()=='exit':
        break
    tcpCliSock.send(b'%s\r\n'%(data.encode()))
    data = tcpCliSock.recv(1024)
    if not data :
        break
    print('Get message :%s  '%(data.decode()))
    tcpCliSock.close()