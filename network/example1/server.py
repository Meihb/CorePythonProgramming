
# -*- coding: cp936 -*-
##tcp��Ӧ������������ͻ��˽������Ӻ󣬷�������ʾ�ͻ���ip�Ͷ˿ڣ�ͬʱ�����յĿͻ�����Ϣ��'I get it!'�����ͻ��ˣ���ʱ�ȴ�����һ���µ���Ϣ�����ͻ��ˡ�

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
        print("�������ԣ�",clientsock.getpeername())
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

