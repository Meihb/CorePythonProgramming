#!/usr/local/bin/local/python3

from socket import *
from time import ctime

HOST = '0.0.0.0'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print('''waiting for connection...''')
    tcpCliSock, addr = tcpSerSock.accept()
    print('this is node', tcpCliSock, addr)
    print('''...connected from:''' ,addr)

    while True:
        data = tcpCliSock.recv(BUFSIZE)
        if not data:
            break
        tcpCliSock.send(b'[%s] %s' % (ctime().encode('utf-8'), data))
    tcpCliSock.close()
tcpSerSock.close()