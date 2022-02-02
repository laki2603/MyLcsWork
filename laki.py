import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLineEdit,QWidget
from PyQt5 import QtWidgets
from PyQt5.Qt import QAbstractItemView
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import sqlite3
import serial
import serial.tools.list_ports
import threading
from datetime import datetime,timedelta,date

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from tabulate import tabulate

from uitest import Ui_MainWindow
import xlsxwriter
from PyQt5.uic import loadUiType
import LoginWindow


class LoginWindowcls(QObject):
    def __init__(self):
        super().__init__()
        self.main_window = QMainWindow()
        self.lui = LoginWindow.Ui_MainWindow()
        self.lui.setupUi(self.main_window)
        self.lui.le_passWord.setEchoMode(QLineEdit.Password)
        self.main_window.show()
        self.lui.pb_login.clicked.connect(self.CheckUser)



    LoginUpdate = pyqtSignal(str)

    def CheckUser(self):

        self.name = self.lui.le_userName.text()
        self.password = self.lui.le_passWord.text()
        self.conn = sqlite3.connect("WeighBridge.db")
        self.c = self.conn.cursor()
        self.set = False
        cmd = "SELECT User, Password, Admin FROM T_UserAccountSettings"
        result = self.c.execute(cmd)
        for user,password,admin in result:

            if self.name == user and self.password == password and admin == '1':
                # self.ui = UI()
                self.set = True
                self.LoginUpdate.emit("1")

                self.main_window.close()

            elif self.name == user and self.password == password and admin == '0':
                self.set = True
                self.LoginUpdate.emit("0")
                self.main_window.close()

        if self.set == False:
            self.lui.le_userName.clear()
            self.lui.le_passWord.clear()
            self.showErrormsg("Error", "Type the correct information")
        self.c.close()
        self.conn.close()
    def showErrormsg(self,title,msg):
        QMessageBox.information(None,title,msg)



class UI():
    def __init__(self):
        ###  Ui setup
        self.main_window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.ui.stackedWidgetMain.setCurrentWidget(self.ui.Home)

        self.lws = LoginWindowcls()
        self.lws.LoginUpdate.connect(self.login)
        ### Declaring variables
        self.idList = []
        self.userList = []
        self.passwordList = []
        self.adminList = []
        self.activeList = []
        # self.t1 = threading.Thread(target=self.ShowDate)
        # self.t1.start()

        self.DownloadDataFromUserAccountTable()
        self.uniquenum = 0
        # ## Setting Up Main Page
        self.serial = Serial()
        self.serial.start()
        self.serial.WeightUpdate.connect(self.WeightDisplay)
        self.setTheField()
        self.mainPageTable()

        ### Setting up Parameter page
        self.setCancelSaveAddDelete()
        self.CodesLeDefault()
        # self.initialisation()
        # self.main_window.show()
    def initialisation(self):


        ### DataBase setup
        # self.connection = sqlite3.connect("WeighBridge.db")
        # self.cursor = self.connection.cursor()




        # self.ShowDate()

        timer = QTimer(self.main_window)

        # adding action to timer
        timer.timeout.connect(self.ShowDate)

        # update the timer every second
        timer.start(1000)
        self.ui.pb_home_Settings.clicked.connect(self.showSettings)

        self.ui.pb_home_report.setHidden(True)
        self.ui.pb_home_report.clicked.connect(self.showReport)

        self.ui.pb_home_ParameterSettings.setHidden(True)
        self.ui.pb_home_ParameterSettings.clicked.connect(self.showParameterSettings)

        self.ui.pb_home_VehicleEntry.clicked.connect(self.showVehicleEntry)
        self.ui.pb_home_VehicleReEntry.clicked.connect(self.showVehicleReEntry)
        self.setMainPageLogo()

        ## Setting up Vehicle Entry Page
        self.ui.pb_VehicleEntry_close.clicked.connect(self.showHome)
        self.ui.pb_VehicleEntry_entry.clicked.connect(self.Entry_Entry)
        self.ui.pb_VehicleEntry_cancel.clicked.connect(self.VehicleEntryCancel)
        self.ui.pb_VehicleEntry_save.clicked.connect(self.VehicleEntrySave)
        self.ui.pb_VehicleEntry_G_weight.clicked.connect(self.Entry_getGrossWeight)
        self.ui.pb_VehicleEntry_T_Weight.clicked.connect(self.Entry_getTareWeight)

        ## Setting up Vehicle ReEntry Page
        self.ui.pb_VehicleReEntry_close_3.clicked.connect(self.showHome)
        self.ui.pb_VehicleReEntry_entry_2.clicked.connect(self.Exit_Entry)
        self.ui.pb_VehicleReEntry_cancel_2.clicked.connect(self.Exit_Cancel)
        self.ui.pb_VehicleReEntry_serialNoSearch_3.clicked.connect(self.Exit_SnoSearch)
        self.ui.pb_VehicleReEntry_G_weight_3.clicked.connect(self.Exit_getGrossWeight)
        self.ui.pb_VehicleReEntry_T_Weight_3.clicked.connect(self.Exit_getTareWeight)
        self.ui.le_VehicleReEntry_netWeight_3.setReadOnly(True)
        self.ui.pb_VehicleReEntry_N_weight_3.clicked.connect(self.Exit_netWeight)
        self.ui.pb_VehicleReEntry_save_2.clicked.connect(self.Exit_Save)

        ## Setting up Parameter Settings Page


        self.ui.pb_Parameter_Close.clicked.connect(self.showHome)
        self.ui.pb_parameter_Code1Details.clicked.connect(self.showCode1Details)
        self.ui.pb_parameter_Code2Details.clicked.connect(self.showCode2Details)
        self.ui.pb_parameter_Code3Details.clicked.connect(self.showCode3Details)
        self.ui.pb_parameter_Code4Details.clicked.connect(self.showCode4Details)
        self.ui.pb_parameter_Code5Details.clicked.connect(self.showCode5Details)

        self.ui.pb_parameter_close_1.clicked.connect(self.showParameterSettingsMainPage)
        self.ui.pb_parameter_close_3.clicked.connect(self.showParameterSettingsMainPage)
        self.ui.pb_parameter_close_4.clicked.connect(self.showParameterSettingsMainPage)
        self.ui.pb_parameter_close_5.clicked.connect(self.showParameterSettingsMainPage)
        self.ui.pb_parameter_close_6.clicked.connect(self.showParameterSettingsMainPage)

        self.ui.pb_Parameter_Save.clicked.connect(self.CodeAndHeaderSettings)
        self.ui.pb_Parameter_Edit.clicked.connect(self.ParameterEdit)
        self.ui.pb_Parameter_Cancel.clicked.connect(self.ParameterCancel)
        self.ui.pb_Parameter_Save.setEnabled(False)

        ### Code 1 page
        self.ui.pb_parameter_edit_1.clicked.connect(self.Code1Edit)
        self.ui.pb_parameter_save_1.clicked.connect(self.Code1Save)
        self.ui.tableWidget_1.selectionModel().selectionChanged.connect(self.on_Code1TableSelectionChanged)
        self.ui.pb_parameter_cancel_1.clicked.connect(self.Code1Cancel)
        self.ui.pb_parameter_delete_1.clicked.connect(self.Code1Delete)
        self.ui.pb_parameter_create_1.clicked.connect(self.Code1Create)
        self.ui.pb_parameter_add.clicked.connect(self.Code1Add)

        ### Code 2 page
        self.ui.pb_parameter_edit_3.clicked.connect(self.Code2Edit)
        self.ui.pb_parameter_save_3.clicked.connect(self.Code2Save)
        self.ui.tableWidget_3.selectionModel().selectionChanged.connect(self.on_Code2TableSelectionChanged)
        self.ui.pb_parameter_cancel_3.clicked.connect(self.Code2Cancel)
        self.ui.pb_parameter_delete_3.clicked.connect(self.Code2Delete)
        self.ui.pb_parameter_create_3.clicked.connect(self.Code2Create)
        self.ui.pb_parameter_add_3.clicked.connect(self.Code2Add)

        ### Code 3 page
        self.ui.pb_parameter_edit_4.clicked.connect(self.Code3Edit)
        self.ui.pb_parameter_save_4.clicked.connect(self.Code3Save)
        self.ui.tableWidget_4.selectionModel().selectionChanged.connect(self.on_Code3TableSelectionChanged)
        self.ui.pb_parameter_cancel_4.clicked.connect(self.Code3Cancel)
        self.ui.pb_parameter_delete_4.clicked.connect(self.Code3Delete)
        self.ui.pb_parameter_create_4.clicked.connect(self.Code3Create)
        self.ui.pb_parameter_add_4.clicked.connect(self.Code3Add)

        ### Code 4 page
        self.ui.pb_parameter_edit_5.clicked.connect(self.Code4Edit)
        self.ui.pb_parameter_save_5.clicked.connect(self.Code4Save)
        self.ui.tableWidget_5.selectionModel().selectionChanged.connect(self.on_Code4TableSelectionChanged)
        self.ui.pb_parameter_cancel_5.clicked.connect(self.Code4Cancel)
        self.ui.pb_parameter_delete_5.clicked.connect(self.Code4Delete)
        self.ui.pb_parameter_create_5.clicked.connect(self.Code4Create)
        self.ui.pb_parameter_add_5.clicked.connect(self.Code4Add)
        ### Code 5 page
        self.ui.pb_parameter_edit_6.clicked.connect(self.Code5Edit)
        self.ui.pb_parameter_save_6.clicked.connect(self.Code5Save)
        self.ui.tableWidget_6.selectionModel().selectionChanged.connect(self.on_Code5TableSelectionChanged)
        self.ui.pb_parameter_cancel_6.clicked.connect(self.Code5Cancel)
        self.ui.pb_parameter_delete_6.clicked.connect(self.Code5Delete)
        self.ui.pb_parameter_create_6.clicked.connect(self.Code5Create)
        self.ui.pb_parameter_add_6.clicked.connect(self.Code5Add)
        ## Setting up Settings Page

        self.ui.stackedWidgetSettings.setCurrentWidget(self.ui.settingsMainPage)

        self.ui.pb_settings_close.clicked.connect(self.showHome)

        self.ui.pb_settings_search.clicked.connect(self.findPorts)
        self.ui.pb_CommPortSettings.clicked.connect(self.showCommPortSettings)
        self.ui.pb_HeaderSettings.clicked.connect(self.showHeaderSettings)
        self.ui.pb_UserAccountSettings.clicked.connect(self.showUserAccountSettings)

        self.ui.pb_UserAccountSettings.setHidden(True)
        self.ui.pb_HeaderSettings.setHidden(True)

        self.ui.pb_settings_comport_close.clicked.connect(self.showSettingsMainPage)
        self.ui.pb_settings_header_close.clicked.connect(self.showSettingsMainPage)
        self.ui.pb_settings_UserSettings_close.clicked.connect(self.showSettingsMainPage)

        ###Comm Port Settings
        self.defaultComboBoxValues()
        self.ui.pb_settings_Comm_save.clicked.connect(self.CommSettingsSave)

        ### User Account Settings
        self.ActiveGrp = QtWidgets.QButtonGroup()
        self.AdminGrp = QtWidgets.QButtonGroup()

        self.ActiveGrp.addButton(self.ui.rb_settings_activeYes)
        self.ActiveGrp.addButton(self.ui.rb_settings_activeNo)
        self.AdminGrp.addButton(self.ui.rb_settings_adminYes)
        self.AdminGrp.addButton(self.ui.rb_settings_adminNo)

        self.ui.tw_settings_users.setColumnWidth(0, 100)
        self.ui.tw_settings_users.setColumnWidth(1, 100)
        self.ui.tw_settings_users.setColumnWidth(2, 100)
        self.ui.tw_settings_users.setColumnWidth(3, 100)

        self.ui.le_settings_id.setReadOnly(True)
        self.ui.le_settings_username.setReadOnly(True)
        self.ui.le_settings_password.setReadOnly(True)
        self.ui.le_settings_newpassword.setReadOnly(True)
        self.ui.le_settings_retypepassword.setReadOnly(True)
        self.ui.rb_settings_activeYes.setCheckable(False)
        self.ui.rb_settings_activeNo.setCheckable(False)
        self.ui.rb_settings_adminYes.setCheckable(False)
        self.ui.rb_settings_adminNo.setCheckable(False)



        self.ui.pb_settings_edit.clicked.connect(self.UserSettingsEdit)
        self.ui.pb_settings_cancel.clicked.connect(self.UserSettingsCancel)
        self.ui.pb_settings_admin.clicked.connect(self.admin)
        self.ui.pb_settings_operator.clicked.connect(self.operator)
        self.ui.pb_settings_lcs.clicked.connect(self.lcs)
        self.ui.pb_settings_save.clicked.connect(self.addToT_UserAccountSettings)

        # self.default()
        # self.ui.pb_settings_save.clicked.connect(self.addToT_UserAccountSettings)

        ### Header settings
        self.ui.le_settings_title1.setReadOnly(True)
        self.ui.le_settings_title2.setReadOnly(True)
        self.ui.le_settings_title3.setReadOnly(True)
        self.setMainPageHeaders()

        self.ui.pb_settings_edit_2.clicked.connect(self.HeaderEdit)
        self.ui.pb_settings_cancel_2.clicked.connect(self.HeaderCancel)
        self.ui.pb_settings_save_2.clicked.connect(self.HeaderSave)
        self.ui.pb_settings_browse.clicked.connect(self.browseLogoImage)

        ## Setting up Report Page
        self.ui.pb_report_close.clicked.connect(self.showHome)
        self.ui.pb_report_OverallReport.clicked.connect(self.openOverallReport)
        self.ui.pb_Report_DailyReport.clicked.connect(self.openDailyReport)
        self.ui.pb_Report_MonthlyReport.clicked.connect(self.openMonthlyReport)
        self.ui.pb_report_dailyReportDateGo.clicked.connect(self.DailyReport)

        self.ui.pb_report_monthlyReportDateGo.clicked.connect(self.MonthlyReport)
        self.ui.pb_report_HeaderOk.clicked.connect(self.setSelectionHeader)
        self.ui.pb_report_CodeOk.clicked.connect(self.setSelectionCode)
        self.ui.pb_report_pdf.clicked.connect(self.createPdf)
        self.ui.pb_report_excel.clicked.connect(self.createExcel)
        self.setTheField()

    def showErrormsg(self,title,msg):
        QMessageBox.information(None,title,msg)
    def login(self,admin):

        self.Admin = admin
        self.initialisation()
        if self.Admin == "1":
            self.AdminUnMask()

        self.main_window.show()

    # Functions used in main page
    def showHome(self):
        self.ui.stackedWidgetMain.setCurrentWidget(self.ui.Home)
        self.setTheField()
        self.mainPageTable()
    def ShowDate(self):
        # while True:
        DateTime = datetime.now()
        date = DateTime.strftime("%d-%m-%y")
        #     time_ = DateTime.strftime("%H:%M:%S")
        self.ui.lb_DateDisplay.setText(str(date))
        #     self.ui.lb_TimeDisplay.setText(str(time_))
        current_time = QTime.currentTime()

        # converting QTime object to string
        label_time = current_time.toString('hh:mm:ss')

        # showing it to the label
        self.ui.lb_TimeDisplay.setText(label_time)

    def WeightDisplay(self, w):
        self.ui.lb_home_WeightDisplay.setText(w)
        self.ui.lb_VehicleEntry_weightDisplay.setText(w)
        self.ui.lb_VehicleReEntry_weightDisplay_3.setText(w)
        self.weight = w

    def mainPageTable(self):
        self.conn = sqlite3.connect("WeighBridge.db")
        self.c = self.conn.cursor()

        result = self.c.execute(
            """SELECT SerialNo,ReportDate,ReportTime, code1_no,code2_no,code3_no,code4_no,code5_no,header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry ORDER BY SerialNo DESC LIMIT 10"""
            )



        nwen = [1, 1, 1] + self.enableField[0:] + [1, 1, 1, 1]


        self.ui.tw_Home_Entry.setRowCount(0)
        self.ui.tw_Home_Entry.setColumnCount(len(self.titles))
        self.ui.tw_Home_Entry.setHorizontalHeaderLabels(self.titles)
        header = self.ui.tw_Home_Entry.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.ui.tw_Home_Entry.setSortingEnabled(True)
        for r_num, r_data in enumerate(result):

            self.ui.tw_Home_Entry.insertRow(r_num)
            r_data = list(r_data)
            row = []
            for i in range(len(r_data)):

                if nwen[i] == 1:
                    row.append(r_data[i])


            for i in range(len(row)):

                self.ui.tw_Home_Entry.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))

        self.c.close()
        self.conn.close()

    # Functions used in Vehicle Entry page
    def showVehicleEntry(self):
        self.ui.stackedWidgetMain.setCurrentWidget(self.ui.VehicleEntry)
        self.getLableNameFromDB()
        self.setParameters()
        self.addValuesInCodeComboBox()
        self.ui.pb_VehicleEntry_entry.setEnabled(True)
        self.Entry_disableCancelSaveAllLe()
        self.Entry_settingReadOnly()
        self.Entry_setInitialValues()

    def Entry_setInitialValues(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        r1 = self.c.execute("SELECT SerialNo FROM T_Entry")
        for data in r1:
            prevSerialNum = data[0]

        currSerialNo = int(prevSerialNum) + 1
        self.ui.le_VehicleEntry_serialNumber.setText(str(currSerialNo))
        self.c.close()
        self.conn.close()
        self.ui.le_VehicleEntry_grossWeight.clear()
        self.ui.le_VehicleEntry_netWeight.clear()
        self.ui.le_VehicleEntry_tareWeight.clear()
        self.ui.le_VehicleEntry_grossDate.clear()
        self.ui.le_VehicleEntry_grossTime.clear()
        self.ui.le_VehicleEntry_tareDate.clear()
        self.ui.le_VehicleEntry_tareTime.clear()
        self.ui.le_VehicleEntry_header5_supplierChalanNo.clear()
        self.ui.le_VehicleEntry_header4_msezDeliverNo.clear()
        self.ui.le_VehicleEntry_header3_count.clear()
        self.ui.le_VehicleEntry_header2_supervisorName.clear()
        self.ui.le_VehicleEntry_header1_vehicle.clear()




    def Entry_settingReadOnly(self):
        self.ui.le_VehicleEntry_grossDate.setReadOnly(True)
        self.ui.le_VehicleEntry_grossTime.setReadOnly(True)
        self.ui.le_VehicleEntry_tareDate.setReadOnly(True)
        self.ui.le_VehicleEntry_tareTime.setReadOnly(True)
        self.ui.le_VehicleEntry_serialNumber.setReadOnly(True)
        self.ui.le_VehicleEntry_grossWeight.setReadOnly(True)
        self.ui.le_VehicleEntry_tareWeight.setReadOnly(True)
        self.ui.le_VehicleEntry_netWeight.setReadOnly(True)

    def Entry_disableCancelSaveAllLe(self):
        self.ui.le_VehicleEntry_serialNumber.setEnabled(False)
        self.ui.le_VehicleEntry_grossWeight.setEnabled(False)
        self.ui.le_VehicleEntry_tareWeight.setEnabled(False)
        self.ui.le_VehicleEntry_netWeight.setEnabled(False)
        self.ui.le_VehicleEntry_header1_vehicle.setEnabled(False)
        self.ui.le_VehicleEntry_header2_supervisorName.setEnabled(False)
        self.ui.le_VehicleEntry_header3_count.setEnabled(False)
        self.ui.le_VehicleEntry_header4_msezDeliverNo.setEnabled(False)
        self.ui.le_VehicleEntry_header5_supplierChalanNo.setEnabled(False)
        # self.ui.le_VehicleEntry_code1.setEnabled(False)
        # self.ui.le_VehicleEntry_code2.setEnabled(False)
        # self.ui.le_VehicleEntry_name_6.setEnabled(False)
        self.ui.le_VehicleEntry_amount.setEnabled(False)

        self.ui.pb_VehicleEntry_save.setEnabled(False)
        self.ui.pb_VehicleEntry_cancel.setEnabled(False)
        self.ui.pb_VehicleEntry_G_weight.setEnabled(False)
        self.ui.pb_VehicleEntry_T_Weight.setEnabled(False)

    def Entry_Entry(self):
        self.ui.pb_VehicleEntry_save.setEnabled(True)
        self.ui.pb_VehicleEntry_cancel.setEnabled(True)
        self.ui.pb_VehicleEntry_entry.setEnabled(False)

        self.ui.le_VehicleEntry_serialNumber.setEnabled(True)


        self.ui.le_VehicleEntry_grossWeight.setEnabled(True)
        self.ui.le_VehicleEntry_tareWeight.setEnabled(True)
        self.ui.le_VehicleEntry_netWeight.setEnabled(True)
        self.ui.le_VehicleEntry_header1_vehicle.setEnabled(True)
        self.ui.le_VehicleEntry_header2_supervisorName.setEnabled(True)
        self.ui.le_VehicleEntry_header3_count.setEnabled(True)
        self.ui.le_VehicleEntry_header4_msezDeliverNo.setEnabled(True)
        self.ui.le_VehicleEntry_header5_supplierChalanNo.setEnabled(True)
        # self.ui.le_VehicleEntry_code1.setEnabled(True)
        # self.ui.le_VehicleEntry_code2.setEnabled(True)
        # self.ui.le_VehicleEntry_name_6.setEnabled(True)
        self.ui.le_VehicleEntry_amount.setEnabled(True)
        self.ui.pb_VehicleEntry_G_weight.setEnabled(True)
        self.ui.pb_VehicleEntry_T_Weight.setEnabled(True)

    def VehicleEntryCancel(self):
        self.ui.pb_VehicleEntry_entry.setEnabled(True)
        self.Entry_disableCancelSaveAllLe()


    def setParameters(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        result = self.c.execute("SELECT EN_ED, EX_ED FROM T_CodeAndHeader")
        for i,data in enumerate(result):
            en = data[0]
            ex = data[1]
            if i==0:
                continue
            elif i ==1 :
                if en:
                    self.ui.lb_VehicleEntry_code2_agentName.setHidden(False)
                    self.ui.combo_VehicleEntry_code2_agentName.setHidden(False)
                else:
                    self.ui.lb_VehicleEntry_code2_agentName.setHidden(True)
                    self.ui.combo_VehicleEntry_code2_agentName.setHidden(True)
                if ex:
                    self.ui.lb_VehicleReEntry_code2_agentName_3.setHidden(False)
                    self.ui.combo_VehicleReEntry_code2_agentName_3.setHidden(False)
                else:
                    self.ui.lb_VehicleReEntry_code2_agentName_3.setHidden(True)
                    self.ui.combo_VehicleReEntry_code2_agentName_3.setHidden(True)
            elif i ==2 :
                if en:
                    self.ui.lb_VehicleEntry_code3_placeOfLoading.setHidden(False)
                    self.ui.combo_VehicleEntry_code3_placeOfLoading.setHidden(False)
                else:
                    self.ui.lb_VehicleEntry_code3_placeOfLoading.setHidden(True)
                    self.ui.combo_VehicleEntry_code3_placeOfLoading.setHidden(True)
                if ex:
                    self.ui.lb_VehicleReEntry_code3_placeOfLoading_3.setHidden(False)
                    self.ui.combo_VehicleReEntry_code3_placeOfLoading_3.setHidden(False)
                else:
                    self.ui.lb_VehicleReEntry_code3_placeOfLoading_3.setHidden(True)
                    self.ui.combo_VehicleReEntry_code3_placeOfLoading_3.setHidden(True)
            elif i ==3 :
                if en:
                    self.ui.lb_VehicleEntry_code4_moistureValue.setHidden(False)
                    self.ui.combo_VehicleEntry_code4_moisturevalue.setHidden(False)
                else:
                    self.ui.lb_VehicleEntry_code4_moistureValue.setHidden(True)
                    self.ui.combo_VehicleEntry_code4_moisturevalue.setHidden(True)
                if ex:
                    self.ui.lb_VehicleReEntry_code4_moistureValue.setHidden(False)
                    self.ui.combo_VehicleReEntry_code4_moistureValue.setHidden(False)
                else:
                    self.ui.lb_VehicleReEntry_code4_moistureValue.setHidden(True)
                    self.ui.combo_VehicleReEntry_code4_moistureValue.setHidden(True)
            elif i ==4 :
                if en:
                    self.ui.lb_VehicleEntry_code5_size.setHidden(False)
                    self.ui.combo_VehicleEntry_code5_size.setHidden(False)
                else:
                    self.ui.lb_VehicleEntry_code5_size.setHidden(True)
                    self.ui.combo_VehicleEntry_code5_size.setHidden(True)
                if ex:
                    self.ui.lb_VehicleReEntry_code5_size.setHidden(False)
                    self.ui.combo_VehicleReEntry_code5_size.setHidden(False)
                else:
                    self.ui.lb_VehicleReEntry_code5_size.setHidden(True)
                    self.ui.combo_VehicleReEntry_code5_size.setHidden(True)
            elif i ==5 :
                continue
            elif i ==6 :
                if en:
                    self.ui.lb_VehicleEntry_header2_supervisorName.setHidden(False)
                    self.ui.le_VehicleEntry_header2_supervisorName.setHidden(False)
                else:
                    self.ui.lb_VehicleEntry_header2_supervisorName.setHidden(True)
                    self.ui.le_VehicleEntry_header2_supervisorName.setHidden(True)
                if ex:
                    self.ui.lb_VehicleReEntry_header2_supervisorName_3.setHidden(False)
                    self.ui.le_VehicleReEntry_header2_supervisorName_3.setHidden(False)
                else:
                    self.ui.lb_VehicleReEntry_header2_supervisorName_3.setHidden(True)
                    self.ui.le_VehicleReEntry_header2_supervisorName_3.setHidden(True)
            elif i ==7 :
                if en:
                    self.ui.lb_VehicleEntry_header3_count.setHidden(False)
                    self.ui.le_VehicleEntry_header3_count.setHidden(False)
                else:
                    self.ui.lb_VehicleEntry_header3_count.setHidden(True)
                    self.ui.le_VehicleEntry_header3_count.setHidden(True)
                if ex:
                    self.ui.lb_VehicleReEntry_header3_count_3.setHidden(False)
                    self.ui.le_VehicleReEntry_header3_count_3.setHidden(False)
                else:
                    self.ui.lb_VehicleReEntry_header3_count_3.setHidden(True)
                    self.ui.le_VehicleReEntry_header3_count_3.setHidden(True)
            elif i ==8 :
                if en:
                    self.ui.lb_VehicleEntry_header4_msezDeliverNo.setHidden(False)
                    self.ui.le_VehicleEntry_header4_msezDeliverNo.setHidden(False)
                else:
                    self.ui.lb_VehicleEntry_header4_msezDeliverNo.setHidden(True)
                    self.ui.le_VehicleEntry_header4_msezDeliverNo.setHidden(True)
                if ex:
                    self.ui.lb_VehicleReEntry_header4_msezDeliverNo_3.setHidden(False)
                    self.ui.le_VehicleReEntry_header4_msezDeliverNo_3.setHidden(False)
                else:
                    self.ui.lb_VehicleReEntry_header4_msezDeliverNo_3.setHidden(True)
                    self.ui.le_VehicleReEntry_header4_msezDeliverNo_3.setHidden(True)
            elif i ==9 :
                if en:
                    self.ui.lb_VehicleEntry_header5_supplierChalanNo.setHidden(False)
                    self.ui.le_VehicleEntry_header5_supplierChalanNo.setHidden(False)
                else:
                    self.ui.lb_VehicleEntry_header5_supplierChalanNo.setHidden(True)
                    self.ui.le_VehicleEntry_header5_supplierChalanNo.setHidden(True)
                if ex:
                    self.ui.lb_VehicleReEntry_header5_supplierChalanNo_3.setHidden(False)
                    self.ui.le_VehicleReEntry_header5_supplierChalanNo_3.setHidden(False)
                else:
                    self.ui.lb_VehicleReEntry_header5_supplierChalanNo_3.setHidden(True)
                    self.ui.le_VehicleReEntry_header5_supplierChalanNo_3.setHidden(True)



        self.c.close()
        self.conn.close()

    def VehicleEntrySave(self):
        self.ui.pb_VehicleEntry_entry.setEnabled(True)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        r1 = self.c.execute("SELECT SerialNo FROM T_Entry")
        for data in r1:
            prevSerialNum = data[0]

        currSerialNo = int(prevSerialNum) +1

        header1 = self.ui.le_VehicleEntry_header1_vehicle.text()
        header2 = self.ui.le_VehicleEntry_header2_supervisorName.text()
        header3 = self.ui.le_VehicleEntry_header3_count.text()
        header4 = self.ui.le_VehicleEntry_header4_msezDeliverNo.text()
        header5 = self.ui.le_VehicleEntry_header5_supplierChalanNo.text()
        code1 = self.ui.combo_VehicleEntry_code1_materia.currentText()
        code2 = self.ui.combo_VehicleEntry_code2_agentName.currentText()
        code3 = self.ui.combo_VehicleEntry_code3_placeOfLoading.currentText()
        code4 = self.ui.combo_VehicleEntry_code4_moisturevalue.currentText()
        code5 = self.ui.combo_VehicleEntry_code5_size.currentText()
        grosswt = self.ui.le_VehicleEntry_grossWeight.text()
        grossunit = self.ui.lb_vehicleEntry_unit_gross.text()
        grossdate = self.ui.le_VehicleEntry_grossDate.text()
        grosstime = self.ui.le_VehicleEntry_grossTime.text()
        tarewt = self.ui.le_VehicleEntry_tareWeight.text()
        tareunit = self.ui.lb_vehicleEntry_unit_tare.text()
        taredate = self.ui.le_VehicleEntry_tareDate.text()
        taretime = self.ui.le_VehicleEntry_tareTime.text()
        amount = self.ui.le_VehicleEntry_amount.text()


        if grosswt and grossdate and grosstime:
            rdate = grossdate
            rtime = grosstime
            a = (currSerialNo, header1, header2, header3, header4, header5, code1, code2, code3, code4, code5, grosswt, grossunit, grosstime, grossdate, amount, rdate, rtime)
            self.c.execute("INSERT INTO T_Entry (SerialNo,header1,header2,header3,header4,header5,code1_no,code2_no,code3_no,code4_no,code5_no,grossWt,grossUnit,grossTime,grossDate,Amount,ReportDate,ReportTime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           a)
            self.conn.commit()

        elif tarewt:
            rdate = taredate
            rtime = taretime
            a = (currSerialNo, header1, header2, header3, header4, header5, code1, code2, code3, code4, code5, tarewt,
                 tareunit, taretime, taredate, amount, rdate, rtime)
            self.c.execute(
                "INSERT INTO T_Entry (SerialNo,header1,header2,header3,header4,header5,code1_no,code2_no,code3_no,code4_no,code5_no,tareWt,tareUnit,tareTime,tareDate,Amount,ReportDate,ReportTime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                a)
            self.conn.commit()
        else:
            self.ui.pb_VehicleEntry_save.setEnabled(True)
            self.showErrormsg("error","enter the weight")

        filename = "Entry.txt"
        file = open(filename, 'w')
        s0 = ("SERIALNO", currSerialNo)
        s1 = (self.names[5], header1)
        s2 = (self.names[6], header2)
        s3 = (self.names[7], header3)
        s4 = (self.names[8], header4)
        s5 = (self.names[9], header5)
        s7 = (self.names[1], code2)
        s6 = (self.names[0], code1)
        s8 = (self.names[2], code3)
        s9 = (self.names[3], code4)
        s10 = (self.names[4], code5)
        s11 = ("GROSS WEIGHT", grosswt)
        s12 = ("TARE WEIGHT", tarewt)
        s13 = ("NET WEIGHT", " ")
        s14 = ("AMOUNT", " ")
        s = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14]
        en = [1] + self.enableField + [1, 1, 1, 1]
        lines = []
        for i in range(len(en)):
            if en[i] == 1:
                lines.append(s[i])

        file.write(tabulate(lines, tablefmt="grid"))
        file.close()

        self.Entry_disableCancelSaveAllLe()
        self.c.close()
        self.conn.close()
        self.Entry_setInitialValues()
        if self.ui.checkBox_VehicleEntry.isChecked():
            self.Printout(filename)

    def Printout(self,status):
        from escpos import printer
        from datetime import datetime

        file = open(status, 'r')
        line = file.readlines()

        p = printer.File("/dev/usb/lp0")

        p.set(align="CENTER", width=2)
        p.text("LCS Control pvt ltd \n\n")
        p.set(align="CENTER", width=1)
        p.text("date: " + str(datetime.now().strftime("%d:%m:%y")) + "            time: " + str(
            datetime.now().strftime("%H:%M")) + "\n\n")
        p.set(align="CENTER")
        p.text(status + "\n")
        p.text("----------------------------------------------\n")
        p.set(align="CENTER")
        for i, l in enumerate(line):
            p.text(l.strip() + "\n")
        p.text("----------------------------------------------\n")
        p.set(width=2)

        p.text("ThankYou! visit again!")
        p.cut()
        p.close()
        file.close()
        os.remove(status)

    def Entry_getGrossWeight(self):
        self.ui.pb_VehicleEntry_G_weight.setEnabled(False)
        self.ui.pb_VehicleEntry_T_Weight.setEnabled(False)
        try:
            self.ui.le_VehicleEntry_grossWeight.setText(self.weight)
        except:
            self.showErrormsg("Error","No weight values")
        DateTime = datetime.now()
        date = DateTime.strftime("%d-%m-%y")
        time_ = DateTime.strftime("%H:%M:%S")

        self.ui.le_VehicleEntry_grossDate.setText(str(date))

        self.ui.le_VehicleEntry_grossTime.setText(str(time_))

    def Entry_getTareWeight(self):
        self.ui.pb_VehicleEntry_G_weight.setEnabled(False)
        self.ui.pb_VehicleEntry_T_Weight.setEnabled(False)
        try:
            self.ui.le_VehicleEntry_tareWeight.setText(self.weight)
        except:
            self.showErrormsg("Error","No weight values")
        DateTime = datetime.now()
        date = DateTime.strftime("%d-%m-%y")
        time_ = DateTime.strftime("%H:%M:%S")

        self.ui.le_VehicleEntry_tareDate.setText(str(date))

        self.ui.le_VehicleEntry_tareTime.setText(str(time_))

    def getLableNameFromDB(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        names = []
        self.names = []
        ens = []
        exs = []
        result = self.c.execute("SELECT Name,EN_ED,EX_ED FROM T_CodeAndHeader")
        for name,en,ex in result:
            names.append(name)
            self.names.append(name)
            ens.append(en)
            exs.append(ex)
        self.ui.lb_VehicleEntry_code1_materia.setText(names[0])
        self.ui.lb_VehicleEntry_code2_agentName.setText(names[1])
        self.ui.lb_VehicleEntry_code3_placeOfLoading.setText(names[2])
        self.ui.lb_VehicleEntry_code4_moistureValue.setText(names[3])
        self.ui.lb_VehicleEntry_code5_size.setText(names[4])

        self.ui.lb_VehicleEntry_header1_vehicle.setText(names[5])
        self.ui.lb_VehicleEntry_header2_supervisorName.setText(names[6])
        self.ui.lb_VehicleEntry_header3_count.setText(names[7])
        self.ui.lb_VehicleEntry_header4_msezDeliverNo.setText(names[8])
        self.ui.lb_VehicleEntry_header5_supplierChalanNo.setText(names[9])

        self.ui.lb_VehicleReEntry_code1_materia_3.setText(names[0])
        self.ui.lb_VehicleReEntry_code2_agentName_3.setText(names[1])
        self.ui.lb_VehicleReEntry_code3_placeOfLoading_3.setText(names[2])
        self.ui.lb_VehicleReEntry_code4_moistureValue.setText(names[3])
        self.ui.lb_VehicleReEntry_code5_size.setText(names[4])

        self.ui.lb_VehicleReEntry_header1_vehicle_3.setText(names[5])
        self.ui.lb_VehicleReEntry_header2_supervisorName_3.setText(names[6])
        self.ui.lb_VehicleReEntry_header3_count_3.setText(names[7])
        self.ui.lb_VehicleReEntry_header4_msezDeliverNo_3.setText(names[8])
        self.ui.lb_VehicleReEntry_header5_supplierChalanNo_3.setText(names[9])


        self.c.close()
        self.conn.close()
    def addValuesInCodeComboBox(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        result1 = self.c.execute("SELECT Code FROM T_Code1")
        code1 = []
        code2 = []
        code3 = []
        code4 = []
        code5 = []
        for c1 in result1:
            code1.append(c1[0])
        result2 = self.c.execute("SELECT Code FROM T_Code2")
        for c2 in result2:
            code2.append(c2[0])
        result3 = self.c.execute("SELECT Code FROM T_Code3")
        for c3 in result3:
            code3.append(c3[0])
        result4 = self.c.execute("SELECT Code FROM T_Code4")
        for c4 in result4:
            code4.append(c4[0])
        result5 = self.c.execute("SELECT Code FROM T_Code5")
        for c5 in result5:
            code5.append(c5[0])
        self.ui.combo_VehicleEntry_code1_materia.addItems(code1)
        self.ui.combo_VehicleEntry_code2_agentName.addItems(code2)
        self.ui.combo_VehicleEntry_code3_placeOfLoading.addItems(code3)
        self.ui.combo_VehicleEntry_code4_moisturevalue.addItems(code4)
        self.ui.combo_VehicleEntry_code5_size.addItems(code5)

        self.ui.combo_VehicleReEntry_code1_materia_3.addItems(code1)
        self.ui.combo_VehicleReEntry_code2_agentName_3.addItems(code2)
        self.ui.combo_VehicleReEntry_code3_placeOfLoading_3.addItems(code3)
        self.ui.combo_VehicleReEntry_code4_moistureValue.addItems(code4)
        self.ui.combo_VehicleReEntry_code5_size.addItems(code5)

        self.c.close()
        self.conn.close()

    # Functions used in Vehicle ReEntry page
    def showVehicleReEntry(self):
        self.ui.stackedWidgetMain.setCurrentWidget(self.ui.VehicleExit)
        self.getLableNameFromDB()
        self.setParameters()
        self.addValuesInCodeComboBox()
        self.ui.pb_VehicleReEntry_entry_2.setEnabled(True)
        self.Exit_disableCancelSaveAllLe()
        self.Exit_settingReadOnly()
        self.Exit_setInitialValues()
        self.Exit_addVehicleComboBox()

    def Exit_addVehicleComboBox(self):
        self.conn = sqlite3.connect("WeighBridge.db")
        self.c = self.conn.cursor()
        vehicles = []
        result = self.c.execute("SELECT header1 FROM T_Entry")
        for v in result:
            vehicles.append(v[0])

        self.ui.combo_VehicleReEntry_vehicle.addItems(vehicles)
        self.c.close()
        self.conn.close()

    def Exit_disableCancelSaveAllLe(self):
        self.ui.le_VehicleReEntry_serialNumber_3.setEnabled(False)
        self.ui.le_VehicleReEntry_grossWeight_3.setEnabled(False)
        self.ui.le_VehicleReEntry_tareWeight_3.setEnabled(False)
        self.ui.le_VehicleReEntry_netWeight_3.setEnabled(False)
        self.ui.combo_VehicleReEntry_vehicle.setEnabled(False)
        self.ui.le_VehicleReEntry_header2_supervisorName_3.setEnabled(False)
        self.ui.le_VehicleReEntry_header3_count_3.setEnabled(False)
        self.ui.le_VehicleReEntry_header4_msezDeliverNo_3.setEnabled(False)
        self.ui.le_VehicleReEntry_header5_supplierChalanNo_3.setEnabled(False)
        # self.ui.le_VehicleEntry_code1.setEnabled(False)
        # self.ui.le_VehicleEntry_code2.setEnabled(False)
        # self.ui.le_VehicleEntry_name_6.setEnabled(False)
        self.ui.le_VehicleReEntry_amount_3.setEnabled(False)

        self.ui.pb_VehicleReEntry_save_2.setEnabled(False)
        self.ui.pb_VehicleReEntry_cancel_2.setEnabled(False)
        self.ui.pb_VehicleReEntry_G_weight_3.setEnabled(False)
        self.ui.pb_VehicleReEntry_T_Weight_3.setEnabled(False)

    def Exit_settingReadOnly(self):
        self.ui.le_VehicleReEntry_grossDate_2.setReadOnly(True)
        self.ui.le_VehicleReEntry_grossTime_2.setReadOnly(True)
        self.ui.le_VehicleReEntry_tareDate_2.setReadOnly(True)
        self.ui.le_VehicleReEntry_tareTime_2.setReadOnly(True)

        self.ui.le_VehicleReEntry_grossWeight_3.setReadOnly(True)
        self.ui.le_VehicleReEntry_tareWeight_3.setReadOnly(True)
        self.ui.le_VehicleReEntry_netWeight_3.setReadOnly(True)

    def Exit_setInitialValues(self):

        self.ui.le_VehicleReEntry_serialNumber_3.clear()
        self.ui.le_VehicleReEntry_grossWeight_3.clear()
        self.ui.le_VehicleReEntry_netWeight_3.clear()
        self.ui.le_VehicleReEntry_tareWeight_3.clear()
        self.ui.le_VehicleReEntry_grossDate_2.clear()
        self.ui.le_VehicleReEntry_grossTime_2.clear()
        self.ui.le_VehicleReEntry_tareDate_2.clear()
        self.ui.le_VehicleReEntry_tareTime_2.clear()
        self.ui.le_VehicleReEntry_header5_supplierChalanNo_3.clear()
        self.ui.le_VehicleReEntry_header4_msezDeliverNo_3.clear()
        self.ui.le_VehicleReEntry_header3_count_3.clear()
        self.ui.le_VehicleReEntry_header2_supervisorName_3.clear()



    def Exit_Entry(self):
        self.ui.pb_VehicleReEntry_save_2.setEnabled(True)
        self.ui.pb_VehicleReEntry_cancel_2.setEnabled(True)
        self.ui.pb_VehicleReEntry_entry_2.setEnabled(False)

        self.ui.le_VehicleReEntry_serialNumber_3.setEnabled(True)


        self.ui.le_VehicleReEntry_grossWeight_3.setEnabled(True)
        self.ui.le_VehicleReEntry_tareWeight_3.setEnabled(True)
        self.ui.le_VehicleReEntry_netWeight_3.setEnabled(True)
        self.ui.combo_VehicleReEntry_vehicle.setEnabled(True)
        self.ui.le_VehicleReEntry_header2_supervisorName_3.setEnabled(True)
        self.ui.le_VehicleReEntry_header3_count_3.setEnabled(True)
        self.ui.le_VehicleReEntry_header4_msezDeliverNo_3.setEnabled(True)
        self.ui.le_VehicleReEntry_header5_supplierChalanNo_3.setEnabled(True)
        # self.ui.le_VehicleEntry_code1.setEnabled(True)
        # self.ui.le_VehicleEntry_code2.setEnabled(True)
        # self.ui.le_VehicleEntry_name_6.setEnabled(True)
        self.ui.le_VehicleReEntry_amount_3.setEnabled(True)
        self.ui.pb_VehicleReEntry_G_weight_3.setEnabled(True)
        self.ui.pb_VehicleReEntry_T_Weight_3.setEnabled(True)


    def Exit_Cancel(self):
        self.ui.pb_VehicleReEntry_entry_2.setEnabled(True)
        self.Exit_disableCancelSaveAllLe()

    def Exit_SnoSearch(self):
        snum = self.ui.le_VehicleReEntry_serialNumber_3.text()
        # self.Exit_setInitialValues()
        flag = 1
        self.conn = sqlite3.connect("WeighBridge.db")
        self.c = self.conn.cursor()
        try:

            result = self.c.execute("SELECT * FROM T_Entry WHERE SerialNo=?",snum)

            for i,data in enumerate(result):
                print(data)
                flag = 0
                self.ui.le_VehicleReEntry_serialNumber_3.setText(data[0])
                self.ui.combo_VehicleReEntry_vehicle.setCurrentText(data[1])
                self.ui.le_VehicleReEntry_header2_supervisorName_3.setText(data[2])
                self.ui.le_VehicleReEntry_header3_count_3.setText(data[3])
                self.ui.le_VehicleReEntry_header4_msezDeliverNo_3.setText(data[4])
                self.ui.le_VehicleReEntry_header5_supplierChalanNo_3.setText(data[5])
                self.ui.combo_VehicleReEntry_code1_materia_3.setCurrentText(data[6])
                self.ui.combo_VehicleReEntry_code2_agentName_3.setCurrentText(data[7])
                self.ui.combo_VehicleReEntry_code3_placeOfLoading_3.setCurrentText(data[8])
                self.ui.combo_VehicleReEntry_code4_moistureValue.setCurrentText(data[9])
                self.ui.combo_VehicleReEntry_code5_size.setCurrentText(data[10])
                print("laki")
                if data[11]:
                    self.ui.pb_VehicleReEntry_G_weight_3.setEnabled(False)
                    self.ui.le_VehicleReEntry_grossWeight_3.setText(data[11])
                    self.ui.le_VehicleReEntry_grossTime_2.setText(data[13])
                    self.ui.le_VehicleReEntry_grossDate_2.setText(data[14])
                elif data[15]:
                    self.ui.pb_VehicleReEntry_T_Weight_3.setEnabled(False)
                    self.ui.le_VehicleReEntry_tareWeight_3.setText(data[15])
                    self.ui.le_VehicleReEntry_tareTime_2.setText(data[17])
                    self.ui.le_VehicleReEntry_tareDate_2.setText(data[18])
            if flag == 1:
                raise Exception()

        except :
            print("Error")
            self.showErrormsg("Warning","No data found")


        self.c.close()
        self.conn.close()

    def Exit_Save(self):
        self.ui.pb_VehicleReEntry_entry_2.setEnabled(True)
        self.conn = sqlite3.connect("WeighBridge.db")
        self.c = self.conn.cursor()

        serialno = self.ui.le_VehicleReEntry_serialNumber_3.text()
        header1 = self.ui.combo_VehicleReEntry_vehicle.currentText()
        header2 = self.ui.le_VehicleReEntry_header2_supervisorName_3.text()
        header3 = self.ui.le_VehicleReEntry_header3_count_3.text()
        header4 = self.ui.le_VehicleReEntry_header4_msezDeliverNo_3.text()
        header5 = self.ui.le_VehicleReEntry_header5_supplierChalanNo_3.text()
        code1 = self.ui.combo_VehicleReEntry_code1_materia_3.currentText()
        code2 = self.ui.combo_VehicleReEntry_code2_agentName_3.currentText()
        code3 = self.ui.combo_VehicleReEntry_code3_placeOfLoading_3.currentText()
        code4 = self.ui.combo_VehicleReEntry_code4_moistureValue.currentText()
        code5 = self.ui.combo_VehicleReEntry_code5_size.currentText()
        grosswt = self.ui.le_VehicleReEntry_grossWeight_3.text()
        grossunit = self.ui.lb_vehicleReEntry_unit_gross.text()
        grossdate = self.ui.le_VehicleReEntry_grossDate_2.text()
        grosstime = self.ui.le_VehicleReEntry_grossTime_2.text()
        tarewt = self.ui.le_VehicleReEntry_tareWeight_3.text()
        tareunit = self.ui.lb_vehicleReEntry_unit_tare.text()
        taredate = self.ui.le_VehicleReEntry_tareDate_2.text()
        taretime = self.ui.le_VehicleReEntry_tareTime_2.text()
        netwt = self.ui.le_VehicleReEntry_netWeight_3.text()
        amount = self.ui.le_VehicleReEntry_amount_3.text()
        try:
            if netwt and amount:
                values = (
                header1, header2, header3, header4, header5, code1, code2, code3, code4, code5, grosswt, grossunit, grosstime, grossdate,
                tarewt, tareunit, taretime, taredate, netwt, amount, self.reportdate, self.reportTime, serialno)
                self.c.execute(
                    "UPDATE T_Entry SET header1=?,header2=?,header3=?,header4=?,header5=?,code1_no=?,code2_no=?,code3_no=?,code4_no=?,code5_no=?,grossWt=?,grossUnit=?,grossTime=?,grossDate=?,tareWt=?,tareUnit=?,tareTime=?,tareDate=?,netWt=?,Amount=?,ReportDate=?,ReportTime=? WHERE SerialNo=?",
                    values)
                self.conn.commit()

            elif not netwt:
                self.showErrormsg("Error","Enter Net Weight")
            elif not amount:
                self.showErrormsg("Error","Enter Amount")
        except:
            pass

        filename = "Re-entry.txt"
        file = open(filename,'w')
        s0 = ("SERIALNO",serialno)
        s1 = (self.names[5], header1)
        s2 = (self.names[6], header2)
        s3 = (self.names[7], header3)
        s4 = (self.names[8], header4)
        s5 = (self.names[9], header5)
        s7 = (self.names[1], code2)
        s6 = (self.names[0], code1)
        s8 = (self.names[2], code3)
        s9 = (self.names[3], code4)
        s10 = (self.names[4], code5)
        s11 = ("GROSS WEIGHT", grosswt)
        s12 = ("TARE WEIGHT", tarewt)
        s13 = ("NET WEIGHT", netwt)
        s14 = ("AMOUNT", amount)
        s = [s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14]
        en = [1] + self.enableField + [1,1,1,1]
        lines = []
        for i in range(len(en)):
            if en[i] == 1:

                lines.append(s[i])

        file.write(tabulate(lines,tablefmt="grid"))
        file.close()
        self.c.close()
        self.conn.close()
        self.Exit_disableCancelSaveAllLe()
        self.Exit_setInitialValues()
        if self.ui.VehicleReEntry_checkBox_3.isChecked():
            self.Printout(filename)

    def Exit_getGrossWeight(self):
        self.ui.pb_VehicleReEntry_G_weight_3.setEnabled(False)
        self.ui.pb_VehicleReEntry_T_Weight_3.setEnabled(False)
        try:
            self.ui.le_VehicleReEntry_grossWeight_3.setText(self.weight)
        except:
            self.showErrormsg("Error","No weight values")
        DateTime = datetime.now()
        date = DateTime.strftime("%d-%m-%y")
        time_ = DateTime.strftime("%H:%M:%S")
        self.reportdate = date
        self.reportTime = time_
        self.ui.le_VehicleReEntry_grossDate_2.setText(str(date))

        self.ui.le_VehicleReEntry_grossTime_2.setText(str(time_))

    def Exit_getTareWeight(self):
        self.ui.pb_VehicleReEntry_G_weight_3.setEnabled(False)
        self.ui.pb_VehicleReEntry_T_Weight_3.setEnabled(False)
        try:
            self.ui.le_VehicleReEntry_tareWeight_3.setText(self.weight)
        except:
            self.showErrormsg("Error","No weight values")
        DateTime = datetime.now()
        date = DateTime.strftime("%d-%m-%y")
        time_ = DateTime.strftime("%H:%M:%S")
        self.reportdate = date
        self.reportTime = time_
        self.ui.le_VehicleReEntry_tareDate_2.setText(str(date))

        self.ui.le_VehicleReEntry_tareTime_2.setText(str(time_))

    def Exit_netWeight(self):
        gw = self.ui.le_VehicleReEntry_grossWeight_3.text()
        tw = self.ui.le_VehicleReEntry_tareWeight_3.text()
        if gw and tw :
            nw = float(tw)-float(gw)
            self.ui.le_VehicleReEntry_netWeight_3.setText(str(nw))
        else:
            self.showErrormsg("Error","Enter both weights")


    # Functions used in Parameter Settings page
    def showParameterSettings(self):
        self.ui.stackedWidgetParameterSettings.setCurrentWidget(self.ui.ParameterSettingsMainPage)
        self.ui.stackedWidgetMain.setCurrentWidget(self.ui.ParameterSettings)

        self.setLePlaceHolderValues()
        self.setRead()
    def CodesLeDefault(self):
        self.ui.le_parameter_code_1.setEnabled(False)
        self.ui.le_parameter_name_1.setEnabled(False)
        self.ui.le_parameter_code_3.setEnabled(False)
        self.ui.le_parameter_name_3.setEnabled(False)
        self.ui.le_parameter_code_4.setEnabled(False)
        self.ui.le_parameter_name_4.setEnabled(False)
        self.ui.le_parameter_code_5.setEnabled(False)
        self.ui.le_parameter_name_5.setEnabled(False)
        self.ui.le_parameter_code_6.setEnabled(False)
        self.ui.le_parameter_name_6.setEnabled(False)


    def showParameterSettingsMainPage(self):
        self.ui.stackedWidgetParameterSettings.setCurrentWidget(self.ui.ParameterSettingsMainPage)
        self.CodesLeDefault()

    def setCancelSaveAddDelete(self):
        self.ui.pb_Parameter_Save.setEnabled(False)
        self.ui.pb_Parameter_Cancel.setEnabled(False)
        self.ui.pb_parameter_save_1.setEnabled(False)
        self.ui.pb_parameter_save_3.setEnabled(False)
        self.ui.pb_parameter_save_4.setEnabled(False)
        self.ui.pb_parameter_save_5.setEnabled(False)
        self.ui.pb_parameter_save_6.setEnabled(False)
        self.ui.pb_parameter_cancel_1.setEnabled(False)
        self.ui.pb_parameter_cancel_3.setEnabled(False)
        self.ui.pb_parameter_cancel_4.setEnabled(False)
        self.ui.pb_parameter_cancel_5.setEnabled(False)
        self.ui.pb_parameter_cancel_6.setEnabled(False)
        self.ui.pb_parameter_add.setEnabled(False)
        self.ui.pb_parameter_add_3.setEnabled(False)
        self.ui.pb_parameter_add_4.setEnabled(False)
        self.ui.pb_parameter_add_5.setEnabled(False)
        self.ui.pb_parameter_add_6.setEnabled(False)
        self.ui.pb_parameter_delete_1.setEnabled(True)
        self.ui.pb_parameter_delete_3.setEnabled(True)
        self.ui.pb_parameter_delete_4.setEnabled(True)
        self.ui.pb_parameter_delete_5.setEnabled(True)
        self.ui.pb_parameter_delete_6.setEnabled(True)


        ### Code 1
    def showCode1Details(self):
        self.ui.stackedWidgetParameterSettings.setCurrentWidget(self.ui.Code1Details)
        self.insertIntoCod1Table()
        self.ui.tableWidget_1.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.tableWidget_1.selectRow(0)
        self.on_Code1TableSelectionChanged()

        ### Code 2
    def showCode2Details(self):
        self.ui.stackedWidgetParameterSettings.setCurrentWidget(self.ui.Code2Details)
        self.insertIntoCod2Table()
        self.ui.tableWidget_3.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.tableWidget_3.selectRow(0)
        self.on_Code2TableSelectionChanged()

        ### code 3
    def showCode3Details(self):

        self.ui.stackedWidgetParameterSettings.setCurrentWidget(self.ui.Code3Details)
        self.insertIntoCod3Table()
        self.ui.tableWidget_4.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.tableWidget_4.selectRow(0)
        self.on_Code3TableSelectionChanged()

        ### Code 4
    def showCode4Details(self):
        self.ui.stackedWidgetParameterSettings.setCurrentWidget(self.ui.Code4Details)
        self.insertIntoCod4Table()
        self.ui.tableWidget_5.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.tableWidget_5.selectRow(0)
        self.on_Code4TableSelectionChanged()

        ### Code 5
    def showCode5Details(self):
        self.ui.stackedWidgetParameterSettings.setCurrentWidget(self.ui.Code5Details)
        self.insertIntoCod5Table()
        self.ui.tableWidget_6.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.tableWidget_6.selectRow(0)
        self.on_Code5TableSelectionChanged()
    def setRead(self):
        self.ui.le_parameterMain_Code1.setReadOnly(True)
        self.ui.le_parameterMain_Code2.setReadOnly(True)
        self.ui.le_parameterMain_Code3.setReadOnly(True)
        self.ui.le_parameterMain_Code4.setReadOnly(True)
        self.ui.le_parameterMain_Code5.setReadOnly(True)

        self.ui.le_parameterMain_Header1.setReadOnly(True)
        self.ui.le_parameterMain_Header2.setReadOnly(True)
        self.ui.le_parameterMain_Header3.setReadOnly(True)
        self.ui.le_parameterMain_Header4.setReadOnly(True)
        self.ui.le_parameterMain_Header5.setReadOnly(True)

        self.ui.cb_parameter_VehicleEntry_Code2.setCheckable(False)
        self.ui.cb_parameter_VehicleEntry_Code3.setCheckable(False)
        self.ui.cb_parameter_VehicleEntry_Code4.setCheckable(False)
        self.ui.cb_parameter_VehicleEntry_Code5.setCheckable(False)

        self.ui.cb_parameter_VehicleExit_Code2.setCheckable(False)
        self.ui.cb_parameter_VehicleExit_Code3.setCheckable(False)
        self.ui.cb_parameter_VehicleExit_Code4.setCheckable(False)
        self.ui.cb_parameter_VehicleExit_Code5.setCheckable(False)

        self.ui.cb_parameter_VehicleEntry_header2.setCheckable(False)
        self.ui.cb_parameter_VehicleEntry_header3.setCheckable(False)
        self.ui.cb_parameter_VehicleEntry_header4.setCheckable(False)
        self.ui.cb_parameter_VehicleEntry_header5.setCheckable(False)

        self.ui.cb_parameter_VehicleExit_header2.setCheckable(False)
        self.ui.cb_parameter_VehicleExit_header3.setCheckable(False)
        self.ui.cb_parameter_VehicleExit_header4.setCheckable(False)
        self.ui.cb_parameter_VehicleExit_header5.setCheckable(False)

        self.ui.cb_parameter_Amount.setCheckable(False)
        self.ui.cb_parameter_GunnyBag.setCheckable(False)
        self.ui.cb_parameterDateTime.setCheckable(False)
        self.ui.rb_parameter_kg.setCheckable(False)
        self.ui.rb_parameter_Tonne.setCheckable(False)
    def setWrite(self):
        self.ui.le_parameterMain_Code1.setReadOnly(False)
        self.ui.le_parameterMain_Code2.setReadOnly(False)
        self.ui.le_parameterMain_Code3.setReadOnly(False)
        self.ui.le_parameterMain_Code4.setReadOnly(False)
        self.ui.le_parameterMain_Code5.setReadOnly(False)

        self.ui.le_parameterMain_Header1.setReadOnly(False)
        self.ui.le_parameterMain_Header2.setReadOnly(False)
        self.ui.le_parameterMain_Header3.setReadOnly(False)
        self.ui.le_parameterMain_Header4.setReadOnly(False)
        self.ui.le_parameterMain_Header5.setReadOnly(False)

        self.ui.cb_parameter_VehicleEntry_Code2.setCheckable(True)
        self.ui.cb_parameter_VehicleEntry_Code3.setCheckable(True)
        self.ui.cb_parameter_VehicleEntry_Code4.setCheckable(True)
        self.ui.cb_parameter_VehicleEntry_Code5.setCheckable(True)

        self.ui.cb_parameter_VehicleExit_Code2.setCheckable(True)
        self.ui.cb_parameter_VehicleExit_Code3.setCheckable(True)
        self.ui.cb_parameter_VehicleExit_Code4.setCheckable(True)
        self.ui.cb_parameter_VehicleExit_Code5.setCheckable(True)

        self.ui.cb_parameter_VehicleEntry_header2.setCheckable(True)
        self.ui.cb_parameter_VehicleEntry_header3.setCheckable(True)
        self.ui.cb_parameter_VehicleEntry_header4.setCheckable(True)
        self.ui.cb_parameter_VehicleEntry_header5.setCheckable(True)

        self.ui.cb_parameter_VehicleExit_header2.setCheckable(True)
        self.ui.cb_parameter_VehicleExit_header3.setCheckable(True)
        self.ui.cb_parameter_VehicleExit_header4.setCheckable(True)
        self.ui.cb_parameter_VehicleExit_header5.setCheckable(True)

        self.ui.cb_parameter_Amount.setCheckable(True)
        self.ui.cb_parameter_GunnyBag.setCheckable(True)
        self.ui.cb_parameterDateTime.setCheckable(True)
        self.ui.rb_parameter_kg.setCheckable(True)
        self.ui.rb_parameter_Tonne.setCheckable(True)

    def ParameterEdit(self):

        self.setWrite()
        self.setCurrentCheckBoxValues()
        self.ui.pb_Parameter_Save.setEnabled(True)
        self.ui.pb_Parameter_Cancel.setEnabled(True)
    def ParameterCancel(self):
        self.setRead()
        self.ui.pb_Parameter_Save.setEnabled(False)

    def setLePlaceHolderValues(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        names = []

        result = self.c.execute("SELECT Name FROM T_CodeAndHeader")
        for name in result:
            names.append(str(name[0]))
        self.ui.le_parameterMain_Code1.setPlaceholderText(names[0])
        self.ui.le_parameterMain_Code2.setPlaceholderText(names[1])
        self.ui.le_parameterMain_Code3.setPlaceholderText(names[2])
        self.ui.le_parameterMain_Code4.setPlaceholderText(names[3])
        self.ui.le_parameterMain_Code5.setPlaceholderText(names[4])

        self.ui.le_parameterMain_Header1.setPlaceholderText(names[5])
        self.ui.le_parameterMain_Header2.setPlaceholderText(names[6])
        self.ui.le_parameterMain_Header3.setPlaceholderText(names[7])
        self.ui.le_parameterMain_Header4.setPlaceholderText(names[8])
        self.ui.le_parameterMain_Header5.setPlaceholderText(names[9])

        self.c.close()
        self.conn.close()

    def setCurrentCheckBoxValues(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        result = self.c.execute("SELECT EN_ED, EX_ED FROM T_CodeAndHeader")
        for i,data in enumerate(result):
            en = data[0]
            ex = data[1]
            if i==0:
                continue
            elif i ==1 :
                if en:self.ui.cb_parameter_VehicleEntry_Code2.setChecked(True)
                else:self.ui.cb_parameter_VehicleEntry_Code2.setChecked(False)
                if ex:self.ui.cb_parameter_VehicleExit_Code2.setChecked(True)
                else:self.ui.cb_parameter_VehicleExit_Code2.setChecked(False)
            elif i ==2 :
                if en:self.ui.cb_parameter_VehicleEntry_Code3.setChecked(True)
                else:self.ui.cb_parameter_VehicleEntry_Code3.setChecked(False)
                if ex:self.ui.cb_parameter_VehicleExit_Code3.setChecked(True)
                else:self.ui.cb_parameter_VehicleExit_Code3.setChecked(False)
            elif i ==3 :
                if en:self.ui.cb_parameter_VehicleEntry_Code4.setChecked(True)
                else:self.ui.cb_parameter_VehicleEntry_Code4.setChecked(False)
                if ex:self.ui.cb_parameter_VehicleExit_Code4.setChecked(True)
                else:self.ui.cb_parameter_VehicleExit_Code4.setChecked(False)
            elif i ==4 :
                if en:self.ui.cb_parameter_VehicleEntry_Code5.setChecked(True)
                else:self.ui.cb_parameter_VehicleEntry_Code5.setChecked(False)
                if ex:self.ui.cb_parameter_VehicleExit_Code5.setChecked(True)
                else:self.ui.cb_parameter_VehicleExit_Code5.setChecked(False)
            elif i ==5 :
                continue
            elif i ==6 :
                if en:self.ui.cb_parameter_VehicleEntry_header2.setChecked(True)
                else:self.ui.cb_parameter_VehicleEntry_header2.setChecked(False)
                if ex:self.ui.cb_parameter_VehicleExit_header2.setChecked(True)
                else:self.ui.cb_parameter_VehicleExit_header2.setChecked(False)
            elif i ==7 :
                if en:self.ui.cb_parameter_VehicleEntry_header3.setChecked(True)
                else:self.ui.cb_parameter_VehicleEntry_header3.setChecked(False)
                if ex:self.ui.cb_parameter_VehicleExit_header3.setChecked(True)
                else:self.ui.cb_parameter_VehicleExit_header3.setChecked(False)
            elif i ==8 :
                if en:self.ui.cb_parameter_VehicleEntry_header4.setChecked(True)
                else:self.ui.cb_parameter_VehicleEntry_header4.setChecked(False)
                if ex:self.ui.cb_parameter_VehicleExit_header4.setChecked(True)
                else:self.ui.cb_parameter_VehicleExit_header4.setChecked(False)
            elif i ==9 :
                if en:self.ui.cb_parameter_VehicleEntry_header5.setChecked(True)
                else:self.ui.cb_parameter_VehicleEntry_header5.setChecked(False)
                if ex:self.ui.cb_parameter_VehicleExit_header5.setChecked(True)
                else:self.ui.cb_parameter_VehicleExit_header5.setChecked(False)



        self.c.close()
        self.conn.close()
    def CodeAndHeaderSettings(self):
        self.ui.pb_Parameter_Save.setEnabled(False)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        self.EntryExitCheckbox()
        code1 = self.ui.le_parameterMain_Code1.text()
        code2 = self.ui.le_parameterMain_Code2.text()
        code3 = self.ui.le_parameterMain_Code3.text()
        code4 = self.ui.le_parameterMain_Code4.text()
        code5 = self.ui.le_parameterMain_Code5.text()

        headers = {
        "header1" : self.ui.le_parameterMain_Header1.text(),
        "header2" : self.ui.le_parameterMain_Header2.text(),
        "header3" : self.ui.le_parameterMain_Header3.text(),
        "header4" : self.ui.le_parameterMain_Header4.text(),
        "header5" : self.ui.le_parameterMain_Header5.text()
        }


        codes = {"code1":code1, "code2":code2, "code3":code3, "code4":code4, "code5":code5}

        for i in range(1,6):
            cd = f"code{i}"
            if len(codes[cd])!= 0:
                # print(codes[cd])
                self.c.execute("UPDATE T_CodeAndHeader SET Name=?, EN_ED=?, EX_ED=? WHERE Type=?",(codes[cd].upper(),self.en_ed[cd],self.ex_ed[cd],str(cd)))
                self.conn.commit()
            else:
                self.c.execute("UPDATE T_CodeAndHeader SET EN_ED=?, EX_ED=? WHERE Type=?",
                               ( self.en_ed[cd], self.ex_ed[cd], str(cd)))
                self.conn.commit()
        for j in range(1,6):
            hd = f"header{j}"
            if len(headers[hd])!= 0:
                self.c.execute("UPDATE T_CodeAndHeader SET Name=?, EN_ED=?, EX_ED=? WHERE Type=?",(headers[hd].upper(),self.en_hd_ed[hd],self.ex_hd_ed[hd],str(hd)))
                self.conn.commit()
            else:
                self.c.execute("UPDATE T_CodeAndHeader SET EN_ED=?, EX_ED=? WHERE Type=?",
                               (self.en_hd_ed[hd], self.ex_hd_ed[hd], str(hd)))
                self.conn.commit()

        self.setRead()
        self.showErrormsg("","Updated")
        self.c.close()
        self.conn.close()


    def EntryExitCheckbox(self):
        self.en_ed = {
            "code1": 1,
            "code2": 1 if self.ui.cb_parameter_VehicleEntry_Code2.isChecked() else 0,
            "code3": 1 if self.ui.cb_parameter_VehicleEntry_Code3.isChecked() else 0,
            "code4": 1 if self.ui.cb_parameter_VehicleEntry_Code4.isChecked() else 0,
            "code5": 1 if self.ui.cb_parameter_VehicleEntry_Code5.isChecked() else 0
        }
        self.ex_ed = {
            "code1": 1,
            "code2": 1 if self.ui.cb_parameter_VehicleExit_Code2.isChecked() else 0,
            "code3": 1 if self.ui.cb_parameter_VehicleExit_Code3.isChecked() else 0,
            "code4": 1 if self.ui.cb_parameter_VehicleExit_Code4.isChecked() else 0,
            "code5": 1 if self.ui.cb_parameter_VehicleExit_Code5.isChecked() else 0
        }
        self.en_hd_ed = {
            "header1": 1,
            "header2": 1 if self.ui.cb_parameter_VehicleEntry_header2.isChecked() else 0,
            "header3": 1 if self.ui.cb_parameter_VehicleEntry_header3.isChecked() else 0,
            "header4": 1 if self.ui.cb_parameter_VehicleEntry_header4.isChecked() else 0,
            "header5": 1 if self.ui.cb_parameter_VehicleEntry_header5.isChecked() else 0
        }
        self.ex_hd_ed = {
            "header1": 1,
            "header2": 1 if self.ui.cb_parameter_VehicleExit_header2.isChecked() else 0,
            "header3": 1 if self.ui.cb_parameter_VehicleExit_header3.isChecked() else 0,
            "header4": 1 if self.ui.cb_parameter_VehicleExit_header4.isChecked() else 0,
            "header5": 1 if self.ui.cb_parameter_VehicleExit_header5.isChecked() else 0
        }


        # print(self.en_ed)
        # print(self.ex_ed)


        ### Code 1 Page
    def Code1Edit(self):
        self.ui.pb_parameter_edit_1.setEnabled(False)
        self.ui.pb_parameter_create_1.setEnabled(False)
        self.ui.pb_parameter_save_1.setEnabled(True)
        self.ui.pb_parameter_cancel_1.setEnabled(True)
        self.ui.le_parameter_code_1.setEnabled(True)
        self.ui.le_parameter_name_1.setEnabled(True)
        self.ui.le_parameter_name_1.clear()
        self.prevCode1code = self.ui.le_parameter_code_1.text()


    def Code1Cancel(self):
        self.CodesLeDefault()
        self.setCancelSaveAddDelete()
        self.ui.pb_parameter_create_1.setEnabled(True)
        self.ui.pb_parameter_create_1.setEnabled(True)

    def Code1Save(self):
        self.setCancelSaveAddDelete()
        self.ui.pb_parameter_edit_1.setEnabled(True)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        code = self.ui.le_parameter_code_1.text()
        name = self.ui.le_parameter_name_1.text()
        self.c.execute("UPDATE T_Code1 SET Code=?,Name=? WHERE Code=?",(code,name,self.prevCode1code))
        self.conn.commit()
        ## Left Here
        self.c.close()
        self.conn.close()

        row = self.ui.tableWidget_1.currentRow()

        self.ui.tableWidget_1.setItem(row,0,QtWidgets.QTableWidgetItem(str(code)))
        self.ui.tableWidget_1.setItem(row, 1, QtWidgets.QTableWidgetItem(str(name)))

    def on_Code1TableSelectionChanged(self):
        row = self.ui.tableWidget_1.currentRow()  # Index of Row
        firstColumnInRow = self.ui.tableWidget_1.item(row, 0)  # returns QTableWidgetItem
        SecondColumnInRow = self.ui.tableWidget_1.item(row, 1)
        self.Code1code = firstColumnInRow.text()
        # print("here ",self.Code1code)
        # print("row ",row)
        Code1name = SecondColumnInRow.text()
        self.ui.le_parameter_code_1.setText(self.Code1code)
        self.ui.le_parameter_name_1.setText(Code1name)
        self.ui.pb_parameter_edit_1.setEnabled(True)
        self.Code1Cancel()


    def insertIntoCod1Table(self):
        if self.ui.tableWidget_1.rowCount() == 0:
            self.conn = sqlite3.connect('WeighBridge.db')
            self.c = self.conn.cursor()

            result = self.c.execute("SELECT Code,Name FROM T_Code1")
            self.ui.tableWidget_1.setRowCount(0)
            self.ui.tableWidget_1.setHorizontalHeaderLabels(['Code','Name'])
            header = self.ui.tableWidget_1.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            for r_num, r_data in enumerate(result):
                self.ui.tableWidget_1.insertRow(r_num)
                for c_num, c_data in enumerate(r_data):
                    self.ui.tableWidget_1.setItem(r_num, c_num, QtWidgets.QTableWidgetItem(str(c_data)))
            # self.ui.tableWidget_1.setSelectionMode(QAbstractItemView.MultiSelection)

            self.c.close()
            self.conn.close()
        else:
            pass

    def Code1Delete(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()


        self.c.execute("DELETE FROM T_Code1 WHERE Code=?",(self.Code1code,))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        self.ui.tableWidget_1.removeRow(self.ui.tableWidget_1.currentRow())
    def Code1Create(self):
        self.ui.pb_parameter_add.setEnabled(True)
        self.ui.pb_parameter_edit_1.setEnabled(False)
        self.ui.pb_parameter_create_1.setEnabled(False)
        self.ui.pb_parameter_save_1.setEnabled(False)
        self.ui.pb_parameter_delete_1.setEnabled(False)
        self.ui.le_parameter_code_1.setEnabled(True)
        self.ui.le_parameter_name_1.setEnabled(True)
        self.ui.le_parameter_name_1.clear()
        self.ui.le_parameter_code_1.clear()

    def Code1Add(self):
        self.ui.pb_parameter_create_1.setEnabled(True)
        self.ui.pb_parameter_add.setEnabled(False)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        code = self.ui.le_parameter_code_1.text()
        name = self.ui.le_parameter_name_1.text()

        self.c.execute("INSERT INTO T_Code2 (Code,Name) VALUES (?,?) ", (code,name))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        row = self.ui.tableWidget_1.rowCount()
        self.ui.tableWidget_1.insertRow(row)
        self.ui.tableWidget_1.setItem(row,0,QtWidgets.QTableWidgetItem(str(code)))
        self.ui.tableWidget_1.setItem(row, 1, QtWidgets.QTableWidgetItem(str(name)))

        ### Code 2 page

    def Code2Edit(self):
        self.ui.pb_parameter_edit_3.setEnabled(False)
        self.ui.pb_parameter_create_3.setEnabled(False)
        self.ui.pb_parameter_save_3.setEnabled(True)
        self.ui.pb_parameter_cancel_3.setEnabled(True)
        self.ui.le_parameter_code_3.setEnabled(True)
        self.ui.le_parameter_name_3.setEnabled(True)
        self.ui.le_parameter_name_3.clear()
        self.prevCode2code = self.ui.le_parameter_code_3.text()

    def Code2Cancel(self):
        self.CodesLeDefault()
        self.setCancelSaveAddDelete()
        self.ui.pb_parameter_create_3.setEnabled(True)
        self.ui.pb_parameter_create_3.setEnabled(True)

    def Code2Save(self):
        self.setCancelSaveAddDelete()
        self.ui.pb_parameter_edit_3.setEnabled(True)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        code = self.ui.le_parameter_code_3.text()
        name = self.ui.le_parameter_name_3.text()
        self.c.execute("UPDATE T_Code2 SET Code=?,Name=? WHERE Code=?", (code, name, self.prevCode2code))
        self.conn.commit()
        ## Left Here
        self.c.close()
        self.conn.close()

        row = self.ui.tableWidget_3.currentRow()

        self.ui.tableWidget_3.setItem(row, 0, QtWidgets.QTableWidgetItem(str(code)))
        self.ui.tableWidget_3.setItem(row, 1, QtWidgets.QTableWidgetItem(str(name)))

    def on_Code2TableSelectionChanged(self):
        row = self.ui.tableWidget_3.currentRow()  # Index of Row
        firstColumnInRow = self.ui.tableWidget_3.item(row, 0)  # returns QTableWidgetItem
        SecondColumnInRow = self.ui.tableWidget_3.item(row, 1)
        self.Code2code = firstColumnInRow.text()
        Code2name = SecondColumnInRow.text()
        self.ui.le_parameter_code_3.setText(self.Code2code)
        self.ui.le_parameter_name_3.setText(Code2name)
        self.ui.pb_parameter_edit_3.setEnabled(True)
        self.Code2Cancel()

    def insertIntoCod2Table(self):
        if self.ui.tableWidget_3.rowCount() == 0:
            self.conn = sqlite3.connect('WeighBridge.db')
            self.c = self.conn.cursor()

            result = self.c.execute("SELECT Code,Name FROM T_Code2")
            self.ui.tableWidget_3.setRowCount(0)
            self.ui.tableWidget_3.setHorizontalHeaderLabels(['Code', 'Name'])
            header = self.ui.tableWidget_3.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            for r_num, r_data in enumerate(result):
                self.ui.tableWidget_3.insertRow(r_num)
                for c_num, c_data in enumerate(r_data):
                    self.ui.tableWidget_3.setItem(r_num, c_num, QtWidgets.QTableWidgetItem(str(c_data)))
            # self.ui.tableWidget_1.setSelectionMode(QAbstractItemView.MultiSelection)

            self.c.close()
            self.conn.close()
        else:
            pass

    def Code2Delete(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()

        self.c.execute("DELETE FROM T_Code2 WHERE Code=?", (self.Code2code,))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        self.ui.tableWidget_3.removeRow(self.ui.tableWidget_3.currentRow())

    def Code2Create(self):
        self.ui.pb_parameter_add_3.setEnabled(True)
        self.ui.pb_parameter_edit_3.setEnabled(False)
        self.ui.pb_parameter_create_3.setEnabled(False)
        self.ui.pb_parameter_save_3.setEnabled(False)
        self.ui.pb_parameter_delete_3.setEnabled(False)
        self.ui.le_parameter_code_3.setEnabled(True)
        self.ui.le_parameter_name_3.setEnabled(True)
        self.ui.le_parameter_name_3.clear()
        self.ui.le_parameter_code_3.clear()

    def Code2Add(self):
        self.ui.pb_parameter_create_3.setEnabled(True)
        self.ui.pb_parameter_add_3.setEnabled(False)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        code = self.ui.le_parameter_code_3.text()
        name = self.ui.le_parameter_name_3.text()

        self.c.execute("INSERT INTO T_Code2 (Code,Name) VALUES (?,?) ", (code, name))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        row = self.ui.tableWidget_3.rowCount()
        self.ui.tableWidget_3.insertRow(row)
        self.ui.tableWidget_3.setItem(row, 0, QtWidgets.QTableWidgetItem(str(code)))
        self.ui.tableWidget_3.setItem(row, 1, QtWidgets.QTableWidgetItem(str(name)))

            ### Code 3 page

    def Code3Edit(self):
        self.ui.pb_parameter_edit_4.setEnabled(False)
        self.ui.pb_parameter_create_4.setEnabled(False)
        self.ui.pb_parameter_save_4.setEnabled(True)
        self.ui.pb_parameter_cancel_4.setEnabled(True)
        self.ui.le_parameter_code_4.setEnabled(True)
        self.ui.le_parameter_name_4.setEnabled(True)
        self.ui.le_parameter_name_4.clear()
        self.prevCode3code = self.ui.le_parameter_code_4.text()

    def Code3Cancel(self):
        self.CodesLeDefault()
        self.setCancelSaveAddDelete()
        self.ui.pb_parameter_create_4.setEnabled(True)

    def Code3Save(self):
        self.setCancelSaveAddDelete()
        self.ui.pb_parameter_edit_4.setEnabled(True)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        code = self.ui.le_parameter_code_4.text()
        name = self.ui.le_parameter_name_4.text()
        self.c.execute("UPDATE T_Code3 SET Code=?,Name=? WHERE Code=?", (code, name, self.prevCode3code))
        self.conn.commit()
        ## Left Here
        self.c.close()
        self.conn.close()

        row = self.ui.tableWidget_4.currentRow()

        self.ui.tableWidget_4.setItem(row, 0, QtWidgets.QTableWidgetItem(str(code)))
        self.ui.tableWidget_4.setItem(row, 1, QtWidgets.QTableWidgetItem(str(name)))

    def on_Code3TableSelectionChanged(self):

        row = self.ui.tableWidget_4.currentRow()  # Index of Row

        firstColumnInRow = self.ui.tableWidget_4.item(row, 0)  # returns QTableWidgetItem
        SecondColumnInRow = self.ui.tableWidget_4.item(row, 1)
        self.Code3code = firstColumnInRow.text()
        Code3name = SecondColumnInRow.text()
        self.ui.le_parameter_code_4.setText(self.Code3code)
        self.ui.le_parameter_name_4.setText(Code3name)
        self.ui.pb_parameter_edit_4.setEnabled(True)
        self.Code3Cancel()

    def insertIntoCod3Table(self):
        if self.ui.tableWidget_4.rowCount() == 0:
            self.conn = sqlite3.connect('WeighBridge.db')
            self.c = self.conn.cursor()

            result = self.c.execute("SELECT Code,Name FROM T_Code3")


            self.ui.tableWidget_4.setRowCount(0)

            self.ui.tableWidget_4.setHorizontalHeaderLabels(['Code', 'Name'])
            header = self.ui.tableWidget_4.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

            for r_num, r_data in enumerate(result):
                self.ui.tableWidget_4.insertRow(r_num)
                for c_num, c_data in enumerate(r_data):
                    self.ui.tableWidget_4.setItem(r_num, c_num, QtWidgets.QTableWidgetItem(str(c_data)))
            # self.ui.tableWidget_1.setSelectionMode(QAbstractItemView.MultiSelection)

            self.c.close()
            self.conn.close()
        else:
            pass

    def Code3Delete(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()

        self.c.execute("DELETE FROM T_Code3 WHERE Code=?", (self.Code3code,))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        self.ui.tableWidget_4.removeRow(self.ui.tableWidget_4.currentRow())

    def Code3Create(self):
        self.ui.pb_parameter_add_4.setEnabled(True)
        self.ui.pb_parameter_edit_4.setEnabled(False)
        self.ui.pb_parameter_create_4.setEnabled(False)
        self.ui.pb_parameter_save_4.setEnabled(False)
        self.ui.pb_parameter_delete_4.setEnabled(False)
        self.ui.le_parameter_code_4.setEnabled(True)
        self.ui.le_parameter_name_4.setEnabled(True)
        self.ui.le_parameter_name_4.clear()
        self.ui.le_parameter_code_4.clear()
        self.ui.pb_parameter_cancel_4.setEnabled(True)

    def Code3Add(self):
        self.ui.pb_parameter_create_4.setEnabled(True)
        self.ui.pb_parameter_add_4.setEnabled(False)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        code = self.ui.le_parameter_code_4.text()
        name = self.ui.le_parameter_name_4.text()

        self.c.execute("INSERT INTO T_Code3 (Code,Name) VALUES (?,?) ", (code, name))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        row = self.ui.tableWidget_4.rowCount()
        self.ui.tableWidget_4.insertRow(row)
        self.ui.tableWidget_4.setItem(row, 0, QtWidgets.QTableWidgetItem(str(code)))
        self.ui.tableWidget_4.setItem(row, 1, QtWidgets.QTableWidgetItem(str(name)))

                ### Code 4
    def Code4Edit(self):
        self.ui.pb_parameter_edit_5.setEnabled(False)
        self.ui.pb_parameter_create_5.setEnabled(False)
        self.ui.pb_parameter_save_5.setEnabled(True)
        self.ui.pb_parameter_cancel_5.setEnabled(True)
        self.ui.le_parameter_code_5.setEnabled(True)
        self.ui.le_parameter_name_5.setEnabled(True)
        self.ui.le_parameter_name_5.clear()
        self.prevCode4code = self.ui.le_parameter_code_5.text()

    def Code4Cancel(self):
        self.CodesLeDefault()
        self.setCancelSaveAddDelete()
        self.ui.pb_parameter_create_5.setEnabled(True)

    def Code4Save(self):
        self.setCancelSaveAddDelete()
        self.ui.pb_parameter_edit_5.setEnabled(True)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        code = self.ui.le_parameter_code_5.text()
        name = self.ui.le_parameter_name_5.text()
        self.c.execute("UPDATE T_Code4 SET Code=?,Name=? WHERE Code=?", (code, name, self.prevCode4code))
        self.conn.commit()
        ## Left Here
        self.c.close()
        self.conn.close()

        row = self.ui.tableWidget_5.currentRow()

        self.ui.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(code)))
        self.ui.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(name)))

    def on_Code4TableSelectionChanged(self):

        row = self.ui.tableWidget_5.currentRow()  # Index of Row

        firstColumnInRow = self.ui.tableWidget_5.item(row, 0)  # returns QTableWidgetItem
        SecondColumnInRow = self.ui.tableWidget_5.item(row, 1)
        self.Code4code = firstColumnInRow.text()
        Code4name = SecondColumnInRow.text()
        self.ui.le_parameter_code_5.setText(self.Code4code)
        self.ui.le_parameter_name_5.setText(Code4name)
        self.ui.pb_parameter_edit_5.setEnabled(True)
        self.Code4Cancel()

    def insertIntoCod4Table(self):
        if self.ui.tableWidget_5.rowCount() == 0:
            self.conn = sqlite3.connect('WeighBridge.db')
            self.c = self.conn.cursor()

            result = self.c.execute("SELECT Code,Name FROM T_Code4")

            self.ui.tableWidget_5.setRowCount(0)

            self.ui.tableWidget_5.setHorizontalHeaderLabels(['Code', 'Name'])
            header = self.ui.tableWidget_5.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

            for r_num, r_data in enumerate(result):
                self.ui.tableWidget_5.insertRow(r_num)
                for c_num, c_data in enumerate(r_data):
                    self.ui.tableWidget_5.setItem(r_num, c_num, QtWidgets.QTableWidgetItem(str(c_data)))
            # self.ui.tableWidget_1.setSelectionMode(QAbstractItemView.MultiSelection)

            self.c.close()
            self.conn.close()
        else:
            pass

    def Code4Delete(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()

        self.c.execute("DELETE FROM T_Code4 WHERE Code=?", (self.Code4code,))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        self.ui.tableWidget_5.removeRow(self.ui.tableWidget_5.currentRow())

    def Code4Create(self):
        self.ui.pb_parameter_add_5.setEnabled(True)
        self.ui.pb_parameter_edit_5.setEnabled(False)
        self.ui.pb_parameter_create_5.setEnabled(False)
        self.ui.pb_parameter_save_5.setEnabled(False)
        self.ui.pb_parameter_delete_5.setEnabled(False)
        self.ui.le_parameter_code_5.setEnabled(True)
        self.ui.le_parameter_name_5.setEnabled(True)
        self.ui.le_parameter_name_5.clear()
        self.ui.le_parameter_code_5.clear()
        self.ui.pb_parameter_cancel_5.setEnabled(True)

    def Code4Add(self):
        self.ui.pb_parameter_create_5.setEnabled(True)
        self.ui.pb_parameter_add_5.setEnabled(False)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        code = self.ui.le_parameter_code_5.text()
        name = self.ui.le_parameter_name_5.text()

        self.c.execute("INSERT INTO T_Code4 (Code,Name) VALUES (?,?) ", (code, name))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        row = self.ui.tableWidget_5.rowCount()
        self.ui.tableWidget_5.insertRow(row)
        self.ui.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(code)))
        self.ui.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(name)))
                ### Code 5
    def Code5Edit(self):
        self.ui.pb_parameter_edit_6.setEnabled(False)
        self.ui.pb_parameter_create_6.setEnabled(False)
        self.ui.pb_parameter_save_6.setEnabled(True)
        self.ui.pb_parameter_cancel_6.setEnabled(True)
        self.ui.le_parameter_code_6.setEnabled(True)
        self.ui.le_parameter_name_6.setEnabled(True)
        self.ui.le_parameter_name_6.clear()
        self.prevCode5code = self.ui.le_parameter_code_6.text()

    def Code5Cancel(self):
        self.CodesLeDefault()
        self.setCancelSaveAddDelete()
        self.ui.pb_parameter_create_6.setEnabled(True)

    def Code5Save(self):
        self.setCancelSaveAddDelete()
        self.ui.pb_parameter_edit_6.setEnabled(True)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        code = self.ui.le_parameter_code_6.text()
        name = self.ui.le_parameter_name_6.text()
        self.c.execute("UPDATE T_Code5 SET Code=?,Name=? WHERE Code=?", (code, name, self.prevCode5code))
        self.conn.commit()
        ## Left Here
        self.c.close()
        self.conn.close()

        row = self.ui.tableWidget_6.currentRow()

        self.ui.tableWidget_6.setItem(row, 0, QtWidgets.QTableWidgetItem(str(code)))
        self.ui.tableWidget_6.setItem(row, 1, QtWidgets.QTableWidgetItem(str(name)))

    def on_Code5TableSelectionChanged(self):

        row = self.ui.tableWidget_6.currentRow()  # Index of Row

        firstColumnInRow = self.ui.tableWidget_6.item(row, 0)  # returns QTableWidgetItem
        SecondColumnInRow = self.ui.tableWidget_6.item(row, 1)
        self.Code5code = firstColumnInRow.text()
        Code5name = SecondColumnInRow.text()
        self.ui.le_parameter_code_6.setText(self.Code5code)
        self.ui.le_parameter_name_6.setText(Code5name)
        self.ui.pb_parameter_edit_6.setEnabled(True)
        self.Code5Cancel()

    def insertIntoCod5Table(self):
        if self.ui.tableWidget_6.rowCount() == 0:
            self.conn = sqlite3.connect('WeighBridge.db')
            self.c = self.conn.cursor()

            result = self.c.execute("SELECT Code,Name FROM T_Code5")

            self.ui.tableWidget_6.setRowCount(0)

            self.ui.tableWidget_6.setHorizontalHeaderLabels(['Code', 'Name'])
            header = self.ui.tableWidget_6.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

            for r_num, r_data in enumerate(result):
                self.ui.tableWidget_6.insertRow(r_num)
                for c_num, c_data in enumerate(r_data):
                    self.ui.tableWidget_6.setItem(r_num, c_num, QtWidgets.QTableWidgetItem(str(c_data)))
            # self.ui.tableWidget_1.setSelectionMode(QAbstractItemView.MultiSelection)

            self.c.close()
            self.conn.close()
        else:
            pass

    def Code5Delete(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()

        self.c.execute("DELETE FROM T_Code5 WHERE Code=?", (self.Code5code,))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        self.ui.tableWidget_6.removeRow(self.ui.tableWidget_6.currentRow())

    def Code5Create(self):
        self.ui.pb_parameter_add_6.setEnabled(True)
        self.ui.pb_parameter_edit_6.setEnabled(False)
        self.ui.pb_parameter_create_6.setEnabled(False)
        self.ui.pb_parameter_save_6.setEnabled(False)
        self.ui.pb_parameter_delete_6.setEnabled(False)
        self.ui.le_parameter_code_6.setEnabled(True)
        self.ui.le_parameter_name_6.setEnabled(True)
        self.ui.le_parameter_name_6.clear()
        self.ui.le_parameter_code_6.clear()
        self.ui.pb_parameter_cancel_6.setEnabled(True)

    def Code5Add(self):
        self.ui.pb_parameter_create_6.setEnabled(True)
        self.ui.pb_parameter_add_6.setEnabled(False)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        code = self.ui.le_parameter_code_6.text()
        name = self.ui.le_parameter_name_6.text()

        self.c.execute("INSERT INTO T_Code5 (Code,Name) VALUES (?,?) ", (code, name))
        self.conn.commit()
        self.c.close()
        self.conn.close()
        row = self.ui.tableWidget_6.rowCount()
        self.ui.tableWidget_6.insertRow(row)
        self.ui.tableWidget_6.setItem(row, 0, QtWidgets.QTableWidgetItem(str(code)))
        self.ui.tableWidget_6.setItem(row, 1, QtWidgets.QTableWidgetItem(str(name)))
    #### Functions used in Settings page
    def showSettings(self):
        self.ui.stackedWidgetMain.setCurrentWidget(self.ui.Settings)
        self.getValuesFromDB()
        self.ui.pb_settings_Comm_save.setEnabled(False)
    def showSettingsMainPage(self):
        self.ui.stackedWidgetSettings.setCurrentWidget(self.ui.settingsMainPage)
    def showCommPortSettings(self):
        self.ui.stackedWidgetSettings.setCurrentWidget(self.ui.CommPortSettings)
        self.getValuesFromDB()
        self.ui.pb_settings_Comm_save.setEnabled(False)
    def showHeaderSettings(self):
        self.ui.stackedWidgetSettings.setCurrentWidget(self.ui.HeaderSettings)

    def showUserAccountSettings(self):
        self.ui.stackedWidgetSettings.setCurrentWidget(self.ui.UserAccountSettings)
        self.setTableData()
        # print(self.adminList)

    def AdminUnMask(self):
        self.ui.pb_HeaderSettings.setHidden(False)
        self.ui.pb_UserAccountSettings.setHidden(False)
        self.ui.pb_home_ParameterSettings.setHidden(False)
        self.ui.pb_home_report.setHidden(False)

          # CommPort  Settings Page
    def findPorts(self):
        self.ui.pb_settings_Comm_save.setEnabled(True)
        self.ui.pb_settings_search.setEnabled(False)
        self.pts = serial.tools.list_ports.comports()
        print("ok")
        self.ports = []
        #portss = ['com1','com2','com3']


        NumOfPorts = len(self.pts)
        for p in self.pts:

            p = str(p)
            p = p.split(" ")
            port = p[0]
            self.ports.append(port)
        self.ui.lb_settings_CommPortDisplay.setText(self.ports[0])
        #self.s = self.ui.combo_settings_CommPortDisplay.setCurrentText()
    def getValuesFromDB(self):
        conn = sqlite3.connect("WeighBridge.db")
        c = conn.cursor()
        result = c.execute("SELECT * FROM T_CommSettings")
        for _,data in enumerate(result):
            comm = data[1]
            bdrate_ = data[2]
            controler_ = data[3]
            pt_ = data[4]
            pport = data[5]
            pbdrate_ = data[6]
        bdrate = ["1200", "2400", "4800", "9600", "19200"]
        controller = ["WT", "MW5004", "AWEW"]
        pbdrate = ["1200", "2400", "4800", "9600", "19200"]
        ptype = ["InkJet", "DotMatrix"]
        bi = bdrate.index(str(bdrate_))
        ci = controller.index(str(controler_))
        pbi = pbdrate.index(str(pbdrate_))
        pi = ptype.index(str(pt_))

        self.ui.lb_settings_CommPortDisplay.setText(str(comm).upper())
        self.ui.lb_settings_PrinterCommPortDisplay.setText(str(pport).upper())
        self.ui.combo_settings_BaudRate.setCurrentIndex(bi)
        self.ui.combo_settings_Controller.setCurrentIndex(ci)
        self.ui.combo_settings_PrinterBaudRate.setCurrentIndex(pbi)
        self.ui.combo_settings_PrinterType.setCurrentIndex(pi)
        c.close()
        conn.close()

    def defaultComboBoxValues(self):
        bdrate = ["1200","2400","4800","9600","19200"]
        controller = ["WT","MW5004","AWEW"]
        pbdrate = ["1200","2400","4800","9600","19200"]
        ptype = ["InkJet","DotMatrix"]
        self.ui.combo_settings_BaudRate.addItems(bdrate)
        self.ui.combo_settings_Controller.addItems(controller)
        self.ui.combo_settings_PrinterBaudRate.addItems(pbdrate)
        self.ui.combo_settings_PrinterType.addItems(ptype)

    def CommSettingsSave(self):
        self.ui.pb_settings_Comm_save.setEnabled(False)
        self.ui.pb_settings_search.setEnabled(True)
        conn = sqlite3.connect("WeighBridge.db")
        c = conn.cursor()
        port = self.ui.lb_settings_CommPortDisplay.text()
        # port = "Com5"
        bdrate = self.ui.combo_settings_BaudRate.currentText()
        controller = self.ui.combo_settings_Controller.currentText()
        PPort = self.ui.lb_settings_PrinterCommPortDisplay.text()
        Pbdrate = self.ui.combo_settings_PrinterBaudRate.currentText()
        ptype = self.ui.combo_settings_PrinterType.currentText()
        values = (port,bdrate,controller,PPort,Pbdrate,ptype,1)
        c.execute("UPDATE T_CommSettings SET Comm=?,BaudRate=?,Controller=?,PrinterPort=?,PrinterBaudRate=?,Printer=? WHERE Id=?",values)

        conn.commit()
        c.close()
        conn.close()
        msg = QMessageBox()
        msg.information(None,"Info","ReStart the application")
        if msg.Ok:

            self.main_window.close()

           # UserAccount Settings
    def default(self):
        userslist = ["admin","operator","lcs"]
        passwordlist = ["admin","operator", "lcs"]
        self.conn = sqlite3.connect('WeighBridge.db')
        self.cursor = self.conn.cursor()
        for i in range(1,4):
            u = userslist[i-1]
            pw = passwordlist[i-1]
            ac = True
            ad = False
            if u == "admin":
                ad = True

            #self.cursor.execute("INSERT INTO T_UserAccountSettings (User, Password, Active, Admin) VALUES (?,?,?,?)",(u,pw,ac,ad))
        # self.cursor.execute("INSERT INTO T_HeaderSettings ('S.no',Header) VALUES (1,'Header1')")
        # self.cursor.execute("INSERT INTO T_HeaderSettings ('S.no',Header) VALUES (2,'Header2')")
        # self.cursor.execute("INSERT INTO T_HeaderSettings ('S.no',Header) VALUES (3,'Header3')")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def setButtonName(self):
        self.ui.pb_settings_admin.setText(self.userList[0])
        self.ui.pb_settings_operator.setText(self.userList[1])
        self.ui.pb_settings_lcs.setText(self.userList[2])
    def clearWhenToggle(self):
        self.ui.le_settings_password.clear()
        self.ui.le_settings_newpassword.clear()
        self.ui.le_settings_retypepassword.clear()
    def UserSettingsEdit(self):

        self.ui.le_settings_password.clear()
        self.ui.le_settings_newpassword.clear()
        self.ui.le_settings_retypepassword.clear()

        self.ui.le_settings_username.setReadOnly(False)
        self.ui.le_settings_password.setReadOnly(False)
        self.ui.le_settings_newpassword.setReadOnly(False)
        self.ui.le_settings_retypepassword.setReadOnly(False)
        self.ui.rb_settings_activeYes.setCheckable(True)
        self.ui.rb_settings_activeNo.setCheckable(True)
        self.ui.rb_settings_adminYes.setCheckable(True)
        self.ui.rb_settings_adminNo.setCheckable(True)
    def UserSettingsCancel(self):
        self.ui.le_settings_id.setReadOnly(True)
        self.ui.le_settings_username.setReadOnly(True)
        self.ui.le_settings_password.setReadOnly(True)
        self.ui.le_settings_newpassword.setReadOnly(True)
        self.ui.le_settings_retypepassword.setReadOnly(True)
        self.ui.rb_settings_activeYes.setCheckable(False)
        self.ui.rb_settings_activeNo.setCheckable(False)
        self.ui.rb_settings_adminYes.setCheckable(False)
        self.ui.rb_settings_adminNo.setCheckable(False)

    def DownloadDataFromUserAccountTable(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        cmd = "SELECT ID,User,Password,Active,Admin FROM T_UserAccountSettings"
        result = self.c.execute(cmd)


        for id,user,password,active,admin in result:
            self.idList.append(id)
            self.userList.append(user)
            self.passwordList.append(password)
            self.activeList.append(active)
            self.adminList.append(admin)
        self.setButtonName()
        # print(self.userList[0])
        self.c.close()
        self.conn.close()

    def admin(self):
        self.clearWhenToggle()

        self.ui.rb_settings_activeYes.setChecked(False)
        self.ui.rb_settings_activeNo.setChecked(False)
        self.ui.rb_settings_adminYes.setChecked(False)
        self.ui.rb_settings_adminNo.setChecked(False)

        self.ui.rb_settings_activeYes.setCheckable(True)
        self.ui.rb_settings_activeNo.setCheckable(True)
        self.ui.rb_settings_adminYes.setCheckable(True)
        self.ui.rb_settings_adminNo.setCheckable(True)

        self.ui.le_settings_id.setText(str(self.idList[0]))
        self.ui.le_settings_username.setText(self.userList[0])
        if self.adminList[0] == '1' :
            self.ui.rb_settings_adminYes.setChecked(True)
        else:
            self.ui.rb_settings_adminNo.setChecked(True)
        if self.activeList[0] == '1':
            self.ui.rb_settings_activeYes.setChecked(True)
        else:
            self.ui.rb_settings_activeNo.setChecked(True)

    def operator(self):
        self.clearWhenToggle()

        self.ui.rb_settings_activeYes.setChecked(False)
        self.ui.rb_settings_activeNo.setChecked(False)
        self.ui.rb_settings_adminYes.setChecked(False)
        self.ui.rb_settings_adminNo.setChecked(False)

        self.ui.rb_settings_activeYes.setCheckable(True)
        self.ui.rb_settings_activeNo.setCheckable(True)
        self.ui.rb_settings_adminYes.setCheckable(True)
        self.ui.rb_settings_adminNo.setCheckable(True)

        self.ui.le_settings_id.setText(str(self.idList[1]))
        self.ui.le_settings_username.setText(self.userList[1])
        if self.adminList[1] == '1' :
            self.ui.rb_settings_adminYes.setChecked(True)
        else:
            self.ui.rb_settings_adminNo.setChecked(True)
        if self.activeList[1] == '1':
            self.ui.rb_settings_activeYes.setChecked(True)
        else:
            self.ui.rb_settings_activeNo.setChecked(True)
    def lcs(self):
        self.clearWhenToggle()

        self.ui.rb_settings_activeYes.setChecked(False)
        self.ui.rb_settings_activeNo.setChecked(False)
        self.ui.rb_settings_adminYes.setChecked(False)
        self.ui.rb_settings_adminNo.setChecked(False)

        self.ui.rb_settings_activeYes.setCheckable(True)
        self.ui.rb_settings_activeNo.setCheckable(True)
        self.ui.rb_settings_adminYes.setCheckable(True)
        self.ui.rb_settings_adminNo.setCheckable(True)
        self.ui.le_settings_id.setText(str(self.idList[2]))
        self.ui.le_settings_username.setText(self.userList[2])
        if self.adminList[2] == '1':
            self.ui.rb_settings_adminYes.setChecked(True)
        else:
            self.ui.rb_settings_adminNo.setChecked(True)
        if self.activeList[2] == '1':
            self.ui.rb_settings_activeYes.setChecked(True)
        else:
            self.ui.rb_settings_activeNo.setChecked(True)

    def setTableData(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        cmd = "SELECT ID,User,Active,Admin FROM T_UserAccountSettings"
        result = self.c.execute(cmd)
        self.ui.tw_settings_users.setRowCount(0)
        self.ui.tw_settings_users.setHorizontalHeaderLabels(['ID','USER','ACTIVE','ADMIN'])
        for r_num, r_data in enumerate(result):
            self.ui.tw_settings_users.insertRow(r_num)
            for c_num, c_data in enumerate(r_data):
                self.ui.tw_settings_users.setItem(r_num, c_num, QtWidgets.QTableWidgetItem(str(c_data)))
        self.c.close()
        self.conn.close()

    def addToT_UserAccountSettings(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()

        Id = self.ui.le_settings_id.text()
        Id = int(Id)
        User = self.ui.le_settings_username.text()
        OldPassword = self.ui.le_settings_password.text()
        NewPassword = self.ui.le_settings_newpassword.text()
        RetypePassword = self.ui.le_settings_retypepassword.text()
        print("before ",self.userList[int(Id)-1])
        if OldPassword == self.passwordList[int(Id)-1]:
            if NewPassword == "":
                self.c.execute("UPDATE T_UserAccountSettings SET User=? WHERE ID=?",
                               (User,Id))
                self.conn.commit()
                self.userList[Id - 1] = User
            elif NewPassword == RetypePassword:
                self.c.execute("UPDATE T_UserAccountSettings SET User=?, Password=? WHERE ID=?",(User,NewPassword,Id))
                self.conn.commit()
                self.userList[Id - 1] = User
                self.passwordList[Id - 1] = NewPassword

            else:
                self.showErrormsg("Error","Password does not match")
        else:
            self.showErrormsg("Error","Type the correst OldPassword")
            self.UserSettingsEdit()
        if self.ui.rb_settings_activeYes.isChecked():
            self.activeList[Id-1] = '1'
        elif self.ui.rb_settings_activeNo.isChecked():
            self.activeList[Id-1] = '0'
        if self.ui.rb_settings_adminYes.isChecked():
            self.adminList[Id-1] = '1'
        elif self.ui.rb_settings_adminNo.isChecked():
            self.adminList[Id-1] = '0'

        self.c.execute("UPDATE T_UserAccountSettings SET Active=?, Admin=? WHERE ID=?",(self.activeList[Id-1],self.adminList[Id-1],Id))
        self.conn.commit()
        self.c.close()
        self.conn.close()

        print("After ", self.userList[int(Id) - 1])
        print("admin= ",self.adminList[Id-1])
        print("active = ",self.activeList[Id-1])
        self.setButtonName()
        self.setTableData()

        #
        # self.conn = sqlite3.connect('WeighBridge.db')
        # self.cursor = self.conn.cursor()

            ### Header Settings
    def setMainPageLogo(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        result = self.c.execute("SELECT LogoName FROM T_LogoImage")
        for path in result:
            imgPath = path[0]
        pixmap = QPixmap(imgPath)
        self.ui.lb_CompanyLogo.setPixmap(QPixmap(pixmap))

        self.c.close()
        self.conn.close()

    def setMainPageHeaders(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        headers = []
        results = self.c.execute("SELECT Header FROM T_HeaderSettings")
        for header in results:
            headers.append(header[0])

        # self.ui.lb_header1.setText(headers[0])
        # self.ui.lb_header2.setText(headers[1])
        # self.ui.lb_header3.setText(headers[2])
        self.c.close()
        self.conn.close()
    def browseLogoImage(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()

        fname = QtWidgets.QFileDialog.getOpenFileName()
        imgPath = fname[0]
        # self.c.execute("INSERT INTO T_LogoImage (LogoName,No) VALUES (?,?)",(str(imgPath),1))
        self.c.execute("UPDATE T_LogoImage SET LogoName=? WHERE No=?",(imgPath,1))
        pixmap = QPixmap(imgPath)
        self.ui.lb_CompanyLogo.setPixmap(QPixmap(pixmap))

        self.conn.commit()
        self.c.close()
        self.conn.close()
    def HeaderEdit(self):
        self.ui.le_settings_title1.setReadOnly(False)
        self.ui.le_settings_title2.setReadOnly(False)
        self.ui.le_settings_title3.setReadOnly(False)

    def HeaderCancel(self):
        self.ui.le_settings_title1.setReadOnly(True)
        self.ui.le_settings_title2.setReadOnly(True)
        self.ui.le_settings_title3.setReadOnly(True)

    def HeaderSave(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()

        header1 = self.ui.le_settings_title1.text()
        header2 = self.ui.le_settings_title2.text()
        header3 = self.ui.le_settings_title3.text()
        if len(header1)>1:
            # self.ui.lb_header1.setText(header1)
            self.c.execute("UPDATE T_HeaderSettings SET Header=? WHERE Sno=?", (header1,1))
        if len(header2)>1:
            # self.ui.lb_header2.setText(header2)
            self.c.execute("UPDATE T_HeaderSettings SET Header=? WHERE Sno=?", (header2, 2))
        if len(header3)>1:
            # self.ui.lb_header3.setText(header3)
            self.c.execute("UPDATE T_HeaderSettings SET Header=? WHERE Sno=?", (header3, 3))
        self.conn.commit()
        self.c.close()
        self.conn.close()

    # Functions used in Report page
    def showReport(self):
        self.ui.stackedWidgetMain.setCurrentWidget(self.ui.Report)
        self.setTheField()
        self.Report_setInitialComponents()
        self.getLableNameFromDB()

        self.ui.pb_report_pdf.setEnabled(False)
        self.ui.report_tableWidget.clear()
        self.OverallReportFlag = 0

    def Report_setInitialComponents(self):

        self.ui.gb_Report_DaiyReport.setHidden(True)
        self.ui.gb_Report_MonthlyReport.setHidden(True)
        self.ui.gb_Report_HeaderCode.setHidden(True)
        self.ui.gb_Report_TypOfReport.setHidden(True)
        self.ui.combo_report_Header.addItems(self.headersname)
        self.ui.combo_report_Code.addItems(self.codersname)
        self.ui.lb_report_selection.clear()
        self.ui.combo_report_selection.clear()
        self.value = ''


    def openOverallReport(self):
        if self.OverallReportFlag == 0:
            self.ui.gb_Report_TypOfReport.setHidden(False)
            self.ui.pb_Report_DailyReport.setHidden(False)
            self.OverallReportFlag = 1
        elif self.OverallReportFlag == 1:
            self.ui.gb_Report_TypOfReport.setChecked(True)
            self.Report_setInitialComponents()
            self.OverallReportFlag = 0

    def openDailyReport(self):
        self.ui.gb_Report_DaiyReport.setHidden(False)

    def openMonthlyReport(self):
        self.ui.gb_Report_MonthlyReport.setHidden(False)

    def setSelectionHeader(self):
        self.OverallReportFlag = 1
        self.ui.gb_Report_HeaderCode.setHidden(False)
        self.ui.gb_Report_TypOfReport.setHidden(False)
        self.ui.pb_Report_DailyReport.setHidden(True)
        self.ui.gb_Report_MonthlyReport.setHidden(False)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        header1,header2,header3,header4,header5 = [],[],[],[],[]
        result = self.c.execute("SELECT header1,header2,header3,header4,header5 FROM T_Entry")
        for i, data in enumerate(result):
            header1.append(data[0])
            header2.append(data[1])
            header3.append(data[2])
            header4.append(data[3])
            header5.append(data[4])
        txt = self.ui.combo_report_Header.currentText()
        self.ui.lb_report_selection.setText(txt)
        index = self.headersname.index(txt)

        self.value = self.headers[index]
        self.ui.combo_report_selection.clear()
        if self.value == 'header1':
            self.ui.combo_report_selection.addItems(header1)
        elif self.value == 'header2':
            self.ui.combo_report_selection.addItems(header2)
        elif self.value == 'header3':
            self.ui.combo_report_selection.addItems(header3)
        elif self.value == 'header4':
            self.ui.combo_report_selection.addItems(header4)
        elif self.value == 'header5':
            self.ui.combo_report_selection.addItems(header5)

        self.c.close()
        self.conn.close()

    def setSelectionCode(self):
        self.OverallReportFlag = 1
        self.ui.gb_Report_HeaderCode.setHidden(False)
        self.ui.gb_Report_TypOfReport.setHidden(False)
        self.ui.pb_Report_DailyReport.setHidden(True)
        self.ui.gb_Report_MonthlyReport.setHidden(False)
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()

        code1, code2, code3, code4, code5 = [], [], [], [], []
        result = self.c.execute("SELECT code1_no,code2_no,code3_no,code4_no,code5_no FROM T_Entry")
        for i, data in enumerate(result):
            code1.append(data[0])
            code2.append(data[1])
            code3.append(data[2])
            code4.append(data[3])
            code5.append(data[4])
        txt = self.ui.combo_report_Code.currentText()
        self.ui.lb_report_selection.setText(txt)
        index = self.codersname.index(txt)

        self.value = self.coders[index]
        self.ui.combo_report_selection.clear()
        if self.value == 'code1':
            self.ui.combo_report_selection.addItems(code1)
        elif self.value == 'code2':
            self.ui.combo_report_selection.addItems(code2)
        elif self.value == 'code3':
            self.ui.combo_report_selection.addItems(code3)
        elif self.value == 'code4':
            self.ui.combo_report_selection.addItems(code4)
        elif self.value == 'code5':
            self.ui.combo_report_selection.addItems(code5)

        self.c.close()
        self.conn.close()
    def setTheField(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        result = self.c.execute("SELECT EN_ED, Name, Type FROM T_CodeAndHeader")
        self.enableField = []
        self.titles = ["SerialNo","Report date","ReportTime"]
        self.headers = []
        self.coders = []
        self.headersname = []
        self.codersname = []
        for i,data in enumerate(result):
            self.enableField.append(data[0])
            if self.enableField[i] == 1:
                self.titles.append(data[1])
                st = data[2]
                if st[0] == 'c':
                    self.codersname.append(data[1])
                    self.coders.append(st)
                elif st[0] == 'h':
                    self.headersname.append(data[1])
                    self.headers.append(st)
        self.titles.append("grosswt")
        self.titles.append("tarewt")
        self.titles.append("netwt")
        self.titles.append("amount")

        self.c.close()
        self.conn.close()
    def DailyReport(self):
        # date = self.ui.report_DateEdit.date().toPyDate("%d%m%y")
        inflag = False
        self.ui.report_tableWidget.clear()
        date = self.ui.report_DateEdit.date().toPyDate().strftime("%d-%m-%y")

        self.conn = sqlite3.connect("WeighBridge.db")
        self.c = self.conn.cursor()
        self.pdfTableData = []
        result = self.c.execute(
                                "SELECT SerialNo,ReportDate,ReportTime, code1_no,code2_no,code3_no,code4_no,code5_no,header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=?",
                                (date,))

        # titles = ["SerialNo","Report date","ReportTime",self.names[5], self.names[6], self.names[7], self.names[8], self.names[9],
        #                                                       self.names[0], self.names[1], self.names[2], self.names[3], self.names[4],
        #                                                       "grosswt","tarewt", "netwt", "amount"]

        nwen = [1,1,1] + self.enableField[0:] + [1,1,1,1]

        self.pdfTableData.append(self.titles)
        self.ui.report_tableWidget.setRowCount(0)
        self.ui.report_tableWidget.setColumnCount(len(self.titles))
        self.ui.report_tableWidget.setHorizontalHeaderLabels(self.titles)
        header = self.ui.report_tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        for r_num, r_data in enumerate(result):
            inflag = True
            self.ui.pb_report_pdf.setEnabled(True)
            self.ui.pb_report_excel.setEnabled(True)
            self.ui.report_tableWidget.insertRow(r_num)
            r_data = list(r_data)
            row = []
            for i in range(len(r_data)):

                if nwen[i] == 1:
                    row.append(r_data[i])

            self.pdfTableData.append(row)
            for i in range(len(row)):
                # self.ui.report_tableWidget.insertColumn(i)
                self.ui.report_tableWidget.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))



        if inflag == False:
            self.showErrormsg("","Data not available")


        self.c.close()
        self.conn.close()

    def MonthlyReport(self):
        inflag = False
        self.ui.report_tableWidget.clear()
        conn = sqlite3.connect("WeighBridge.db")
        c = conn.cursor()
        sd = self.ui.report_FromDate.date().toPyDate().strftime("%d-%m-%y")
        ed = self.ui.report_ToDate.date().toPyDate().strftime("%d-%m-%y")
        sortusing = self.value
        sortname = self.ui.combo_report_selection.currentText()
        sd = list(map(int, sd.split('-')))
        ed = list(map(int, ed.split('-')))
        sd[2] = sd[2] + 2000
        ed[2] = ed[2] + 2000
        dates = []

        start_date = date(sd[2], sd[1], sd[0])
        end_date = date(ed[2], ed[1], ed[0])

        delta = end_date - start_date  # returns timedelta
        nwen = [1, 1, 1] + self.enableField[0:] + [1, 1, 1, 1]
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            dates.append(day.strftime("%d-%m-%y"))

        self.pdfTableData = []

        self.pdfTableData.append(self.titles)

        self.ui.report_tableWidget.setRowCount(0)
        self.ui.report_tableWidget.setColumnCount(len(self.titles))
        self.ui.report_tableWidget.setHorizontalHeaderLabels(self.titles)

        header = self.ui.report_tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        for d in dates:
            if sortusing == '':
                result = c.execute(
                    """SELECT SerialNo,ReportDate,ReportTime,code1_no,code2_no,code3_no,code4_no,code5_no, header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=?""",
                    (d,))

                for r_num, r_data in enumerate(result):
                    inflag = True
                    self.ui.pb_report_pdf.setEnabled(True)
                    self.ui.pb_report_excel.setEnabled(True)
                    self.ui.report_tableWidget.insertRow(r_num)
                    r_data = list(r_data)
                    row = []
                    for i in range(len(r_data)):

                        if nwen[i] == 1:
                            row.append(r_data[i])

                    self.pdfTableData.append(row)
                    for i in range(len(row)):

                        self.ui.report_tableWidget.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))
            elif sortusing == 'header1':
                result = c.execute(
                    """SELECT SerialNo,ReportDate,ReportTime,code1_no,code2_no,code3_no,code4_no,code5_no, header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=? AND header1=?""",
                    (d,sortname))
                for r_num, r_data in enumerate(result):
                    inflag = True
                    self.ui.pb_report_pdf.setEnabled(True)
                    self.ui.pb_report_excel.setEnabled(True)
                    self.ui.report_tableWidget.insertRow(r_num)
                    r_data = list(r_data)
                    row = []
                    for i in range(len(r_data)):

                        if nwen[i] == 1:
                            row.append(r_data[i])

                    self.pdfTableData.append(row)
                    for i in range(len(row)):

                        self.ui.report_tableWidget.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))
            elif sortusing == 'header2':
                result = c.execute(
                    """SELECT SerialNo,ReportDate,ReportTime,code1_no,code2_no,code3_no,code4_no,code5_no, header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=? AND header2=?""",
                    (d,sortname))
                for r_num, r_data in enumerate(result):
                    inflag = True
                    self.ui.pb_report_pdf.setEnabled(True)
                    self.ui.pb_report_excel.setEnabled(True)
                    self.ui.report_tableWidget.insertRow(r_num)
                    r_data = list(r_data)
                    row = []
                    for i in range(len(r_data)):

                        if nwen[i] == 1:
                            row.append(r_data[i])

                    self.pdfTableData.append(row)
                    for i in range(len(row)):

                        self.ui.report_tableWidget.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))
            elif sortusing == 'header3':
                result = c.execute(
                    """SELECT SerialNo,ReportDate,ReportTime,code1_no,code2_no,code3_no,code4_no,code5_no, header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=? AND header3=?""",
                    (d,sortname))
                for r_num, r_data in enumerate(result):
                    inflag = True
                    self.ui.pb_report_pdf.setEnabled(True)
                    self.ui.pb_report_excel.setEnabled(True)
                    self.ui.report_tableWidget.insertRow(r_num)
                    r_data = list(r_data)
                    row = []
                    for i in range(len(r_data)):

                        if nwen[i] == 1:
                            row.append(r_data[i])

                    self.pdfTableData.append(row)
                    for i in range(len(row)):

                        self.ui.report_tableWidget.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))
            elif sortusing == 'header4':
                result = c.execute(
                    """SELECT SerialNo,ReportDate,ReportTime,code1_no,code2_no,code3_no,code4_no,code5_no, header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=? AND header4=?""",
                    (d,sortname))
                for r_num, r_data in enumerate(result):
                    inflag = True
                    self.ui.pb_report_pdf.setEnabled(True)
                    self.ui.pb_report_excel.setEnabled(True)
                    self.ui.report_tableWidget.insertRow(r_num)
                    r_data = list(r_data)
                    row = []
                    for i in range(len(r_data)):

                        if nwen[i] == 1:
                            row.append(r_data[i])

                    self.pdfTableData.append(row)
                    for i in range(len(row)):

                        self.ui.report_tableWidget.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))
            elif sortusing == 'header5':
                result = c.execute(
                    """SELECT SerialNo,ReportDate,ReportTime,code1_no,code2_no,code3_no,code4_no,code5_no, header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=? AND header5=?""",
                    (d,sortname))
                for r_num, r_data in enumerate(result):
                    inflag = True
                    self.ui.pb_report_pdf.setEnabled(True)
                    self.ui.pb_report_excel.setEnabled(True)
                    self.ui.report_tableWidget.insertRow(r_num)
                    r_data = list(r_data)
                    row = []
                    for i in range(len(r_data)):

                        if nwen[i] == 1:
                            row.append(r_data[i])

                    self.pdfTableData.append(row)
                    for i in range(len(row)):

                        self.ui.report_tableWidget.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))
            elif sortusing == 'code1':
                result = c.execute(
                    """SELECT SerialNo,ReportDate,ReportTime,code1_no,code2_no,code3_no,code4_no,code5_no, header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=? AND code1_no=?""",
                    (d,sortname))
                for r_num, r_data in enumerate(result):
                    inflag = True
                    self.ui.pb_report_pdf.setEnabled(True)
                    self.ui.pb_report_excel.setEnabled(True)
                    self.ui.report_tableWidget.insertRow(r_num)
                    r_data = list(r_data)
                    row = []
                    for i in range(len(r_data)):

                        if nwen[i] == 1:
                            row.append(r_data[i])

                    self.pdfTableData.append(row)
                    for i in range(len(row)):

                        self.ui.report_tableWidget.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))
            elif sortusing == 'code2':
                result = c.execute(
                    """SELECT SerialNo,ReportDate,ReportTime,code1_no,code2_no,code3_no,code4_no,code5_no, header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=? AND code2_no=?""",
                    (d,sortname))
                for r_num, r_data in enumerate(result):
                    inflag = True
                    self.ui.pb_report_pdf.setEnabled(True)
                    self.ui.pb_report_excel.setEnabled(True)
                    self.ui.report_tableWidget.insertRow(r_num)
                    r_data = list(r_data)
                    row = []
                    for i in range(len(r_data)):

                        if nwen[i] == 1:
                            row.append(r_data[i])

                    self.pdfTableData.append(row)
                    for i in range(len(row)):

                        self.ui.report_tableWidget.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))
            elif sortusing == 'code3':
                result = c.execute(
                    """SELECT SerialNo,ReportDate,ReportTime,code1_no,code2_no,code3_no,code4_no,code5_no, header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=? AND code3_no=?""",
                    (d,sortname))
                for r_num, r_data in enumerate(result):
                    inflag = True
                    self.ui.pb_report_pdf.setEnabled(True)
                    self.ui.pb_report_excel.setEnabled(True)
                    self.ui.report_tableWidget.insertRow(r_num)
                    r_data = list(r_data)
                    row = []
                    for i in range(len(r_data)):

                        if nwen[i] == 1:
                            row.append(r_data[i])

                    self.pdfTableData.append(row)
                    for i in range(len(row)):

                        self.ui.report_tableWidget.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))
            elif sortusing == 'code4':
                result = c.execute(
                    """SELECT SerialNo,ReportDate,ReportTime,code1_no,code2_no,code3_no,code4_no,code5_no, header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=? AND code4_no=?""",
                    (d,sortname))
                for r_num, r_data in enumerate(result):
                    inflag = True
                    self.ui.pb_report_pdf.setEnabled(True)
                    self.ui.pb_report_excel.setEnabled(True)
                    self.ui.report_tableWidget.insertRow(r_num)
                    r_data = list(r_data)
                    row = []
                    for i in range(len(r_data)):

                        if nwen[i] == 1:
                            row.append(r_data[i])

                    self.pdfTableData.append(row)
                    for i in range(len(row)):

                        self.ui.report_tableWidget.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))
            elif sortusing == 'code5':
                result = c.execute(
                    """SELECT SerialNo,ReportDate,ReportTime,code1_no,code2_no,code3_no,code4_no,code5_no, header1,header2,header3,header4,header5,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=? AND code5_no=?""",
                    (d,sortname))
                for r_num, r_data in enumerate(result):
                    inflag = True
                    self.ui.pb_report_pdf.setEnabled(True)
                    self.ui.pb_report_excel.setEnabled(True)
                    self.ui.report_tableWidget.insertRow(r_num)
                    r_data = list(r_data)
                    row = []
                    for i in range(len(r_data)):

                        if nwen[i] == 1:
                            row.append(r_data[i])

                    self.pdfTableData.append(row)
                    for i in range(len(row)):

                        self.ui.report_tableWidget.setItem(r_num, i, QtWidgets.QTableWidgetItem(str(row[i])))

        if inflag == False:
            self.showErrormsg("", "Data not available")

        c.close()
        conn.close()
    def createPdf(self):
        self.uniquenum +=1
        self.ui.pb_report_pdf.setEnabled(False)
        inch = 55
        pgsize = (20 * inch, 10 * inch)
        dt = datetime.now()
        d = dt.strftime("%d%m%y")
        t = dt.strftime("%H%M%S")
        doc = SimpleDocTemplate("WB_"+str(d)+str(t)+str(self.uniquenum)+".pdf", pagesize=pgsize)
        elements = []
        t = Table(self.pdfTableData)
        t.setStyle(TableStyle(
            [
                ('BACKGROUND', (0, 0), (-1, 0), colors.brown),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.yellow),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),

                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ('GRID', (0, 0), (-1, -1), 2, colors.black)
            ]
        ))
        elements.append(t)
        doc.build(elements)
    def createExcel(self):
        self.uniquenum += 2
        self.ui.pb_report_excel.setEnabled(False)
        dt = datetime.now()

        d = dt.strftime("%d%m%y")
        t = dt.strftime("%H%M%S")
        workbook = xlsxwriter.Workbook('WB_'+ str(d) + str(t) + str(self.uniquenum) + '.xlsx')


        worksheet = workbook.add_worksheet("My sheet")


        for r_num, r_data in enumerate(self.pdfTableData):
            for c_num, c_data in enumerate(r_data):
                worksheet.write(r_num, c_num, c_data)


        workbook.close()
class Serial(QThread):
    def __init__(self):
        super(Serial, self).__init__()

    WeightUpdate = pyqtSignal(str)

    def decode(self, x):
        try:
            i = 0
            num = x[2:7]
            dpoint = int(x[0])
            rnum = str(num[::-1])
            n = len(rnum)
            res = ''
            while i < n:
                if i == dpoint:
                    res += '.'
                    res += rnum[i]

                else:
                    res += rnum[i]
                i += 1
            w = res[::-1]
            if w[0] == '0':
                w = w[1::]
            return w
        except:
            pass

    def run(self):
        conn = sqlite3.connect("WeighBridge.db")
        c = conn.cursor()
        result = c.execute("SELECT Comm,BaudRate FROM T_CommSettings")
        for i,data in enumerate(result):
            comm = str(data[0]).upper()
            bdrate = int(data[1])
        c.close()
        conn.close()

        try:

            ip = serial.Serial(port=comm, baudrate=bdrate, bytesize=8, parity=serial.PARITY_NONE,
                               stopbits=serial.STOPBITS_ONE)
            print(comm)

            while ip.isOpen():

                l = str(ip.read(13))

                val = l[2:15]
                # print(val)
                x = val[4:11]
                weight = self.decode(x)

                self.WeightUpdate.emit(str(weight))
        except :
            pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")


