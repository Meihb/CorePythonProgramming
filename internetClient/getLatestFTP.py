#/usr/local/bin/python3

import ftplib,os,socket

HOST = 'ftp.mozilla.org'
DIRN='pub/mozilla.org/webtools'
FILE = 'bugzilla-LATEST.tar.gz'

def main():
    try:
        f = ftplib.FTP(HOST)
    except(socket.error,socket.gaierror) as e:
        print('ERROR:cannot reach %s'%(HOST))
        return
    print('''Connected to host %s'''%(HOST))

    try:
        f.login()
    except ftplib.error_perm:
        print('ERROR:cannot login anonymously')
        f.quit()
        return
    print('Logged as anonymous successfully')

    try:
        f.cwd(DIRN)
    except ftplib.error_perm:
        print('ERROR:cannot  cd to %s'%DIRN)
        f.quit()
        return
    print('CD to %s '%DIRN)

    try:
        f.retrbinary('RETR %s '%FILE,open(FILE,'wb').write)
    except ftplib.error_perm:
        print('ERROR:cannot  retr  %s'%FILE)
        os.unlink(FILE)
    else:
        print('retr %s'%FILE)
        f.quit()

if __name__=='__main__':
    main()

