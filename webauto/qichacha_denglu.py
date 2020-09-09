import random
import time
from selenium import webdriver
from selenium.webdriver import ActionChains

from UI_qichacha_denglu import Ui_DengluWindow
from qichacha_process import ProcessWindow

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDesktopWidget


# 登录页面
class Qichacha_DengluWindow(QMainWindow, Ui_DengluWindow):

    def __init__(self, company_list, company_name_sum, generate_name, generate_data, url):
        super(Qichacha_DengluWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.driver = webdriver.Chrome()
        self.track = 308

        self.url = url
        self.generate_name = generate_name
        self.generate_data = generate_data
        self.company_list = company_list
        self.company_name_sum = company_name_sum

        self.control_init()
        self.auto_Bracket = None

    # 页面组件设置
    def control_init(self):
        screen = QDesktopWidget().screenGeometry()
        self.move(0, screen.height() * 0.3)

        self.username_line.textChanged.connect(self.check_input_func)
        self.password_line.textChanged.connect(self.check_input_func)

        self.auto_verification.toggled.connect(self.tuokuai_verification)
        self.manual_verification.toggled.connect(self.tuokuai_verification)

        self.dl_active_button.setEnabled(False)
        self.dl_active_button.clicked.connect(self.check_active_button)
        self.dl_active_button.clicked.connect(self.closewin)

    # 输入框验证
    def check_input_func(self):
        if self.username_line.text() and self.password_line.text():
            self.dl_active_button.setEnabled(True)
        else:
            self.dl_active_button.setEnabled(False)

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

    # 登录按钮操作
    def check_active_button(self):
        self.driver.get(self.url)
        script = 'Object.defineProperty(navigator,"webdriver",{get:() => false,});'
        self.driver.execute_script(script)
        self.driver.maximize_window()
        time.sleep(1)
        username = self.username_line.text()
        password = self.password_line.text()
        try:
            self.driver.find_element_by_xpath("/html/body/div[4]/div/div/button").click()
        except:
            print("无广告")
        self.driver.find_element_by_xpath('/html/body/header/div/ul/li[12]/a').click()
        time.sleep(1)
        self.driver.find_element_by_id('normalLogin').click()
        time.sleep(1)
        input1 = self.driver.find_element_by_id("nameNormal")
        input2 = self.driver.find_element_by_id("pwdNormal")
        for i in username:
            input1.send_keys(i)
            time.sleep(random.uniform(0.2, 0.5))
        for i in password:
            input2.send_keys(i)
            time.sleep(random.uniform(0.2, 0.5))
        self.tuokuai_choose_run()
        self.Ui_processwindow = ProcessWindow(self.company_list, self.company_name_sum, self.driver, self.generate_name,
                                              self.generate_data, self.url)
        self.Ui_processwindow.show()

    # 对托块验证的选择运行
    def tuokuai_choose_run(self):
        if self.auto_Bracket == True:
            self.get_track_move()
            self.driver.find_element_by_xpath('/html/body/div[10]/div/div/div/div[2]/div[2]/form/button/b').click()
            try:
                self.driver.find_element_by_xpath('/html/body/header/div/ul/li[13]/a')
            except:
                reply = QMessageBox.question(self, '提示', '自动实现托块验证登陆失败，请联系开发人员！', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.close()
        else:
            time.sleep(10)
            self.driver.find_element_by_xpath('/html/body/div[10]/div/div/div/div[2]/div[2]/form/button/b').click()
            try:
                self.driver.find_element_by_xpath('/html/body/header/div/ul/li[13]/a')
            except:
                reply = QMessageBox.question(self, '提示', '请手动进行托块验证！',
                                             QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.driver.implicitly_wait(10)
            try:
                self.driver.find_element_by_xpath('/html/body/header/div/ul/li[13]/a')
            except:
                reply = QMessageBox.question(self, '提示', '未手动进行托块验证，请退出！', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.close()

    # 拖动托块
    def get_track_move(self):
        track = []
        current = 0
        mid = self.track * 3 / 4
        t = random.uniform(0.5, 0.8)
        v = 0
        while current <= self.track:
            if current <= mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        slider = self.driver.find_element_by_xpath("/html/body/div[10]/div/div/div/div[2]/div[2]/form/div[3]/div/div/div[1]/span")
        ActionChains(self.driver).click_and_hold(slider).perform()
        track += [5, 3]
        print(track)
        for i in track:
            ActionChains(self.driver).move_by_offset(xoffset=i, yoffset=0).perform()
            a = random.uniform(0.1, 0.5)
            time.sleep(a)
        ActionChains(self.driver).release(slider).perform()

    def closewin(self):
        self.close()