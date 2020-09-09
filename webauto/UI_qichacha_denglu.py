# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'active_denglu.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit


class Ui_DengluWindow(object):
    def setupUi(self, DengluWindow):
        DengluWindow.setObjectName("DengluWindow")
        DengluWindow.resize(550, 330)
        self.centralwidget = QtWidgets.QWidget(DengluWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.dl_active_button = QtWidgets.QPushButton(self.centralwidget)
        self.dl_active_button.setGeometry(QtCore.QRect(240, 210, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dl_active_button.setFont(font)
        self.dl_active_button.setObjectName("dl_active_button")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 50, 261, 131))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.username_line = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.username_line.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.username_line.setFont(font)
        self.username_line.setObjectName("username_line")
        self.username_line.setPlaceholderText("Please enter your username")
        self.gridLayout.addWidget(self.username_line, 0, 1, 1, 1)
        self.username_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.gridLayout.addWidget(self.username_label, 0, 0, 1, 1)
        self.password_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.gridLayout.addWidget(self.password_label, 1, 0, 1, 1)
        self.password_line = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.password_line.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.password_line.setFont(font)
        self.password_line.setObjectName("password_line")
        self.password_line.setPlaceholderText("Please enter your password")
        self.password_line.setEchoMode(QLineEdit.Password)
        self.gridLayout.addWidget(self.password_line, 1, 1, 1, 1)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(320, 80, 230, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.choose_tuokuai = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.choose_tuokuai.setFont(font)
        self.choose_tuokuai.setObjectName("choose_tuokuai")
        self.verticalLayout.addWidget(self.choose_tuokuai)
        self.manual_verification = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.manual_verification.setFont(font)
        self.manual_verification.setObjectName("Manual_verification")
        self.verticalLayout.addWidget(self.manual_verification)
        self.auto_verification = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.auto_verification.setFont(font)
        self.auto_verification.setObjectName("auto_verification")
        self.auto_verification.setChecked(True)
        self.verticalLayout.addWidget(self.auto_verification)
        DengluWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DengluWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 560, 23))
        self.menubar.setObjectName("menubar")
        DengluWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DengluWindow)
        self.statusbar.setObjectName("statusbar")
        DengluWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DengluWindow)
        QtCore.QMetaObject.connectSlotsByName(DengluWindow)

    def retranslateUi(self, DengluWindow):
        _translate = QtCore.QCoreApplication.translate
        DengluWindow.setWindowTitle(_translate("DengluWindow", "企查查登录页面"))
        self.dl_active_button.setText(_translate("DengluWindow", "登录"))
        self.username_label.setText(_translate("DengluWindow", "用户名："))
        self.password_label.setText(_translate("DengluWindow", "密码："))
        self.choose_tuokuai.setText(_translate("DengluWindow", "托块验证方式："))
        self.manual_verification.setText(_translate("DengluWindow", "手动实现验证"))
        self.auto_verification.setText(_translate("DengluWindow", "自动实现验证(推荐)"))