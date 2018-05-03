from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


def login():
    # 手动登录获取cookies
    driver = webdriver.Chrome( r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    driver.get("https://pan.baidu.com/")
    driver.implicitly_wait(5)  # 如果不等待，下面的语句会出现找不到元素的错误
    login = driver.find_element_by_id("TANGRAM__PSP_4__footerULoginBtn")
    print(login.get_attribute("innerHTML"))
    login.click()
    username = "********"
    password = "********"
    driver.find_element_by_css_selector("#TANGRAM__PSP_4__userName").clear()
    driver.find_element_by_css_selector("#TANGRAM__PSP_4__userName").send_keys(username)
    driver.find_element_by_css_selector("#TANGRAM__PSP_4__password").send_keys(password)
    driver.find_element_by_css_selector("#TANGRAM__PSP_4__submit").click()
    time.sleep(10)  # 留充足的时间手动输入验证码
    try:  # 查找登录按钮，如果找不到，抛出异常
        driver.find_element_by_css_selector("#TANGRAM__PSP_4__submit").click()
    except NoSuchElementException as msg:
        print(msg)
    time.sleep(5)
    cookies = driver.get_cookies()
    print(cookies)
    print(driver.title)
    title = driver.title  # 返回的title为unicode类型，下面比较时应该也应与unicode类型比较
    user = driver.find_element_by_class_name("user-name")
    username = user.get_attribute("innerHTML")
    # 下面的代码是自己测试是否登录成功的
    try:
        if title == u'百度网盘-全部文件' and username == u'*****':  # u定义了一个unicode类型
            print("登录成功")
        else:
            raise AssertionError("登录失败")
    except AssertionError as  msg:
        print(msg)


if __name__ == "__main__":
    login()
