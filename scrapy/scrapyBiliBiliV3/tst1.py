#!/usr/bin/python3

import sqlCon, multiprocessing, requests,ssl


def setRequest():
    headers = {'Accept':'application/vnd.github.v3+json'}
    r = requests.get('https://api.github.com/user',auth = ('mhb_208@outlook.com','mhb12121992'),headers=headers,proxies={}, allow_redirects=False)
    print(r.content.decode('utf-8'))

def main():
    try:
        conn, cur = sqlCon.mysqlConn()
    except Exception as  e:
        print('Fail to connect to mysql! error occurs as %s'%(e.__str__(),))
        exit()

    setRequest()

# requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context  # 关闭ssl证书验证
if __name__ == '__main__':
    main()
