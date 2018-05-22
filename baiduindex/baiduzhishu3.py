# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 23:31:10 2017

@author: Administrator
"""
from selenium import webdriver
from PIL import Image
import requests
import time
import re
import urllib
import pytesseract
import traceback 


save_path = 'D:\\download\\baiduzhishu'


keys=input('关键词:')
word=keys.encode('utf8')
word=urllib.parse.quote(word)
keys=keys.encode('gb2312')
keys=urllib.parse.quote(keys)


driver = webdriver.Chrome('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe')
url = 'http://index.baidu.com/?tpl=trend&word=%s'%keys
driver.get(url)
e1 = driver.find_element_by_id("TANGRAM__PSP_4__userName")
e1.send_keys("13851020274")
e2 = driver.find_element_by_id("TANGRAM__PSP_4__password")
e2.send_keys("mhb12121992")
time.sleep(2)
e3 = driver.find_element_by_id("TANGRAM__PSP_4__submit")
e3.click()
#driver.find_element_by_xpath('//a[@rel="%s"]' %'180').click()
time.sleep(5)

new_cookies=''
cookies = driver.get_cookies()
print(cookies)
for cookie in cookies:
    name=(cookie['name'])
    value=(cookie['value'])
    new_cookie=name+'='+ value+';'
    new_cookies=new_cookies + new_cookie
new_cookies=new_cookies[:-1]
print(new_cookies)
exit()
res = driver.execute_script('return PPval.ppt;')
res2 = driver.execute_script('return PPval.res2;')
startdate='2017-12-01'
enddate='2017-12-30'

header={
        'Host': 'index.baidu.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
        'Referer': 'http://index.baidu.com/?tpl=trend&word=%CE%A4%B5%C2',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': new_cookies

        }

url='http://index.baidu.com/Interface/Search/getSubIndex/?res={}&res2={}&type=0&startdate={}&enddate={}&forecast=0&word={}'.format(res,res2,startdate,enddate,word)
req=requests.get(url,headers=header).json()

print(req)
res3_list = req['data']['all'][0]['userIndexes_enc']
res3_list = res3_list.split(',')
print(len(res3_list))

m=0
range_dict=[]
for res3 in res3_list:
    #print(res3)
    timestamp=int(time.time())
    viewbox_url='http://index.baidu.com/Interface/IndexShow/show/?res=%s&res2=%s&classType=1&res3[]=%s&className=view-value&%s'%(res,res2,res3,timestamp)
    try:
        req=requests.get(viewbox_url,headers=header).json()
        print('请求成功')
        response=req['data']['code'][0]       
        width = re.findall('width:(.*?)px',response)
        margin_left = re.findall('margin-left:-(.*?)px',response)
        width = [ int(x) for x in width ]
        margin_left= [ int(x) for x in margin_left ]
        # print(width,margin_left)
        range_dict.append({'width':width,'margin_left':margin_left})
        img_url ='http://index.baidu.com' + re.findall('url\("(.*?)"',response)[0]
        # print(img_url)
        img_content = requests.get(img_url,headers=header)
        time.sleep(1.5) 
        if img_content.status_code == requests.codes.ok:
            with open('%s\\%s.png'%(save_path,m), 'wb') as file:
                file.write(img_content.content)
                print('下载成功')
        m+=1
    except:
        traceback.print_exc()



        
print(len(range_dict))

n=0
j=0   
#region=range_dict[76]
for region in range_dict:
    #print(region)
    try:
        code = Image.open('%s\\%s.png'%(save_path,n))
        hight = code.size[1]
        target = Image.new('RGB', (sum(region['width']), hight)) 
        for i in range(len(region['width'])):
            #print(i)
            img=code.crop((region['margin_left'][i],0,region['margin_left'][i]+region['width'][i],hight)) 
            # img.show()
            target.paste(img, (sum(region['width'][0:i]), 0, sum(region['width'][0:i+1]), hight))   
            target.save('%s\\Puzzle%s.png'%(save_path,j))
        n+=1
        j+=1
        print('拼接成功')

    except:
        traceback.print_exc()
        n+=1

print(j)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'D:\software\dev\Tesseract-OCR\tesseract.exe'
index = []
for k in range(j):
        jpgzoom = Image.open("%s/Puzzle%s.png" %(save_path,k))
        (x, y) = jpgzoom.size
        x_s = 2*x
        y_s = 2*y
        out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
        out.save('%s/zoom%s.jpg' %(save_path,k), quality=95)
        num = pytesseract.image_to_string(out)
        if num:
            num=num.replace("'",'').replace('.','').replace(',','').replace('?','7').replace("S", '5').replace(" ", "").replace("E", "8").replace("B", "8").replace("I", "1").replace("$", "8")
            index.append(num)
        else:
            num=''
            index.append(num)

with open ('%s/index.txt'%save_path,'w') as f:
    for item in index:
        f.write(item + '\n')
        
