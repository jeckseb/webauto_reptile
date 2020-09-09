import random
import time

from PyQt5.QtCore import QTimer
from selenium import webdriver
from selenium.webdriver import ActionChains

from UI_aiqicha_denglu import Ui_DengluWindow
from aiqicha_process import ProcessWindow

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDesktopWidget


# 登录页面
class Aiqicha_DengluWindow(QMainWindow, Ui_DengluWindow):

    def __init__(self, company_list, company_name_sum, generate_name, generate_data, url):
        super(Aiqicha_DengluWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.count = 58
        self.time = QTimer(self)
        self.time.setInterval(1000)

        self.url = url
        self.driver = webdriver.Chrome()

        self.generate_name = generate_name
        self.generate_data = generate_data
        self.company_list = company_list
        self.company_name_sum = company_name_sum

        self.control_init()
        self.choose_input = None

    # 页面组件设置
    def control_init(self):
        screen = QDesktopWidget().screenGeometry()
        self.move(0, screen.height() * 0.3)

        self.password_line.textChanged.connect(self.check_input_password)
        self.verification_line.textChanged.connect(self.check_input_sms)

        self.password_verification.toggled.connect(self.input_verification)
        self.sms_verification.toggled.connect(self.input_verification)

        self.password_line.setVisible(False)
        self.password_label.setVisible(False)
        self.verification_button.setVisible(False)
        self.verification_line.setVisible(False)
        self.active_button.setEnabled(False)

        self.verification_button.clicked.connect(self.get_verification_button)

        self.active_button.clicked.connect(self.check_active_button)
        self.active_button.clicked.connect(self.closewin)

    # 密码输入框验证
    def check_input_password(self):
        if self.password_line.text():
            self.active_button.setEnabled(True)
        else:
            self.active_button.setEnabled(False)

    # 短信输入框验证
    def check_input_sms(self):
        if self.verification_line.text():
            self.active_button.setEnabled(True)
        else:
            self.active_button.setEnabled(False)

    # 登录方式选择
    def input_verification(self):
        radiobutton = self.sender()
        if radiobutton.isChecked():
            if radiobutton == self.password_verification:
                self.choose_input = True
                self.password_line.setVisible(True)
                self.password_label.setVisible(True)
                self.verification_line.setVisible(False)
                self.verification_button.setVisible(False)
            else:
                self.choose_input = False
                # self.verification_button.setVisible(True)
                # self.verification_line.setVisible(True)
                self.password_line.setVisible(False)
                self.password_label.setVisible(False)
        else:
            if radiobutton == self.password_verification:
                self.choose_input = True
                self.password_line.setVisible(True)
                self.password_label.setVisible(True)
                self.verification_line.setVisible(False)
                self.verification_button.setVisible(False)
            else:
                self.choose_input = False
                # self.verification_button.setVisible(True)
                # self.verification_line.setVisible(True)
                self.password_line.setVisible(False)
                self.password_label.setVisible(False)

    # 获取验证码按钮操作
    def get_verification_button(self):
        # self.verification_button.setEnabled(False)
        # telephone = self.username_line.text()
        # self.driver.get(self.url)
        # script = 'Object.defineProperty(navigator,"webdriver",{get:() => false,});'
        # self.driver.execute_script(script)
        # self.driver.maximize_window()
        # time.sleep(1)
        # self.driver.find_element_by_xpath('/html/body/div[1]/header/div/div[1]/span[1]').click()
        # time.sleep(0.5)
        # self.driver.find_element_by_id('TANGRAM__PSP_4__smsSwitchWrapper').click()
        # time.sleep(0.5)
        # input = self.driver.find_element_by_id('TANGRAM__PSP_4__smsPhone')
        # for i in telephone:
        #     input.send_keys(i)
        #     time.sleep(0.4)
        # time.sleep(0.5)
        # self.driver.find_element_by_id('TANGRAM__PSP_4__smsTimer').click()
        # self.time.timeout.connect(self.Refresh)
        self.verification_button.setEnabled(False)
        self.verification_line.setVisible(False)
        reply = QMessageBox.question(self, '提示', '获取验证码需字母验证，未实现，该功能不能使用！', QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            pass

    # 验证码刷新
    def Refresh(self):
        self.time.start()
        if self.count >= 0:
            self.verification_button.setText(str(self.count) + '秒')
            self.count -= 1
        else:
            self.time.stop()
            self.verification_button.setEnabled(True)
            self.verification_button.setText('重新获取验证码')
            self.count = 58

    # 登录按钮操作
    def check_active_button(self):
        if self.choose_input == True:
            self.driver.get(self.url)
            script = 'Object.defineProperty(navigator,"webdriver",{get:() => false,});'
            self.driver.execute_script(script)
            self.driver.maximize_window()
            time.sleep(1)
            username = self.username_line.text()
            password = self.password_line.text()
            self.driver.find_element_by_xpath('/html/body/div[1]/header/div/div[1]/span[1]').click()
            time.sleep(1)
            input1 = self.driver.find_element_by_id("TANGRAM__PSP_4__userName")
            input2 = self.driver.find_element_by_id("TANGRAM__PSP_4__password")
            for i in username:
                input1.send_keys(i)
                time.sleep(random.uniform(0.2, 0.5))
            for i in password:
                input2.send_keys(i)
                time.sleep(random.uniform(0.2, 0.5))
            self.driver.find_element_by_id('TANGRAM__PSP_4__submit').click()
            self.Ui_processwindow = ProcessWindow(self.company_list, self.company_name_sum, self.driver, self.generate_name,
                                                  self.generate_data, self.url)
            self.Ui_processwindow.show()
        else:
            input = self.driver.find_element_by_id('TANGRAM__PSP_4__smsVerifyCode')
            for i in self.verification_line.text():
                input.send_keys(i)
                time.sleep(0.4)
            self.driver.find_element_by_id('TANGRAM__PSP_4__submit').click()
            self.Ui_processwindow = ProcessWindow(self.company_list, self.company_name_sum, self.driver,
                                                  self.generate_name,
                                                  self.generate_data, self.url)
            self.Ui_processwindow.show()

    def closewin(self):
        self.close()