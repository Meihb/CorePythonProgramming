
# -*- coding: cp936 -*-
##tcp响应服务器，当与客户端建立连接后，服务器显示客户端ip和端口，同时将接收的客户端信息和'I get it!'传给客户端，此时等待输入一个新的信息传给客户端。

import socket,traceback
host='0.0.0.0'
port=12345
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))
s.listen(1)
while 1:
    try:
        clientsock,clientaddr=s.accept()
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exc()
        continue
    try:
        print("连接来自：",clientsock.getpeername())
        while 1:
            data=clientsock.recv(4096).decode()
            if not len(data):
                break
            print(clientsock.getpeername()[0]+':'+str(data))
            clientsock.sendall(data.encode())
            clientsock.sendall(("\nI get it!\n").encode())
            t=input('input the word:')
            clientsock.sendall(t.encode())
    except (KeyboardInterrupt,SystemExit):
        raise
    except:
        traceback.print_exc()
    try:
        clientsock.close()
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exc()

