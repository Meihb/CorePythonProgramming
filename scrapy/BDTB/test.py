#!/usr/bin/python3

import requests, time, re, smtpd, traceback
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


class myBDTB:
    def __init__(self, url, keywords):
        self.error = ""
        self.url = url
        self.keywords = keywords
        self.frequencyData = {}

    def get_title(self, content):
        pattern = re.compile(r'<div class="col2_right j_threadlist_li_right ">(.*?)</div>', re.S)
        items = re.findall(pattern, content)

    def start(self):
        try:
            r = requests.get(self.url)
            soup = BeautifulSoup(r.content.decode('utf-8'), 'html5lib')
            for item in soup.find_all("div", {'class': 'col2_right j_threadlist_li_right '}):
                self.analyzeStructure(item)


        except Exception as e:
            print(traceback.print_exc())
            print(e)

    def analyzeStructure(self, itemContent):
        # print(itemContent)
        href = itemContent.div.div.a['href']
        title = itemContent.div.div.a['title']
        summary = itemContent.find("div", {'class': 'threadlist_abs threadlist_abs_onlyline '})
        if summary:
            summary = summary.get_text()
        print('here lies the info ', href, title, summary, "---------------------")

        if title:
            self.checkKeyWord(title, href, 'title')
        if summary:
            self.checkKeyWord(summary, href, 'summary')

        # print(self.error)

    def checkKeyWord(self, result, href, tag='title'):
        for keyword in self.keywords:
            print(tag + '查找关键字' + keyword)
            if result.find(keyword) >= 0:
                print('YES' + '于' + result)
                if self.mailFrequency(href):
                    errormsg = "find  keyword [" + keyword + '] in  ' + tag + '[' + result + ' ] ,href is https://tieba.baidu.com' + href
                    self.mailWarning('1253880904@qq.com', 'iqjnzsydcofpibif', '1253880904@qq.com', errormsg, href)
                else:
                    print('太过频繁,取消发送')

    def mailWarning(self, sender, authcode, receiver, errormsg, href):
        print('errormsg is ' + errormsg)
        ret = True
        try:
            msg = MIMEText(errormsg, 'plain', 'utf-8')
            msg['From'] = formataddr(["发件人昵称", sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["收件人昵称", receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "邮件主题-贴吧关键字提示"  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
            server.login(sender, authcode)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(sender, [receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print(traceback.print_exc())
            ret = False

        if ret:
            self.frequencyData[href] = time.time()
            print('发送成功')
        return ret

    def mailFrequency(self, href):

        '''
        对于同一个href发送频率 为1h
        '''
        print(self.frequencyData)

        if not href in self.frequencyData:
            last_time = 0
        else:
            last_time = self.frequencyData[href]
        print('last time for ' + href + ' is ' + last_time.__str__())
        if int(time.time()) - int(last_time) > 3600:
            return True
        else:
            return False


obj = myBDTB(url='https://tieba.baidu.com/f?kw=ff14&fr=ala0&tpl=5', keywords=['报警', '奸商'])

try:
    obj.start()
    print(' End@' + time.strftime("%Y-%m-%d %H %M %S", time.localtime()))
except Exception as e:
    print(traceback.print_exc())
    print(e.__str__())

# while True:
#
#     try:
#         obj.start()
#         print(' End@' + time.strftime("%Y-%m-%d %H %M %S", time.localtime()))
#     except Exception as e:
#         print(traceback.print_exc())
#         print(e.__str__())
#
#     time.sleep(60)
