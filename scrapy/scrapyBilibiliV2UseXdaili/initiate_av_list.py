import os
import pymysql

target_root = os.path.expanduser('~') + '/哔哩哔哩AV号.txt'

conn = pymysql.connect(host='122.112.248.56', user='dwts', passwd='12121992', port=3306, charset='utf8mb4')
conn.select_db('dwts')

with open(target_root, 'r') as f:
    for line in f.readlines():
        conn.cursor().execute("INSERT INTO bilibili_av_list  SET avid = %s",[int(line)])
    conn.commit()

print('Success')