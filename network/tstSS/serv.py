#/usr/local/bin/python3

from socketserver import (TCPServer as TCP,StreamRequestHandler as SRH)
from time import  ctime


HOST = '0.0.0.0'
PORT = 21567
ADDR = (HOST,PORT)

class MyRequestHandler(SRH):
    def handle(self):
        print('connected from:',self.client_address)
        self.wfile.write(b'[%s]%s'%(ctime().encode(),self.rfile.readline()))

tcpServ = TCP(ADDR,MyRequestHandler)
print('connecting...')
tcpServ.serve_forever()