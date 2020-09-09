import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog

import os
import time
import random
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class Ui_WebAuto(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 150)

        self.user_label = QLabel('用户名：', self)
        self.pwd_label = QLabel('密码：', self)
        self.cpydata_label = QLabel('生成文件地址：', self)
        self.cpyname_label = QLabel('生成文件名称：', self)
        self.spacer_label = QLabel('导入企业名称分隔符：', self)
        self.select_cpyname_label = QLabel('导入公司名称文件：', self)
        self.user_line = QLineEdit(self)
        self.pwd_line = QLineEdit(self)
        self.cpydata_line = QLineEdit(self)
        self.cpyname_line = QLineEdit(self)
        self.spacer_line = QLineEdit(self)
        self.active_button = QPushButton('开始', self)
        self.select_button = QPushButton('导入', self)
        self.login_button = QPushButton('注册', self)

        self.grid_layout = QGridLayout()
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()

        self.url = 'https://www.tianyancha.com/'
        self.driver = webdriver.Chrome()
        self.company_list = []
        self.j = 0

    # 页面布局
    def layout_init(self):
        self.grid_layout.addWidget(self.user_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.user_line, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.pwd_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.pwd_line, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.cpydata_label, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.cpydata_line, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.cpyname_label, 3, 0, 1, 1)
        self.grid_layout.addWidget(self.cpyname_line, 3, 1, 1, 1)
        self.grid_layout.addWidget(self.spacer_label, 4, 0, 1, 1)
        self.grid_layout.addWidget(self.spacer_line, 4, 1, 1, 1)
        self.grid_layout.addWidget(self.select_cpyname_label, 5, 0, 1, 1)
        self.grid_layout.addWidget(self.select_button, 5, 1, 1, 1)
        self.h_layout.addWidget(self.active_button)
        self.h_layout.addWidget(self.login_button)
        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    # 输入框按钮操作
    def lineedit_init(self):
        self.user_line.setPlaceholderText('Please enter your username')
        self.pwd_line.setPlaceholderText('Please enter your password')
        self.pwd_line.setEchoMode(QLineEdit.Password)
        self.cpydata_line.setPlaceholderText('示例:C:\\kuaifawu\\')
        self.cpyname_line.setPlaceholderText('示例:company_data.txt')

        self.user_line.textChanged.connect(self.check_input_func)
        self.pwd_line.textChanged.connect(self.check_input_func)
        self.cpyname_line.textChanged.connect(self.check_input_func)
        self.cpydata_line.textChanged.connect(self.check_input_func)
        self.spacer_line.textChanged.connect(self.check_input_func)

        self.select_button.clicked.connect(self.select_file)
        self.login_button.clicked.connect(self.check_login_func)

    def pushbutton_init(self):
        self.active_button.setEnabled(False)
        self.active_button.clicked.connect(self.check_active_func)

    # 输入框设置
    def check_input_func(self):
        if self.user_line.text() and self.pwd_line.text() and self.cpyname_line.text() and self.cpydata_line.text():
            self.active_button.setEnabled(True)
        else:
            self.active_button.setEnabled(False)

    # 开始按钮
    def check_active_func(self):
        self.check_input_func()
        self.index_login()
        a = self.url.replace('"', '')
        for company_name in self.company_list:
            if company_name != None:
                b = self.driver.current_url
                if a == b:
                    try:
                        print(company_name)
                        input_company = self.driver.find_element_by_id('home-main-search')
                        time.sleep(1)
                        input_company.send_keys(company_name)
                        time.sleep(1)
                        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div').click()
                        time.sleep(1)
                        self.get_company_info(company_name)
                    except:
                        continue
                else:
                    try:
                        self.driver.find_element_by_id('header-company-search').clear()
                        time.sleep(1)
                        self.driver.find_element_by_id('header-company-search').send_keys(company_name)
                        time.sleep(1)
                        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div[1]/div').click()
                        time.sleep(1)
                        self.get_company_info(company_name)
                    except:
                        continue
            else:
                self.success_func()

    # 注册按钮
    def check_login_func(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[1]/div/div[2]/div/div[5]/a').click()

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
        ActionChains(self.driver).move_by_offset(xoffset=196, yoffset=0).perform()
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

    # 滑块移动
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

    # 登录
    def index_login(self):
        username = self.user_line.text()
        password = self.pwd_line.text()
        self.driver.get(self.url)
        script = 'Object.defineProperty(navigator,"webdriver",{get:() => false,});'
        self.driver.execute_script(script)
        self.driver.maximize_window()
        time.sleep(2)
        try:
            self.driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div").click()
        except:
            print("无广告")
        # self.driver.find_element_by_partial_link_text("登录/注册").click()
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[1]/div/div[2]/div/div[5]/a').click()
        time.sleep(2)
        self.driver.find_element_by_xpath(
            '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[1]/div[2]').click()
        time.sleep(1)
        input1 = self.driver.find_element_by_id("mobile")
        input2 = self.driver.find_element_by_id("password")

        input1.send_keys(username)
        time.sleep(0.7)
        input2.send_keys(password)
        time.sleep(1)
        self.driver.find_element_by_xpath(
            "/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[2]/div[2]").click()

        # time.sleep(10)
        # 拖块部分
        self.before_deal_image()
        self.after_deal_image()
        time.sleep(1)
        self.track = self.slide_distance('ele_capture1.png', 'ele_capture2.png')
        print('按钮移动距离：', self.track)
        self.get_track_move(self.track)
        try:
            self.driver.find_element_by_partial_link_text('大卫·佩特鲁齐')
            print('登录成功！')
            return self.track
        except:
            print('拖块存在问题，正在重试...')
            self.for_tuokuai()

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
                self.driver.find_element_by_xpath('/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[2]/div[2]').click()
                time.sleep(1)
                self.before_deal_image()
                time.sleep(1)
                self.after_deal_image()
                time.sleep(1)
                self.track = self.slide_distance('ele_capture1.png', 'ele_capture2.png')
                print('按钮移动距离：', self.track)
                self.get_track_move(self.track)
                self.driver.find_element_by_partial_link_text('大卫·佩特鲁齐')
                self.j += 1
                return self.track
            except:
                print('拖块误差错误，重试中...')
            if self.j > 0:
                print('拖动成功')
                break
        self.driver.close()
        print('----拖块验证存在错误----')
        self.error_func()

    # 导入文件
    def select_file(self):
        spacer = self.spacer_line.text()
        company_data = QFileDialog.getOpenFileName(self, "Open company name File", "*.txt")
        f = open(company_data[0], 'r', encoding='utf-8')
        for i in f.readlines():
            company_name = i.replace(spacer, '')
            self.company_list.append(company_name)
        f.close()
        if self.company_list:
            success = QMessageBox.question(self, '提示', '导入文件成功！', QMessageBox.Yes)
            if success == QMessageBox.Yes:
                pass
        else:
            failure = QMessageBox.question(self, '提示', '导入文件失败！或导入文件不可用，重新导入？',
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if failure == QMessageBox.Yes:
                pass
            else:
                self.closeEvent()

    # 信息采集
    def get_company_info(self, company_name):
        nowhandles = self.driver.current_window_handle
        time.sleep(1)
        js1 = "window.scrollTo(0,500)"
        self.driver.execute_script(js1)
        time.sleep(1)
        try:
            self.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div/div[3]/div[1]/a').click()
        except:
            self.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/a').click()
        time.sleep(1)
        allhandles = self.driver.window_handles
        for handles in allhandles:
            if handles != nowhandles:
                self.driver.switch_to.window(handles)
        time.sleep(1)
        js2 = "window.scrollTo(0,650)"
        self.driver.execute_script(js2)
        time.sleep(1.5)
        # 工商信息表
        try:
            business_content = self.driver.find_elements_by_xpath('.//table[contains(@class, "table")'
                                                            ' and contains(@class, "-striped-col")'
                                                            ' and contains(@class, "-border-top-none")'
                                                            '][1]/tbody[1]/tr')

            # 工商信息采集
            company_data_1 = ''
            for cont_1 in business_content:
                # if self.j < 5:
                company_title_1 = cont_1.find_element_by_xpath('.//td[1]')
                company_info_1 = cont_1.find_element_by_xpath('.//td[2]')
                try:
                    company_title_2 = cont_1.find_element_by_xpath('.//td[3]')
                except:
                    pass
                try:
                    company_info_2 = cont_1.find_element_by_xpath('.//td[4]')
                except:
                    pass
                company_data_1 += company_title_1.text + ':' + company_info_1.text + ';' + company_title_2.text + \
                                        ':' + company_info_2.text + '\n'
                    # self.j += 1
                # else:
                #     break

            company_content_1 = company_data_1
        except:
            print(company_name, '工商信息爬取失败')

        # 股东信息表
        try:
            Action = ActionChains(self.driver)
            element = self.driver.find_element_by_class_name('itemtitle.-active')
            Action.move_to_element(element).perform()
            time.sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[5]/div[1]/div/div[1]/div/div/div[8]/div[1]/div/div[5]').click()
            time.sleep(1)
            shareholder_content = self.driver.find_elements_by_xpath('/html/body/div[2]/div/div/div[5]/div[1]/div/div[2]/div[1]/div[6]/div[2]/table/tbody/tr')

            # 股东信息采集
            company_data_2 = ''
            for cont_2 in shareholder_content:
                shareholder_info_1 = cont_2.find_element_by_xpath('.//td[2]/table/tbody/tr/td[2]/a')
                shareholder_info_2 = cont_2.find_element_by_xpath('.//td[3]/div/div/span')
                shareholder_info_3 = cont_2.find_element_by_xpath('.//td[4]/div/span')
                company_data_2 += shareholder_info_1.text + ';' + shareholder_info_2.text + ';' + shareholder_info_3.text + '\n'
            company_content_2 = '--股东信息：' + '\n' + '股东-' + '-持股占比-' + '-认缴出资额' + '\n' + company_data_2
        except:
            print(company_name, '股东信息爬取失败')

        # 公司主要人员信息表
        try:
            Action.move_to_element(element).perform()
            time.sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[5]/div[1]/div/div[1]/div/div/div[8]/div[1]/div/div[4]').click()
            time.sleep(1)
            manager_content = self.driver.find_elements_by_xpath('/html/body/div[2]/div/div/div[5]/div[1]/div/div[2]/div[1]/div[5]/div[2]/div/table/tbody/tr')

            # 公司主要人员信息采集
            company_data_3 = ''
            for cont_3 in manager_content:
                manager_info_1 = cont_3.find_element_by_xpath('.//td[2]/table/tbody/tr/td[2]/a')
                manager_info_2 = cont_3.find_element_by_xpath('.//td[3]/span')
                company_data_3 += manager_info_1.text + ';' + manager_info_2.text + '\n'
            company_content_3 = '--主要人员信息：' + '\n' + '姓名-' + '-职位' + '\n' + company_data_3
        except:
            print(company_name, '公司主要人员爬取失败')

        # 信息保存
        company_data_name = self.cpyname_line.text()
        company_data_site = self.cpydata_line.text()
        company_content = '----' + company_name + '\n' + company_content_1 + company_content_2 + company_content_3 + '\n'
        if not os.path.exists(company_data_site+company_data_name):
            open(company_data_site+company_data_name, 'a', encoding='utf-8')
        with open(company_data_site+company_data_name, 'a', encoding='utf-8') as cp_file:
            cp_file.write(company_content)
            print("信息保存成功!")
        time.sleep(1)

        self.driver.close()
        self.driver.switch_to.window(nowhandles)

    # 退出操作
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', 'Are you sure to quit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 错误退出
    def error_func(self):
        error = QMessageBox.critical(self, '错误', '程序错误！', QMessageBox.Yes)
        if error == QMessageBox.Yes:
            self.closeEvent()

    def success_func(self):
        success = QMessageBox.question(self, '提示', '爬取成功！', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if success == QMessageBox.Yes:
            pass
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Ui_WebAuto()
    demo.show()
    sys.exit(app.exec())