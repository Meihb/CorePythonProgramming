#/usr/local/bin/python3

import tkinter

def son():
    text = input('speak:')
    if text=='exit':
        return
    else:
        print('B{}'.format(text))

# son()

from urllib import request
from atexit import register
import re

# REGEX = compile('')
# if __name__ == "__main__":
#     response = request.urlopen("http://index.baidu.com/?tpl=trend&word=%CC%B0%CD%E6%C0%B6%D4%C2")
#     html = response.read()
#     print(html)


def MyGenerator():
    value = yield 1
    yield value
    return 'done'

gen = MyGenerator()
print(next(gen))
print(gen.send(' I am Value'))


def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)#send(None) = next()
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

# c = consumer()
# produce(c)

import  time
tss1 = '2013-10-10 23:40:00'
tm = time.strptime(tss1, '%Y-%m-%d %H:%M:%S')

str1 =r"4k0,s%,d9x,40S,9a91,A99,4C0,44b,9P0,zv,YG,34ca,Pa0,aA7,444e,o49,99D,na0,49cd,3000,444a,ja0,90A,mB,44J,aK7,a0W,x0c7,U9c7,f207,d445,Y8c7,nIc,fh07,Cr5,f8051,Aaa,xad,f8d7,M01,4y4,GQ,rK,6B,4999,bx,O09,48c3,3nd,49d9,4093,x0a,4t1,40K,f6P,Dy5,E09,R907,R9c7,Xa47,34k7,W06,S9d7,x46,R8c7,0e5,U097,dT1,fG40,G9j,GA5,da07,d8d0,dj5,d8B,6N5,dKc,TX5,rX5,Xx7,atX,4942,Fe4,F8ca,4961,44cR,48J7,qj5,48k5,NaL,fSp,94d9,6C5,6mc,H8e,bec,XNc,fX40,fN97,aDd,4aW,4E3,3009,S0d,49c7,fX2,48cd,f6s,aue,%H5,uz5,04p,p9X,aA6,a%6,Nk5,d407,R4L,Xm5,f0d51,fm6,24e,NZ5,X0p,dSc,eQ5,606,z8p,qd5,Ng5,OIc,fT9a,fqh,f0I7,9Ve,G9j,fT6,XP5,eH5,Gbc,f0e7,6Dc,Xak,gIc,S46,r9c7,30L,2q,Fad,20d,f0r,4Fc,9d0,O05,494a,j8d,a409,b09,98h,48l,f6V,4000,eg5,X0J,fa9X,dt9,6r5,68p,0N5,fqX,dL7,94p7,RU5,dF7,FXa,X8m,4QX,480R,WL7,Y25,QH1,H9J,Mo5,g8i,X9c9,gIa,hNa,aFk,u8T,EZ5,kea,SRa,F000,h8W,F4F,X9V,9QR,X9i,rr1,r9de,6d7,ei5,296,dK5,Sj5,2L5,X65,Nh5,d4O,99S7,TS7,fTp,aC6,r06,Sap,d00e,D06,tr5,t007,9867,dT7,ab6,2k5,xp5,FJ5,6%7,r099,pa47,HL7,rZc,RO7,9lX,e8R,FP1,OQ5,9a9m,yzd,aed5,a864,X0l,S9l,3j6,eH9,N9D,w8J,FQ5,X25,Rai,ZC5,E0i,G9V,Fnc,K4J,l8S,ei3,RVa,E8Y,N403,OD5,Fm5,ym5,Yz1,ib5,xC5,90cR,qI1,G901,r8P,B9J,QY5,4gi,apR,Fpc,F4z,69C,3Pi,BH1,da41,e09a,aEJ,E4V,js5,hCa,e0s,64d4,hH9,aX45,xl5,fB07,Mu5,X044,Ra%,SG9,fw97,mX5,E94e,Ftd,du1,U9S,Dp5,OW5,et3,r449,D0k,da41,R8k,e0d7,do5,H86,99j7,dP5,d25,Kj5,4096,6M5,4Ac7,4Ze,9Md,39H7,fkX,G0L,gL5,X997,dh9,eI5,X65,0e5,fN4a,fR09,hLc,xLc,4096,d9J,dL4,d8F,du3,d92,da9a,N097,SG5,09p,G0d7,v06,zz5,Nj5,49i5,G46,Vz5,f9051,b47,30de,4M9,30ce,994e,foc7,0sc,4Wd,frd,TG,au0,Wt,b9a,ZM,aD4,30d0,99d0,9%4,El,Z9a,aK3,aM1,a%7,3m1,q95,644,929,34de,4O9,B84,aN1,E91,O95,DL,El,4l7,D0c,ay3",

str2 = ""
