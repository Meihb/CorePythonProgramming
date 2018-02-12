from socket import *
import threading

HOST = '127.0.0.1'
# HOST = '122.112.248.56'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)

tsTcliSock = socket(AF_INET,SOCK_STREAM)
tsTcliSock.connect(ADDR)

def recvData(cliSocket,buffsize):
    while True:
        data = cliSocket.recv(buffsize)
        if data:
            print(data.decode())
        if data.decode=='exit':
            break

def sendData(cliSocket):
    while True:
        data = input('>')
        print(data)
        if not data:
            break
        cliSocket.send(data.encode('utf-8'))

recv_t = threading.Thread(target=recvData,args=(tsTcliSock,BUFSIZE))
send_t = threading.Thread(target=sendData,args=(tsTcliSock,))
recv_t.start()
send_t.start()



# while True:
#     data = input('>')
#     if not data:
#         break
#     tsTcliSock.send(data.encode('utf-8'))
#     data = tsTcliSock.recv(BUFSIZE)
#     print(data.decode('utf-8'))
#     if not data:
#         break
# tsTcliSock.close()
