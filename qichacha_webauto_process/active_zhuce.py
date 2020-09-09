import time
import random

from selenium import webdriver
from selenium.webdriver import ActionChains

from UI_zhuce import Ui_ZhuceWindow
from active_process import ProcessWindow

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDesktopWidget


# 注册页面
class ZhuceWindow(QMainWindow, Ui_ZhuceWindow):

    def __init__(self, company_list, company_name_sum, generate_name, generate_data):
        super(ZhuceWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.count = 58
        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.track = 308

        self.url = 'https://www.qcc.com/?utm_source=baidu1&utm_medium=cpc&utm_term=pzsy/'
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
        try:
            self.driver.find_element_by_xpath("/html/body/div[4]/div/div/button").click()
        except:
            print("无广告")
        self.driver.find_element_by_xpath('/html/body/header/div/ul/li[12]/a/span').click()
        time.sleep(1)
        input_tel = self.driver.find_element_by_id('nameVerify')
        time.sleep(0.5)
        input_tel.send_keys(telephone)
        time.sleep(1)
        self.toukuai_choose_run()
        try:
            self.driver.find_element_by_xpath('/html/body/div[10]/div/div/div/div[3]/div[2]/form/div[2]/div/div/div[1]/div[2]/span/b')
            self.time.start()
            self.verification_label.setVisible(True)
            self.verification_line.setVisible(True)
        except:
            reply = QMessageBox.question(self, '提示', '拖块存在问题，请联系开发人员！',
                                         QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.close()

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
            self.count = 58

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
        slider = self.driver.find_element_by_xpath("/html/body/div[10]/div/div/div/div[3]/div[2]/form/div[2]/div/div/div[1]/span")
        ActionChains(self.driver).click_and_hold(slider).perform()
        track += [5, 3]
        print(track)
        for i in track:
            ActionChains(self.driver).move_by_offset(xoffset=i, yoffset=0).perform()
            a = random.uniform(0.1, 0.5)
            time.sleep(a)
        ActionChains(self.driver).release(slider).perform()

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
            self.get_track_move()
            try:
                self.driver.find_element_by_xpath('/html/body/div[10]/div/div/div/div[3]/div[2]/form/div[2]/div/div/div[1]/div[2]/span/b')
            except:
                reply = QMessageBox.question(self, '提示', '拖块存在问题，请联系开发人员！',
                                             QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.close()
        else:
            self.driver.implicitly_wait(15)
            try:
                self.driver.find_element_by_xpath('/html/body/div[10]/div/div/div/div[3]/div[2]/form/div[2]/div/div/div[1]/div[2]/span/b')
            except:
                reply = QMessageBox.question(self, '提示', '请手动进行托块验证！',
                                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.driver.implicitly_wait(10)
                else:
                    self.close()

    # 注册按钮操作
    def check_active_button(self):
        verification = self.verification_line.text()
        try:
            input_verification = self.driver.find_element_by_id('vcodeNormal')
            time.sleep(0.5)
            input_verification.send_keys(verification)
        except:
            reply = QMessageBox.question(self, '提示', '手动验证，则没有实现托块验证，重新启动程序，手动解决；自动验证，则托块验证存在问题，请联系开发人员！', QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.close()
        try:
            self.driver.find_element_by_xpath('/html/body/div[10]/div/div/div/div[3]/div[2]/form/button').click()
            self.Ui_processwindow = ProcessWindow(self.company_list, self.company_name_sum, self.driver, self.generate_name, self.generate_data)
            self.Ui_processwindow.show()
        except:
            self.close()

    def closewin(self):
        self.close()