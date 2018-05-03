#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time

chromeDriver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'  # chromedriver路径


def logIn():
    browser = webdriver.Chrome(chromeDriver)
    browser.get('http://index.baidu.com/?tpl=trend')  # 接下来需等待chrome启动和页面加载,如果不等待，下面的语句会出现找不到元素的错误
    # time.sleep(5)#强制等待,最简单的等待方法,强制等待,浪费资源,且不知何时才能正确执行,则命中率低
    # browser.implicitly_wait(10)#隐性等待,设置最长等待时间,若页面所有资源在时间内完成加载,则停止等待,较高的时间利用率,但是是否需要页面全部加载的问题浮现
    try:  # 显性等待,通过until/until_not 实现自定义的目标
        WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located((By.ID,'TANGRAM_12__userName')))
        print('here')
        # WebDriverWait(browser, 10, 0.5).until(lambda driver: driver.find_element_by_class_name('lb'))
        browser.find_element_by_id('TANGRAM_12__userName').clear()
        browser.find_element_by_id('TANGRAM_12__userName').send_keys('13851020274')
        browser.find_element_by_id('TANGRAM_12__password').clear()
        browser.find_element_by_id('TANGRAM_12__password').send_keys('mhb12121992')

        browser.find_element_by_id('TANGRAM_12__submit').submit()#确认登录

        cookies = browser.get_cookies()
        print(cookies)


        time.sleep(15)
    except  NoSuchElementException as e:
        print('111' + e.msg)
        exit()
    except StaleElementReferenceException as e:
        print('222' + e.msg)
        exit()
    except TimeoutException as e:
        print('333' + e.msg)
        exit()


if __name__ == '__main__':
    logIn()
