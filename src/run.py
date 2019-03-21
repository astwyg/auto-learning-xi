import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time, os

import qrcode

browser = webdriver.Chrome(os.path.join(os.path.dirname(__file__), "chromedriver.exe"))

def user_login():
    browser.get("https://pc.xuexi.cn/points/login.html?ref=https://www.xuexi.cn/")
    login_iframe = browser.find_elements_by_tag_name('iframe')[-2]
    browser.switch_to.frame(login_iframe)
    qr_element = browser.find_element_by_css_selector("#qrcode img")
    browser.execute_script("arguments[0].scrollIntoView();", qr_element)
    print("等待扫码登录")
    while True:  # FIXME 这里需要用命令行显示qr_str并扫码登录
        time.sleep(1)
        if "login" not in browser.current_url:
            print("登录成功")
            return

def read_news():
    browser.get("https://www.xuexi.cn/")
    news = browser.find_elements_by_css_selector(".word-item")
    cnt = 1
    for element in news[5:15]:  # 读5-15条新闻
        print("开始读第{}条新闻".format(cnt))
        cnt = cnt + 1
        try:
            browser.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            browser.switch_to.window(browser.window_handles[0])
            browser.switch_to.window(browser.window_handles[-1])
            for _ in range(100):
                ActionChains(browser).key_down(Keys.DOWN).perform()
                time.sleep(0.2)
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
        except selenium.common.exceptions.ElementNotVisibleException:
            pass

def watch_video():
    browser.get("https://www.xuexi.cn/")
    browser.find_element_by_link_text("学习电视台").click()

    # 关闭主标签页
    browser.switch_to.window(browser.window_handles[0])
    browser.close()
    browser.switch_to.window(browser.window_handles[0])

    # 切换到"第一频道"
    browser.find_element_by_link_text("第一频道").click()
    # 关闭主标签页
    browser.switch_to.window(browser.window_handles[0])
    browser.close()
    browser.switch_to.window(browser.window_handles[0])

    time.sleep(5) # 等待js运行完毕
    videos = browser.execute_script('return $("div.word-item")')
    video_flag = False
    cnt = 1
    for video in videos:
        video_flag = not video_flag
        if video_flag:
            print("开始看第{}条视频".format(cnt))
            cnt = cnt+1
            video.click()
            browser.execute_script("arguments[0].scrollIntoView();", browser.execute_script('''return $("div:contains('>>')")[5]'''))
            time.sleep(60)
            browser.switch_to.window(browser.window_handles[-1])  # 关闭当前标签页
            browser.close()
            browser.switch_to.window(browser.window_handles[0])


if __name__ == "__main__":
    user_login()
    read_news()
    watch_video()