#!/usr/bin/python3
import  requests
from bs4 import  BeautifulSoup
import  re

url = 'https://v.douyu.com/show/Qyz171wZyK1WBJj9'
strhtml = requests.get(url)  # 所有在源码中的数据请求方式都是get
soup = BeautifulSoup(strhtml.text, 'html5lib') # lxml解析器进行解析，解析之后的文档保存到变量soup
# d1 = soup.find_all(id = 'J-collect')
# print(d1)
d2 = soup.select('div .nums')
# print(d2)
for item in d2:
    print(item)
# 使用soup.select引用这个路径
# data = soup.select('#J-collect > div.nums')
# print(data)
# 清洗和组织数据，完成上面的步骤只是获得了一段目标HTML代码，但没有把数据提取出来
# for item in data:                    # soup匹配到的有多个数据，用for循环取出
#     result = {
#         'title': item.get_text(),     # 标签在<a>标签中，提取标签的正文用get_text()方法
#         'link': item.get('href'),  # 链接在<a>标签的href中，提取标签中的href属性用get()方法，括号指定属性数据
#         'ID': re.findall('\d+', item.get('href'))    # 每一篇文章的链接都有一个数字ID。可以用正则表达式提取这个ID;\d  匹配数字； + 匹配前一个字符1次或者多次
#     }
#     print(result)
