# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lb_userName = QtWidgets.QLabel(self.centralwidget)
        self.lb_userName.setGeometry(QtCore.QRect(190, 240, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.lb_userName.setFont(font)
        self.lb_userName.setObjectName("lb_userName")
        self.le_userName = QtWidgets.QLineEdit(self.centralwidget)
        self.le_userName.setGeometry(QtCore.QRect(360, 250, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_userName.setFont(font)
        self.le_userName.setObjectName("le_userName")
        self.lb_passWord = QtWidgets.QLabel(self.centralwidget)
        self.lb_passWord.setGeometry(QtCore.QRect(190, 310, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.lb_passWord.setFont(font)
        self.lb_passWord.setObjectName("lb_passWord")
        self.le_passWord = QtWidgets.QLineEdit(self.centralwidget)
        self.le_passWord.setGeometry(QtCore.QRect(360, 320, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_passWord.setFont(font)
        self.le_passWord.setObjectName("le_passWord")
        self.pb_login = QtWidgets.QPushButton(self.centralwidget)
        self.pb_login.setGeometry(QtCore.QRect(290, 400, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.pb_login.setFont(font)
        self.pb_login.setObjectName("pb_login")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lb_userName.setText(_translate("MainWindow", "USER NAME"))
        self.lb_passWord.setText(_translate("MainWindow", "PASSWORD"))
        self.pb_login.setText(_translate("MainWindow", "LOGIN"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
