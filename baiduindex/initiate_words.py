#!/usr/bin/python3
# coding=gbk
import pymysql


def mysqlConn():
    host = '118.25.41.135'
    port = 3306
    user = 'dwts'
    pwd = 'dwts'
    # ��������
    conn = pymysql.connect(host=host, user=user, passwd=pwd, port=port, charset='utf8mb4',db='dwts')

    # �����α�,�޸�Ĭ��Ԫ������Ϊ�ֵ�����
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn,cur

if  __name__=='__main__':
    words = [ 'LOVE LIVE', '�����س�֮��','����Ů��֮��','������','������������','�����һ�','����MM', '������ʿ��','����������','����֮��','��ɢ�԰�����ɪ��','��֮��','��֮�ȴ�½̽��','��֮����Դ','��֮ս��', 'ħ��HD','ħ���ռ�','ħ��������','ƴս����־','����֮��','��Ѫ�����ֻ���', 'ɳ�Ϳ˴���','������','�ػ��ߴ�˵','����ս��', 'Ѫ��','Ӷ������','�������','��������','�ݺ���������','����Ѫͳ2','�����ٻ�', '����֮ʫ',
    ]
    conn, cur = mysqlConn()
    for word in words:
        cur.execute('INSERT INTO `baidu_index_words` (word) VALUES (%s)',[word.encode('utf-8')])
    conn.commit()
    print('Success')
