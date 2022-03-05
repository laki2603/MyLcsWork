# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GunnyBag.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(676, 300)
        self.formLayoutWidget = QtWidgets.QWidget(Form)
        self.formLayoutWidget.setGeometry(QtCore.QRect(80, 60, 471, 151))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setVerticalSpacing(41)
        self.formLayout.setObjectName("formLayout")
        self.lb_VehicleEntry_header1_vehicle_2 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lb_VehicleEntry_header1_vehicle_2.setFont(font)
        self.lb_VehicleEntry_header1_vehicle_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: bold 14pt \"MS Shell Dlg 2\";")
        self.lb_VehicleEntry_header1_vehicle_2.setObjectName("lb_VehicleEntry_header1_vehicle_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lb_VehicleEntry_header1_vehicle_2)
        self.le_BagWeight = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.le_BagWeight.setObjectName("le_BagWeight")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_BagWeight)
        self.lb_VehicleEntry_serialNumber_2 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lb_VehicleEntry_serialNumber_2.setFont(font)
        self.lb_VehicleEntry_serialNumber_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: bold 14pt \"MS Shell Dlg 2\";")
        self.lb_VehicleEntry_serialNumber_2.setObjectName("lb_VehicleEntry_serialNumber_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lb_VehicleEntry_serialNumber_2)
        self.le_NoOfBags = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.le_NoOfBags.setObjectName("le_NoOfBags")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.le_NoOfBags)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 671, 301))
        self.label.setStyleSheet("background-color: rgb(4, 7, 7);")
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(140, 190, 391, 102))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_ok = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pb_ok.setFont(font)
        self.pb_ok.setStyleSheet("\n"
"boder-style: outset;\n"
"border-wiidth: 2px;\n"
"border-radius: 8px;\n"
"border-color: black;\n"
"font: bold 16px;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("WeighBridgeScreens/Button/ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_ok.setIcon(icon)
        self.pb_ok.setIconSize(QtCore.QSize(118, 59))
        self.pb_ok.setObjectName("pb_ok")
        self.horizontalLayout.addWidget(self.pb_ok)
        self.pb_close = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pb_close.setFont(font)
        self.pb_close.setStyleSheet("\n"
"boder-style: outset;\n"
"border-wiidth: 2px;\n"
"border-radius: 12px;\n"
"border-color: black;\n"
"font: bold 16px;\n"
"")
        self.pb_close.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("WeighBridgeScreens/Button/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_close.setIcon(icon1)
        self.pb_close.setIconSize(QtCore.QSize(143, 100))
        self.pb_close.setObjectName("pb_close")
        self.horizontalLayout.addWidget(self.pb_close)
        self.label.raise_()
        self.formLayoutWidget.raise_()
        self.horizontalLayoutWidget.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lb_VehicleEntry_header1_vehicle_2.setText(_translate("Form", "BAG WEIGHT        "))
        self.lb_VehicleEntry_serialNumber_2.setText(_translate("Form", "NO OF BAGS"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())