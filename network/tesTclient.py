from socket import *


HOST = '127.0.0.1'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)

tsTcliSock = socket(AF_INET,SOCK_STREAM)
tsTcliSock.connect(ADDR)
print(tsTcliSock)

while True:
    data = input('>')
    if not data:
        break
    tsTcliSock.send(data.encode('utf-8'))
    data = tsTcliSock.recv(BUFSIZE)
    print(data.decode('utf-8'))
    if not data:
        break
tsTcliSock.close()
