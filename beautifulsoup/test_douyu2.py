

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import  time


chromeDriver = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'

def start_chrome():
    url = 'https://v.douyu.com/show/Qyz171wZyK1WBJj9'
    browser = webdriver.Chrome(chromeDriver)
    browser.get(url)
    try:  # 显性等待,通过until/until_not 实现自定义的目标
        browser.implicitly_wait(2)

        time.sleep(25)#修改此处或使用webdriverwait
        result = browser.execute_script('''return $('.nums')[0].textContent''')
        print('result is '+ result,type(result))
        return result
    except  NoSuchElementException as e:
        print('NoSuchElementException' + e.msg)
        exit()
    except StaleElementReferenceException as e:
        print('StaleElementReferenceException' + e.msg)
        exit()
    except TimeoutException as e:
        print('TimeoutException' + e.msg)
        exit()

if __name__=='__main__':
    start_chrome()