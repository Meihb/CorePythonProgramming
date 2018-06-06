

[toc]

# BaiduIndex scrap

### 配置介绍
- conf文件,填写百度账号、tesseract-OCR地址、chromedriver地址(可以使用本文件夹下chromedriver.exe)mysql连接方法
- 将主目录下的num.traineddata 复制到tesseract-OCR文件目录下tessdata文件夹内

### 数据库准备
- table baidu_index_words 关键字表
 ```mysql
CREATE TABLE IF NOT EXISTS  `baidu_index_words` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(128) CHARACTER SET utf8 NOT NULL,
  `flag` int(11) NOT NULL DEFAULT '0',
  `start` date DEFAULT NULL COMMENT '起始日期不小于2006-06-01',
  `end` date DEFAULT NULL COMMENT '结束日期不大于昨日',
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
```
- table  baidu_index 记录表
```mysql
CREATE TABLE `baidu_index` (
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```
### python3 第三方库
- PIL、requests、selenium、pytesseract