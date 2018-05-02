#!/usr/bin/python3

import sqlCon


conn,cur = sqlCon.mysqlConn()

cur.execute('''UPDATE   bilibili_av_list SET avid = '2222' WHERE id=1 ''')
# cur.execute('SELECT *  FROM bilibili_av_list WHERE pro_flag = 0 LIMIT 1 ')
conn.commit()
print(cur.fetchall())