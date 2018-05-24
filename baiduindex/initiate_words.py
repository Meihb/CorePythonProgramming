#!/usr/bin/python3
# coding=gbk
import pymysql


def mysqlConn():
    host = '118.25.41.135'
    port = 3306
    user = 'dwts'
    pwd = 'dwts'
    # 创建连接
    conn = pymysql.connect(host=host, user=user, passwd=pwd, port=port, charset='utf8mb4',db='dwts')

    # 建立游标,修改默认元组数据为字典类型
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn,cur

if  __name__=='__main__':
    words = [ 'LOVE LIVE', '超级地城之光','超级女神之光','城与龙','传奇世界手游','传世挂机','封神MM', '钢铁骑士团','鬼吹灯昆仑神宫','混沌之理','扩散性百万亚瑟王','龙之谷','龙之谷大陆探险','龙之谷起源','龙之战记', '魔界HD','魔王日记','魔物狩猎者','拼战三国志','破晓之光','热血传奇手机版', '沙巴克传奇','神无月','守护者传说','锁链战记', '血族','佣兵传奇','永恒幻想','勇者世界','纵横天下手游','暗黑血统2','神域召唤', '境界之诗',
    ]
    conn, cur = mysqlConn()
    for word in words:
        cur.execute('INSERT INTO `baidu_index_words` (word) VALUES (%s)',[word.encode('utf-8')])
    conn.commit()
    print('Success')
