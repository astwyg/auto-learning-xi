import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time

import qrcode

browser = webdriver.Chrome()

def user_login():
    browser.get("https://pc.xuexi.cn/points/login.html?ref=https://www.xuexi.cn/")
    login_iframe = browser.find_elements_by_tag_name('iframe')[-2]
    browser.switch_to.frame(login_iframe)
    qr_str = browser.find_element_by_css_selector("#qrcode img").get_attribute("src")
    # FIXME 这里需要用命令行显示qr_str并扫码登录

def read_news():
    browser.get("https://www.xuexi.cn/")
    news = browser.find_elements_by_css_selector(".word-item")
    for element in news:
        try:
            browser.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            browser.switch_to.window(browser.window_handles[0])
            browser.switch_to.window(browser.window_handles[-1])
            for _ in range(20):
                ActionChains(browser).key_down(Keys.DOWN).perform()
                time.sleep(0.2)
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
        except selenium.common.exceptions.ElementNotVisibleException:
            pass

if __name__ == "__main__":
    # user_login()
    read_news()