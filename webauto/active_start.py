import sys

from PyQt5 import QtCore

from UI_start import Ui_MainWindow

from aiqicha_denglu import Aiqicha_DengluWindow
from qichacha_denglu import Qichacha_DengluWindow
from tianyancha_denglu import Tianyancha_DengluWindow

from qichacha_zhuce import Qichacha_ZhuceWindow
from tianyancha_zhuce import Tianyancha_ZhuceWindow

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.spacer = ','
        self.url = 'https://www.tianyancha.com/'
        self.generate_name = ''
        self.generate_data = ''
        self.company_list = []
        self.city_name = []
        self.company_name_sum = 0

        self.control_init()

    # 控件设置
    def control_init(self):
        self.cpyname_line.textChanged.connect(self.check_import_func)
        self.cpydata_line.textChanged.connect(self.check_import_func)

        self.denglu_button.setEnabled(False)
        self.zhuce_button.setEnabled(False)
        self.import_button.setEnabled(False)
        self.choose_url.setEnabled(False)
        self.denglu_button.clicked.connect(self.check_denglu_button)
        self.denglu_button.clicked.connect(self.closewin)
        self.zhuce_button.clicked.connect(self.check_zhuce_button)
        self.zhuce_button.clicked.connect(self.closewin)
        self.import_button.clicked.connect(self.import_file)

        self.choose_spacer.currentTextChanged.connect(self.spacer_site)
        self.choose_url.currentTextChanged.connect(self.url_site)

        self.import_result.setVisible(False)
        self.import_prompt.setVisible(False)

    # 输入框设置
    def check_input_func(self):
        if self.import_result.isVisible():
            self.denglu_button.setEnabled(True)
            self.zhuce_button.setEnabled(True)
        else:
            self.denglu_button.setEnabled(False)
            self.zhuce_button.setEnabled(False)

    # 导入按钮设置
    def check_import_func(self):
        if self.cpyname_line.text() and self.cpydata_line.text():
            self.import_button.setEnabled(True)
        else:
            self.import_button.setEnabled(False)

    # 导入省市名称文件
    def import_city_file(self):
        city = open('new_city.txt', 'r')
        for j in city.readlines():
            data = j.replace('\n', '')
            self.city_name.append(data)
        city.close()

    # 爬取网址选择
    def url_site(self, i):
        if i == "天眼查":
            self.zhuce_button.setEnabled(True)
            self.url = 'https://www.tianyancha.com/'
        elif i == "企查查":
            self.zhuce_button.setEnabled(True)
            self.url = 'https://www.qcc.com/'
        else:
            self.zhuce_button.setEnabled(False)
            self.url = 'https://aiqicha.baidu.com/'

    # 企业名称间隔符设置
    def spacer_site(self, i):
        if i == "回车":
            self.spacer = '\n'
        elif i == "空格":
            self.spacer = ' '
        else:
            self.spacer = i

    # 导入文件操作
    def import_file(self):
        if self.spacer == '\n':
            try:
                company_data = QFileDialog.getOpenFileName(self, "Open company name file", '*.txt')
                f = open(company_data[0], 'r', encoding='utf-8')
                a = company_data[0].split("/")
                for i in f.readlines():
                    company_name = i.replace(self.spacer, '')
                    self.company_list.append(company_name)
                for c in self.company_list:
                    self.company_name_sum += 1
                f.close()
                self.import_result.setVisible(True)
                self.import_prompt.setVisible(True)
                self.import_result.setText(a[-1])
                self.import_button.setVisible(False)
                self.choose_url.setEnabled(True)
                self.check_input_func()
            except:
                reply = QMessageBox.warning(self, '提示', '导入文件错误！请重新导入',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    pass
                else:
                    self.close()
        else:
            try:
                company_data = QFileDialog.getOpenFileName(self, "Open company name file", '*.txt')
                f = open(company_data[0], 'r', encoding='utf-8')
                a = company_data[0].split("/")
                for i in f.readlines():
                    self.company_list = i.split(self.spacer, -1)
                for c in self.company_list:
                    self.company_name_sum += 1
                f.close()
                self.import_result.setVisible(True)
                self.import_prompt.setVisible(True)
                self.import_result.setText(a[-1])
                self.import_button.setVisible(False)
                self.choose_url.setEnabled(True)
                self.check_input_func()
                self.choose_spacer.setEnabled(False)
            except:
                reply = QMessageBox.warning(self, '提示', '导入文件错误！请重新导入',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    pass
                else:
                    self.close()

        # self.import_file_detect()

    # 对导入文件的检测
    def import_file_detect(self):
        # self.import_city_file()
        print(self.city_name)
        for i in self.company_list:
            print(i)
            if any(jj in i for jj in self.city_name):
                pass
            else:
                reply = QMessageBox.warning(self, '提示', '导入文件错误！请重新导入', QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    pass
                    break

        self.import_file()

    # 登录按钮操作
    def check_denglu_button(self):
        self.generate_name = self.cpyname_line.text()
        self.generate_data = self.cpydata_line.text()
        if self.url == 'https://www.tianyancha.com/':
            self.Ui_dengluwindow = Tianyancha_DengluWindow(self.company_list, self.company_name_sum, self.generate_name, self.generate_data, self.url)
            self.Ui_dengluwindow.show()
        elif self.url == 'https://aiqicha.baidu.com/':
            self.Ui_dengluwindow = Aiqicha_DengluWindow(self.company_list, self.company_name_sum, self.generate_name,
                                              self.generate_data, self.url)
            self.Ui_dengluwindow.show()
        else:
            self.Ui_dengluwindow = Qichacha_DengluWindow(self.company_list, self.company_name_sum, self.generate_name,
                                              self.generate_data, self.url)
            self.Ui_dengluwindow.show()

    # 注册按钮操作
    def check_zhuce_button(self):
        self.generate_name = self.cpyname_line.text()
        self.generate_data = self.cpydata_line.text()
        if self.url == 'https://www.tianyancha.com/':
            self.Ui_zhucewindow = Tianyancha_ZhuceWindow(self.company_list, self.company_name_sum, self.generate_name, self.generate_data, self.url)
            self.Ui_zhucewindow.show()
        else:
            self.Ui_zhucewindow = Qichacha_ZhuceWindow(self.company_list, self.company_name_sum, self.generate_name,
                                                          self.generate_data, self.url)
            self.Ui_zhucewindow.show()

    # 主页面退出操作
    def closewin(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec())