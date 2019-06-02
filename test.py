from appium import webdriver
import time
from functools import reduce
from database import Douyin,Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from addons.fans import Fans
max = 105
# addons = [
#     Fans(),
# ]

engine = create_engine('sqlite:///douyin.sqlite')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

count = 0


def init_device():
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '7.0'
    desired_caps['deviceName'] = 'A02AECPB2CFMX'
    desired_caps['appPackage'] = 'com.ss.android.ugc.aweme'
    desired_caps['appActivity'] = 'com.ss.android.ugc.aweme.main.MainActivity'
    desired_caps['unicodeKeyboard'] = True
    desired_caps['resetKeyboard'] = True
    desired_caps["noReset"] = True
    desired_caps["newCommandTimeout"] = 600
    # 启动appium-desktop服务器，服务器IP根据实际填写
    device = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    return device


def move_to_fans(device, kw):
    global count
    global max
    # 点击 搜索图标
    search_icon = WebDriverWait(device, 10).until(lambda x: x.find_element_by_id("com.ss.android.ugc.aweme:id/aug"))
    search_icon.click()
    # device.find_element_by_id("com.ss.android.ugc.aweme:id/aug").click()
    # 搜索框输入高考
    device.find_element_by_id("com.ss.android.ugc.aweme:id/a8d").send_keys(kw)
    # 点击搜索
    device.find_element_by_id("com.ss.android.ugc.aweme:id/d6m").click()
    WebDriverWait(device, 10).until(lambda x: x.find_element_by_id("android:id/text1"))
    # time.sleep(3)
    # 点击用户列表
    device.find_elements_by_id("android:id/text1")[2].click()
    # time.sleep(10)

    size = get_screen_size(device)
    x1 = int(size[0] * 0.5)
    y1 = int(size[1] * 0.9)
    y2 = int(size[1] * 0.15)

    users_done = []
    while  count < max:
        # 获取所有名称中包含高考的用户
        WebDriverWait(device, 10).until(lambda x: x.find_element_by_id("com.ss.android.ugc.aweme:id/d9j"))
        users = device.find_elements_by_id("com.ss.android.ugc.aweme:id/d9j")
        all_users = [x.text for x in users]
        if reduce(lambda x, y: x and y, [(x in users_done) for x in all_users]) and users_done:
            print("遍历结束, 将会终止session")
            break
        for user in users:
            if user.text not in users_done:
                user.click()
                WebDriverWait(device, 10).until(lambda x: x.find_element_by_id("com.ss.android.ugc.aweme:id/adp"))
                # time.sleep(5)
                device.find_element_by_id("com.ss.android.ugc.aweme:id/adp").click()
                # time.sleep(2)
                fans_cycle(device)
                users_done.append(user.text)
                print(user.text)

        device.swipe(x1, y1, x1, y2, duration=1000)
        if len(users_done) > 30:
            users_done = users_done[10:]


def get_screen_size(device):
    """获取屏幕宽高度"""
    x = device.get_window_size()['width']
    y = device.get_window_size()['height']
    return x,y


def fans_cycle(device):
    global count
    global max
    size = get_screen_size(device)
    x1 = int(size[0] * 0.5)
    y1 = int(size[1] * 0.9)
    y2 = int(size[1] * 0.15)

    fans_done = []
    while count < max:
        # 获取所有的粉丝
        # time.sleep(3)
        WebDriverWait(device, 10).until(lambda x: x.find_element_by_id("com.ss.android.ugc.aweme:id/da3"))
        elements = device.find_elements_by_id("com.ss.android.ugc.aweme:id/da3")
        all_fans = [x.text for x in elements]
        if reduce(lambda x, y: x and y, [(x in fans_done) for x in all_fans]) and fans_done:
            print("遍历结束, 将会终止session")
            # 返回个人页面
            device.press_keycode("4")
            # 返回列表页面
            device.press_keycode("4")
            break
        for element in elements:
            if count > max:
                break
            if (element.text not in fans_done) and element.text != "格物水滴":
                # 检查是否已经发过了
                my_douyin = session.query(Douyin).filter(Douyin.name==element.text).all()
                if len(my_douyin)>0:
                    continue
                element.click()
                # 如果已经关注过了，则
                if len(device.find_elements_by_id("com.ss.android.ugc.aweme:id/ad_")) > 0:
                    # 返回粉丝列表页面
                    device.press_keycode("4")
                    continue
                # 点击 关注
                # time.sleep(5)
                WebDriverWait(device, 10).until(lambda x: x.find_element_by_id("com.ss.android.ugc.aweme:id/bz5"))
                device.find_element_by_id("com.ss.android.ugc.aweme:id/bz5").click()
                time.sleep(1)
                # 点击 私信
                try:
                    device.find_element_by_id("com.ss.android.ugc.aweme:id/ce_").click()
                except Exception as e:
                    # device.press_keycode("4")
                    print(e)
                    # 返回粉丝列表页面
                    device.press_keycode("4")
                    continue

                # time.sleep(2)
                WebDriverWait(device, 10).until(lambda x: x.find_element_by_id("com.ss.android.ugc.aweme:id/bgo"))
                # 点击编辑消息
                device.find_element_by_id("com.ss.android.ugc.aweme:id/bgo").send_keys('高考志愿模拟填报选格物水滴APP,报名同时查看录取结果，与所有报名者沟通交流')
                # 点击发送
                device.find_element_by_id("com.ss.android.ugc.aweme:id/cdz").click()
                time.sleep(1)
                # 退出键盘
                device.press_keycode("4")
                time.sleep(1)
                # 返回个人页面
                device.press_keycode("4")
                time.sleep(1)
                # 返回粉丝列表页面
                device.press_keycode("4")
                time.sleep(1)
                print(element.text)
                fans_done.append(element.text)
                user = Douyin(name=element.text, hassend=True)
                count += 1
                session.add(user)
                session.commit()

        device.swipe(x1, y1, x1, y2, duration=1000)

        if len(fans_done) > 30:
            fans_done = fans_done[10:]


if __name__ == '__main__':
    # while True:
    dev = init_device()
    try:
        move_to_fans(dev, "高考")
    except Exception as e:
        print(e)
        dev.quit()
