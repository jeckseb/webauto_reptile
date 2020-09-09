# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crawling_process.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QTextCursor


class Ui_ProcessWindow(object):
    def setupUi(self, ProcessWindow):
        ProcessWindow.setObjectName("ProcessWindow")
        ProcessWindow.resize(696, 370)
        self.centralwidget = QtWidgets.QWidget(ProcessWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.failname_label = QtWidgets.QLabel(self.centralwidget)
        self.failname_label.setGeometry(QtCore.QRect(300, 130, 111, 31))
        self.failname_label.setObjectName("failname_label")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(310, 20, 291, 55))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.sum_browser = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        self.sum_browser.setObjectName("sum_browser")
        self.gridLayout.addWidget(self.sum_browser, 2, 2, 1, 1)
        self.success_browser = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        self.success_browser.setObjectName("success_browser")
        self.gridLayout.addWidget(self.success_browser, 4, 2, 1, 1)
        self.sum_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.sum_label.setObjectName("sum_label")
        self.gridLayout.addWidget(self.sum_label, 2, 0, 1, 1)
        self.end_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.end_label.setObjectName("end_label")
        self.gridLayout.addWidget(self.end_label, 2, 3, 1, 1)
        self.fail_browser = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        self.fail_browser.setObjectName("fail_browser")
        self.gridLayout.addWidget(self.fail_browser, 4, 4, 1, 1)
        self.end_browser = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        self.end_browser.setObjectName("end_browser")
        self.end_browser.moveCursor(QTextCursor.End)
        self.gridLayout.addWidget(self.end_browser, 2, 4, 1, 1)
        self.success_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.success_label.setObjectName("success_label")
        self.gridLayout.addWidget(self.success_label, 4, 0, 1, 1)
        self.fail_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.fail_label.setObjectName("fail_label")
        self.gridLayout.addWidget(self.fail_label, 4, 3, 1, 1)
        self.process_browser = QtWidgets.QTextBrowser(self.centralwidget)
        self.process_browser.setGeometry(QtCore.QRect(30, 10, 231, 291))
        self.process_browser.setObjectName("process_browser")
        self.process_browser.moveCursor(QTextCursor.End)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(330, 270, 311, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.active_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.active_button.setObjectName("active_button")
        self.horizontalLayout.addWidget(self.active_button)
        self.end_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.end_button.setObjectName("end_button")
        self.horizontalLayout.addWidget(self.end_button)
        self.failname_browser = QtWidgets.QTextBrowser(self.centralwidget)
        self.failname_browser.setGeometry(QtCore.QRect(420, 120, 221, 131))
        self.failname_browser.setObjectName("failname_browser")
        ProcessWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ProcessWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 696, 23))
        self.menubar.setObjectName("menubar")
        ProcessWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ProcessWindow)
        self.statusbar.setObjectName("statusbar")
        ProcessWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ProcessWindow)
        QtCore.QMetaObject.connectSlotsByName(ProcessWindow)

    def retranslateUi(self, ProcessWindow):
        _translate = QtCore.QCoreApplication.translate
        ProcessWindow.setWindowTitle(_translate("ProcessWindow", "天眼查爬取"))
        self.failname_label.setText(_translate("ProcessWindow", "爬取失败企业名称："))
        self.sum_label.setText(_translate("ProcessWindow", "共爬取："))
        self.end_label.setText(_translate("ProcessWindow", "已完成："))
        self.success_label.setText(_translate("ProcessWindow", "成功爬取："))
        self.fail_label.setText(_translate("ProcessWindow", "失败爬取："))
        self.active_button.setText(_translate("ProcessWindow", "开始"))
        self.end_button.setText(_translate("ProcessWindow", "完成"))
