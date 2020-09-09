import time
import random

from selenium import webdriver
from PIL import Image
from selenium.webdriver import ActionChains

from UI_tianyancha_zhuce import Ui_ZhuceWindow
from tianyancha_process import ProcessWindow

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QDesktopWidget


# 注册页面
class Tianyancha_ZhuceWindow(QMainWindow, Ui_ZhuceWindow):

    def __init__(self, company_list, company_name_sum, generate_name, generate_data, url):
        super(Tianyancha_ZhuceWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.count = 50
        self.time = QTimer(self)
        self.time.setInterval(1000)

        self.url = url
        self.driver = webdriver.Chrome()

        self.control_init()

        self.generate_name = generate_name
        self.generate_data = generate_data
        self.company_list = company_list
        self.company_name_sum = company_name_sum

        self.auto_Bracket = None

    # 页面组件设置
    def control_init(self):
        screen = QDesktopWidget().screenGeometry()
        self.move(0, screen.height() * 0.3)

        self.tel_line.textChanged.connect(self.check_get_func)
        self.verification_line.textChanged.connect(self.check_input_func)

        self.auto_verification.toggled.connect(self.tuokuai_verification)
        self.manual_verification.toggled.connect(self.tuokuai_verification)

        self.zc_active_button.setEnabled(False)
        self.get_verification_button.setEnabled(False)
        self.verification_line.setVisible(False)
        self.verification_label.setVisible(False)

        self.get_verification_button.clicked.connect(self.check_get_button)
        self.zc_active_button.clicked.connect(self.check_active_button)

        self.zc_active_button.clicked.connect(self.check_active_button)
        self.zc_active_button.clicked.connect(self.closewin)

        self.time.timeout.connect(self.Refresh)

    # 获取验证码按钮设置
    def check_get_func(self):
        if self.tel_line.text():
            self.get_verification_button.setEnabled(True)
        else:
            self.get_verification_button.setEnabled(False)

    # 获得验证码按钮
    def check_get_button(self):
        self.get_verification_button.setEnabled(False)
        telephone = self.tel_line.text()
        self.driver.get(self.url)
        script = 'Object.defineProperty(navigator,"webdriver",{get:() => false,});'
        self.driver.execute_script(script)
        self.driver.maximize_window()
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[1]/div/div[2]/div/div[5]/a').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[1]/div[1]').click()
        time.sleep(0.5)
        try:
            input_tel = self.driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[3]/div[1]/div[1]/input')
            time.sleep(1)
            for j in telephone:
                input_tel.send_keys(j)
                time.sleep(random.uniform(0.2, 0.5))
        except:
            input_tel = self.driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[3]/div[1]/div[1]/input')
            time.sleep(1)
            for k in input_tel:
                input_tel.send_keys(k)
                time.sleep(random.uniform(0.2, 0.5))
        try:
            self.driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[3]/div[2]/div[1]').click()
        except:
            self.driver.find_element_by_xpath('/html/body/div[10]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[3]/div[2]/div[1]').click()
        self.toukuai_choose_run()
        try:
            self.driver.find_element_by_class_name('input-group-btn.-disabled')
            self.time.start()
            self.verification_label.setVisible(True)
            self.verification_line.setVisible(True)
        except:
            self.close()

    # 完整背景图
    def before_deal_image(self):
        time.sleep(1)
        self.location = self.driver.find_element_by_class_name('gt_box_holder').location
        self.size = self.driver.find_element_by_class_name('gt_box_holder').size
        time.sleep(1)
        self.driver.save_screenshot('capture1.png')
        self.left = self.location['x']
        self.top = self.location['y']
        self.right = self.location['x'] + self.size['width']
        self.bottom = self.location['y'] + self.size['height']
        self.im = Image.open('capture1.png')
        self.im = self.im.crop((self.left, self.top, self.right, self.bottom))
        self.im.save('ele_capture1.png')
        print("完整背景截取成功------")

    # 缺口背景图
    def after_deal_image(self):
        time.sleep(1)
        slider = self.driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[2]/div[2]/div[2]')
        ActionChains(self.driver).click_and_hold(slider).perform()
        ActionChains(self.driver).move_by_offset(xoffset=198, yoffset=0).perform()
        time.sleep(1)
        self.driver.save_screenshot('capture2.png')
        ActionChains(self.driver).release().perform()
        time.sleep(1)
        self.left = self.location['x']
        self.top = self.location['y']
        self.right = self.location['x'] + self.size['width']
        self.bottom = self.location['y'] + self.size['height']

        self.im = Image.open('capture2.png')
        self.im = self.im.crop((self.left, self.top, self.right, self.bottom))
        self.im.save('ele_capture2.png')
        print("缺口背景截取成功------")
        time.sleep(1)

    # 获得滑动距离
    def slide_distance(self, image1, image2):
        cut_image = Image.open(image2)
        full_image = Image.open(image1)
        threshold = 85
        for i in range(cut_image.size[0]):
            for j in range(cut_image.size[1]):
                pixel1 = cut_image.load()[i, j]
                pixel2 = full_image.load()[i, j]
                res_R = abs(pixel1[0] - pixel2[0])
                res_G = abs(pixel1[1] - pixel2[1])
                res_B = abs(pixel1[2] - pixel2[2])
                if res_R >= threshold and res_G >= threshold and res_B >= threshold:
                    print("缺口相对所截取图片位置", i)
                    num = i - 7 - 14 - 2 - 2
                    num = int(num)
                    return num

    # 拖动托块
    def get_track_move(self, distance):
        track = []
        current = 0
        mid = distance * 3 / 4
        t = random.uniform(0.5, 0.8)
        v = 0
        while current <= distance:
            if current <= mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        slider = self.driver.find_element_by_class_name("gt_slider_knob.gt_show")
        ActionChains(self.driver).click_and_hold(slider).perform()
        time.sleep(0.5)
        track += [5, -7, 3, -1]
        print('移动轨迹：', track)
        # time.sleep(0.5)
        for i in track:
            ActionChains(self.driver).move_by_offset(xoffset=i, yoffset=0).perform()
            a = random.uniform(0.1, 0.8)
            time.sleep(a)
        ActionChains(self.driver).release(slider).perform()

    # 循环尝试拖块部分
    def for_tuokuai(self):
        print('开始重试。。。')
        for i in range(5):
            try:
                time.sleep(1)
                self.driver.find_element_by_class_name('gt_refresh_button').click()
                time.sleep(1)
                self.driver.find_element_by_class_name('gt_popup_cross').click()
                time.sleep(0.5)
                self.driver.find_element_by_xpath(
                    '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[3]/div[2]/div[1]').click()
                time.sleep(1)
                self.before_deal_image()
                time.sleep(1)
                self.after_deal_image()
                time.sleep(1)
                self.track = self.slide_distance('ele_capture1.png', 'ele_capture2.png')
                print('按钮移动距离：', self.track)
                self.get_track_move(self.track)
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[3]/div[4]')
                self.j += 1
                return self.track
            except:
                pass
            if self.j > 0:
                break
        self.driver.close()
        self.error_func()

    # 验证码刷新
    def Refresh(self):
        self.time.start()
        if self.count >= 0:
            self.get_verification_button.setText(str(self.count) + '秒')
            self.count -= 1
        else:
            self.time.stop()
            self.get_verification_button.setEnabled(True)
            self.get_verification_button.setText('重新获取验证码')
            self.count = 60

    # 输入框设置
    def check_input_func(self):
        if self.verification_line.text():
            self.zc_active_button.setEnabled(True)
        else:
            self.zc_active_button.setEnabled(False)

    # 托块验证设置
    def tuokuai_verification(self):
        radiobutton = self.sender()
        if radiobutton.isChecked():
            if radiobutton == self.auto_verification:
                self.auto_Bracket = True
            else:
                self.auto_Bracket = False
        else:
            if radiobutton == self.auto_verification:
                self.auto_Bracket = True
            else:
                self.auto_Bracket = False

    # 对托块验证的选择运行
    def toukuai_choose_run(self):
        if self.auto_Bracket == True:
            self.before_deal_image()
            self.after_deal_image()
            time.sleep(1)
            self.track = self.slide_distance('ele_capture1.png', 'ele_capture2.png')
            print('按钮移动距离：', self.track)
            self.get_track_move(self.track)
            try:
                self.driver.find_element_by_class_name('home-main-search')
                print('登录成功！')
                return self.track
            except:
                print('拖块存在问题，正在重试...')
                self.for_tuokuai()
        else:
            time.sleep(10)
            try:
                self.driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[3]/div[4]')
            except:
                self.driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[2]/div[2]/div[2]')
                reply = QMessageBox.question(self, '提示', '请手动进行托块验证！',
                                             QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.driver.implicitly_wait(10)
                self.driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[3]/div[4]')

    # 注册按钮操作
    def check_active_button(self):
        verification = self.verification_line.text()
        input_verification = self.driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[3]/div[2]/input')
        time.sleep(1)
        for i in verification:
            input_verification.send_keys(i)
            time.sleep(random.uniform(0.2, 0.5))
        try:
            self.driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[3]/div[4]').click()
            self.Ui_processwindow = ProcessWindow(self.company_list, self.company_name_sum, self.driver, self.generate_name, self.generate_data, self.url)
            self.Ui_processwindow.show()
        except:
            self.close()

    def closewin(self):
        self.close()