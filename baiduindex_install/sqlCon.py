import pymysql
import conf


def mysqlConn():
    host = conf.host
    port = conf.port
    user = conf.user
    pwd = conf.pwd
    # 创建连接
    conn = pymysql.connect(host=host, user=user, passwd=pwd, port=port, charset='utf8mb4', db='dwts')
    # 建立游标
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 业务表初始化
    cur.execute('''
    CREATE TABLE IF NOT EXISTS  `baidu_index_words` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(128) CHARACTER SET utf8 NOT NULL,
  `flag` int(11) NOT NULL DEFAULT '0',
  `start` date DEFAULT NULL COMMENT '起始日期不小于2006-06-01',
  `end` date DEFAULT NULL COMMENT '结束日期不大于昨日',
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS  `baidu_index` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recognitions` int(11) DEFAULT NULL,
  `process_status` int(11) NOT NULL DEFAULT '0' COMMENT '0未处理,-1processing,1commit',
  `word` varchar(128) NOT NULL,
  `refer_date_begin` date DEFAULT NULL,
  `time` datetime NOT NULL,
  `refer_date_end` date DEFAULT NULL,
  `width` varchar(256) CHARACTER SET utf8mb4 NOT NULL,
  `margin_left` varchar(256) CHARACTER SET utf8mb4 NOT NULL,
  `img_url` text CHARACTER SET utf8mb4 NOT NULL,
  `dir` varchar(256) CHARACTER SET utf8mb4 DEFAULT NULL,
  `location` varchar(256) CHARACTER SET utf8mb4 NOT NULL,
  `resolved_location` varchar(256) CHARACTER SET utf8mb4 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `recognitions` (`recognitions`),
  KEY `process_status` (`process_status`),
  KEY `word` (`word`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
    ''')

    # 初始化table
    return conn, cur


if __name__ == '__main__':
    conn, cur = mysqlConn()
    try:
        conn.ping()
    except:
        conn.ping(True)
