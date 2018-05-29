import pymysql


def mysqlConn():
    host = '118.25.41.135'
    port = 3306
    user = 'dwts'
    pwd = 'dwts'
    # 创建连接
    conn = pymysql.connect(host=host, user=user, passwd=pwd, port=port, charset='utf8mb4',db='dwts')
    # 建立游标
    cur = conn.cursor(cursor = pymysql.cursors.DictCursor)
    # 执行sql,返回影响行数
    # effect_rows = cur.execute('SELECT * FROM  bilibili_av_list  WHERE  1')
    #获取全部返回值
    # result = cur.fetchall()
    #执行sql,返回影响行数和执行次数
    # effect_many_rows = cur.executemany(
    #     "INSERT INTO bilibili_av_list (id,avid,pro_flag,proc_date_time) VALUES (%s,%s,%s,%s)",
    #     [(0,'2132001','0',None),(0,'22212121','0',None)])
    #参数化
    # test_insert = cur.execute('Insert into bilibili_av_list(id,avid) VALUES (%s,%s)',[0,'2121'])

    return conn,cur
    # cur.close()
    # conn.commit()
    # conn.close()




if __name__ == '__main__':
    mysqlConn()
