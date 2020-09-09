import os
import random
import time

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QDesktopWidget

from selenium.webdriver import ActionChains

from UI_process import Ui_ProcessWindow


class MyThread(QThread, Ui_ProcessWindow):
    end_browser_num = pyqtSignal(int)
    success_browser_num = pyqtSignal(int)
    fail_browser_num = pyqtSignal(int)
    failname_browser_window = pyqtSignal(str)
    process_browser_window = pyqtSignal(str)

    def __init__(self, company_list, driver, generate_name, generate_data, url):
        super(MyThread, self).__init__()

        self.url = url
        self.generate_name = generate_name
        self.generate_data = generate_data
        self.driver = driver
        self.company_list = company_list
        self.n = 0
        self.s = 0
        self.f = 0

    # 运行
    def active(self):
        a = self.url.replace('"', '')
        self.process_browser_window.emit("正在爬取，请稍后。。。")
        for company_name in self.company_list:
            if u'\u4e00' <= company_name <= u'\u9fff':
                self.process_browser_window.emit("正在爬取的企业名称：" + company_name)
                b = self.driver.current_url
                if a == b:
                    input1 = self.driver.find_element_by_id('aqc-search-input')
                    time.sleep(1)
                    for i in company_name:
                        input1.send_keys(i)
                        time.sleep(random.uniform(0.2, 0.5))
                    self.driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[2]/div[2]/button').click()
                    time.sleep(1)
                    self.process_browser_window.emit("正在查询该企业，请稍后。。。")
                    self.get_company(company_name)
                else:
                    self.driver.find_element_by_xpath('/html/body/div[1]/header/div/div[2]/div/div[1]/div/input').clear()
                    time.sleep(1)
                    input2 = self.driver.find_element_by_xpath('/html/body/div[1]/header/div/div[2]/div/div[1]/div/input')
                    for i in company_name:
                        input2.send_keys(i)
                        time.sleep(random.uniform(0.2, 0.5))
                    self.driver.find_element_by_xpath('/html/body/div[1]/header/div/div[2]/button').click()
                    time.sleep(1)
                    self.process_browser_window.emit("正在查询该企业，请稍后。。。")
                    self.get_company(company_name)
            else:
                self.process_browser_window.emit("该企业名称存在问题，请检查企业名称文件!")
                self.s += 1
                self.success_browser_num.emit(self.s)
                self.failname_browser_window.emit(company_name)
                self.n += 1
                self.end_browser_num.emit(self.n)
                continue

        sum = self.s + self.f
        self.process_browser_window.emit(" --爬取结束-- \n 应爬 %s条 已爬 %s条  爬取成功 %s条 爬取失败 %s条" % (sum, self.n, self.s, self.f))

    # 信息采集
    def get_company(self, company_name):
        nowhandles = self.driver.current_window_handle
        time.sleep(1)
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/div/h3/a').click()
        except:
            self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[2]/div[2]/div/div/div/div/div[3]')
            self.process_browser_window.emit(company_name + '没有查找到该企业信息，请确认该名称是否存在！')
            self.s += 1
            self.success_browser_num.emit(self.s)
            self.failname_browser_window.emit(company_name)
            self.n += 1
            self.end_browser_num.emit(self.n)
            return

        time.sleep(1)
        self.process_browser_window.emit("已进入%s该企业详情页面，请稍后。。。" % company_name)
        allhandles = self.driver.window_handles
        for handles in allhandles:
            if handles != nowhandles:
                self.driver.switch_to.window(handles)
        time.sleep(1)
        js = "window.scrollTo(0,600)"
        self.driver.execute_script(js)
        time.sleep(0.5)

        # 工商信息表
        company_data_1 = ''
        try:
            business_content = self.driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[5]/div[1]/div[3]/table/tbody/tr')
            # 工商信息采集
            for cont_1 in business_content:
                company_title_1 = cont_1.find_element_by_xpath('.//td[1]')
                try:
                    company_info_1 = cont_1.find_element_by_xpath('.//td[2]')
                except:
                    company_info_1 = cont_1.find_element_by_xpath('.//td[2]/div[2]/a[1]')
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

            self.process_browser_window.emit(company_name + '--工商信息爬取成功!')
            company_content_1 = company_data_1
        except:
            self.process_browser_window.emit(company_name + '没有查找到该企业工商信息，请确认该名称是否存在！')
            self.f += 1
            self.fail_browser_num.emit(self.f)
            self.failname_browser_window.emit(company_name)
            self.n += 1
            self.end_browser_num.emit(self.n)
            return

        # 股东信息表
        Action = ActionChains(self.driver)
        element = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/div/div[1]/a')
        Action.move_to_element(element).perform()
        time.sleep(1)
        company_data_2 = ''
        try:

            self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div[4]/div/div/div[1]/div/a[3]').click()

            time.sleep(1)
            shareholder_content = self.driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div/div[5]/div[1]/div[4]/table/tbody/tr')
            # 股东信息采集
            for cont_2 in shareholder_content:
                shareholder_info_1 = cont_2.find_element_by_xpath('.//td[2]/div/div[2]/a[1]')
                shareholder_info_2 = cont_2.find_element_by_xpath('.//td[3]/div/span')
                shareholder_info_3 = cont_2.find_element_by_xpath('.//td[4]/div/span')
                shareholder_info_4 = cont_2.find_element_by_xpath('.//td[5]/div/span')
                company_data_2 += shareholder_info_1.text + ';' + shareholder_info_2.text + ';' + shareholder_info_3.text + '\n'
            self.process_browser_window.emit(company_name + '--股东信息爬取成功!')
            company_content_2 = '--股东信息：' + '\n' + '股东-' + '-持股占比-' + '-认缴出资额' + '实际出资额' + '\n' + company_data_2
        except:
            company_content_2 = '--股东信息：' + '\n' + '股东-' + '-持股占比-' + '-认缴出资额' + '实际出资额' + '\n' + company_data_2
            self.process_browser_window.emit(company_name + '--股东信息爬取失败，或该公司未有股东信息!')

        # 公司主要人员信息表
        Action.move_to_element(element).perform()
        time.sleep(1)
        company_data_3 = ''
        try:
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div[4]/div/div/div[1]/div/a[5]').click()
            time.sleep(1)
            manager_content = self.driver.find_elements_by_xpath(
                '/html/body/div[1]/div/div/div[5]/div[1]/div[6]/table/tbody/tr')
            # 公司主要人员信息采集
            for cont_3 in manager_content:
                manager_info_1 = cont_3.find_element_by_xpath('.//td[2]/div/div[2]/a[1]')
                manager_info_2 = cont_3.find_element_by_xpath('.//td[3]/div/span')
                company_data_3 += manager_info_1.text + ';' + manager_info_2.text + '\n'
            self.process_browser_window.emit(company_name + '--主要人员爬取成功')
            company_content_3 = '--主要人员信息：' + '\n' + '姓名-' + '-职位' + '\n' + company_data_3
        except:
            company_content_3 = '--主要人员信息：' + '\n' + '姓名-' + '-职位' + '\n' + company_data_3

            self.process_browser_window.emit(company_name + '--主要人员爬取失败,或该公司未有主要人员信息。。。')

        company_content = '----' + company_name + '\n' + company_content_1 + company_content_2 + company_content_3 + '\n'

        if not os.path.exists(self.generate_data + self.generate_name):
            open(self.generate_data + self.generate_name, 'a', encoding='utf-8')
        with open(self.generate_data + self.generate_name, 'a', encoding='utf-8') as cp_file:
            cp_file.write(company_content)
            self.process_browser_window.emit(company_name + "--信息保存成功!")
        self.s += 1
        self.success_browser_num.emit(self.s)

        self.n += 1
        self.end_browser_num.emit(self.n)
        self.driver.close()
        self.driver.switch_to.window(nowhandles)

    def run(self):
        self.active()


class ProcessWindow(QMainWindow, Ui_ProcessWindow):

    def __init__(self, company_list, company_name_sum, driver, generate_name, generate_data, url):
        super(ProcessWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.url = url
        self.generate_name = generate_name
        self.generate_data = generate_data
        self.company_list = company_list
        self.company_name_sum = company_name_sum
        self.driver = driver

        self.control_init()

        self.success_browser.append(str(0))
        self.end_browser.append(str(0))
        self.fail_browser.append(str(0))

    # 控件设置
    def control_init(self):

        screen = QDesktopWidget().screenGeometry()
        self.move(0, screen.height() * 0.3)

        self.active_button.setEnabled(True)
        self.active_button.clicked.connect(self.check_active_button)

    # 开始按钮
    def check_active_button(self):
        self.sum_browser.append(str(self.company_name_sum))
        self.thread_author()
        self.active_button.setEnabled(False)

    # 线程相关
    def thread_author(self):
        self.thread = MyThread(self.company_list, self.driver, self.generate_name, self.generate_data, self.url)
        self.thread.end_browser_num.connect(self.show_data_1)
        self.thread.success_browser_num.connect(self.show_data_2)
        self.thread.fail_browser_num.connect(self.show_data_3)
        self.thread.failname_browser_window.connect(self.show_data_4)
        self.thread.process_browser_window.connect(self.show_data_5)
        self.thread.start()

    # 页面显示数据
    def show_data_1(self, i):
        self.end_browser.setPlainText("")
        self.end_browser.append(str(i))

    def show_data_2(self, i):
        self.success_browser.setPlainText("")
        self.success_browser.append(str(i))

    def show_data_3(self, i):
        self.fail_browser.setPlainText("")
        self.fail_browser.append(str(i))

    def show_data_4(self, i):
        self.failname_browser.append(i)

    def show_data_5(self, i):
        self.process_browser.append(i)

    # 退出设置
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()