#!/usr/bin/python3

import requests, time, re,smtpd
from bs4 import BeautifulSoup


class myBDTB:
    def __init__(self, url, keywords):
        self.error = ""
        self.url = url
        self.keywords = keywords

    def get_title(self, content):
        pattern = re.compile(r'<div class="col2_right j_threadlist_li_right ">(.*?)</div>', re.S)
        items = re.findall(pattern, content)

    def start(self):
        try:
            r = requests.get(self.url)
            soup = BeautifulSoup(r.content.decode('utf-8'), 'html5lib')
            i = 0
            for item in soup.find_all("div", {'class': 'col2_right j_threadlist_li_right '}):
                self.analyzeStructure(item)


        except Exception as e:
            print(e)

    def analyzeStructure(self, itemContent):
        href = itemContent.div.div.a['href']
        title = itemContent.div.div.a['title']

        if title:
            self.checkKeyWord(title, href)
        summary = itemContent.find("div", {'class': 'threadlist_abs threadlist_abs_onlyline '})
        if summary:
            summary = summary.get_text()
            self.checkKeyWord(summary,href,'summary')

        print(href, title,summary,"---------------------")
        print(self.error)

    def checkKeyWord(self, result, href, tag='title'):
        for keyword in self.keywords:
            if result.find(keyword) >= 0:
                self.error = "find  keyword [" + keyword + '] in  ' + tag + '[' + result + ' ] ,href is https://tieba.baidu.com' + href
                self.mailWarning('1253880904@qq.com','iqjnzsydcofpibif','1253880904@qq.com')
                return False

    def mailWarning(self,sender,authcode,receiver):
        import smtplib
        from email.mime.text import MIMEText
        from email.utils import formataddr
        ret = True
        try:
            msg = MIMEText(self.error, 'plain', 'utf-8')
            msg['From'] = formataddr(["发件人昵称", sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["收件人昵称", receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "邮件主题-贴吧关键字提示"  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
            server.login(sender, authcode)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(sender, [receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
        return ret



obj = myBDTB(url='https://tieba.baidu.com/f?kw=ff14&fr=ala0&tpl=5', keywords=['垃圾', '报警'])

while True:

    try:
        obj.start()
        print(' End@' +time.strftime("%Y-%m-%d %H %M %S",time.localtime()))
    except Exception as e:
        print(e.__str__())

    time.sleep(60)
