#!/usr/bin/python3

import sqlCon,time

conn,cur = sqlCon.mysqlConn()

cur.execute('SELECT  *  FROM bilibili_av_list WHERE pro_flag = 0 LIMIT 1 FOR  UPDATE ')
conn.commit()
print(cur.fetchall())

time.sleep(12)

print('Success')