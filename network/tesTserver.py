#!/usr/local/bin/local/python3

from socket import *
from time import ctime
import threading

HOST = '0.0.0.0'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

def handleSocket(cliSock,cliAddr):
    print('Connection Accepted')
    cliSock.send(b'Welcome!,%s'%((str(addr))).encode())
    while True:
        msg = cliSock.recv(BUFSIZE)
        if not msg or msg.decode() == 'exit':
            break
        print('[%s] Recv message :%s'%(ctime(),msg.decode()))
    try:
        cliSock.close()
    except:
        pass
    finally:
        print('Close connection from ',cliAddr)



# while True:
#     print('''waiting for connection...''')
#     tcpCliSock, addr = tcpSerSock.accept()
#     print('this is node', tcpCliSock, addr)
#     print('''...connected from:''' ,addr)
#
#     while True:
#         data = tcpCliSock.recv(BUFSIZE)
#         if not data:
#             break
#         tcpCliSock.send(b'[%s] %s' % (ctime().encode('utf-8'), data))
#     tcpCliSock.close()
print('waiting for connected...')
while True:
    tcpCliSock,addr = tcpSerSock.accept()
    try:
        new_thread=threading.Thread(target=handleSocket,args=( tcpCliSock,addr))
        new_thread.start()
    except:
        tcpSerSock.close()

