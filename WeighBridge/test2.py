import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5 import QtWidgets
from PyQt5.Qt import QAbstractItemView
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import sqlite3
import serial
import serial.tools.list_ports
import threading
from datetime import datetime


import LoginWindow
from uitest import Ui_MainWindow

class LoginWindowcls(QObject):
    def __init__(self):
        super().__init__()
        self.main_window = QMainWindow()
        self.lui = LoginWindow.Ui_MainWindow()
        self.lui.setupUi(self.main_window)
        self.lui.le_passWord.setEchoMode(QLineEdit.Password)
        self.lui.pb_login.clicked.connect(self.CheckUser)
        self.main_window.show()


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



class UI:
    def __init__(self):
        ###  Ui setup
        self.main_window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.ui.stackedWidgetMain.setCurrentWidget(self.ui.Home)

        self.lws = LoginWindowcls()
        self.lws.LoginUpdate.connect(self.login)

        # self.serial = Serial()
        # self.serial.start()

        ### DataBase setup
        # self.connection = sqlite3.connect("WeighBridge.db")
        # self.cursor = self.connection.cursor()

        ### Declaring variables
        self.idList = []
        self.userList = []
        self.passwordList = []
        self.adminList = []
        self.activeList = []
        self.t1 = threading.Thread(target=self.ShowDate)
        self.t1.start()
        self.DownloadDataFromUserAccountTable()

        ## Setting Up MainPage
        #self.serial.WeightUpdate.connect(self.WeightDisplay)
        # self.ShowDate()
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

        ## Setting up Vehicle ReEntry Page
        self.ui.pb_VehicleReEntry_close_3.clicked.connect(self.showHome)

        ## Setting up Parameter Settings Page
        self.setCancelSaveAddDelete()
        self.CodesLeDefault()

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

        self.ui.stackedWidgetSettings.setCurrentWidget(self.ui.CommPortSettings)

        self.ui.pb_settings_close.clicked.connect(self.showHome)

        self.ui.pb_settings_search.clicked.connect(self.findPorts)
        self.ui.pb_CommPortSettings.clicked.connect(self.showCommPortSettings)
        self.ui.pb_HeaderSettings.clicked.connect(self.showHeaderSettings)
        self.ui.pb_UserAccountSettings.clicked.connect(self.showUserAccountSettings)

        self.ui.pb_UserAccountSettings.setHidden(True)
        self.ui.pb_HeaderSettings.setHidden(True)

                 ### User Account Settings
        self.ActiveGrp = QtWidgets.QButtonGroup()
        self.AdminGrp = QtWidgets.QButtonGroup()

        self.ActiveGrp.addButton(self.ui.rb_settings_activeYes)
        self.ActiveGrp.addButton(self.ui.rb_settings_activeNo)
        self.AdminGrp.addButton(self.ui.rb_settings_adminYes)
        self.AdminGrp.addButton(self.ui.rb_settings_adminNo)

        self.ui.tw_settings_users.setColumnWidth(0,100)
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

        # self.DownloadDataFromUserAccountTable()

        # self.conn = sqlite3.connect('WeighBridge.db')
        # self.c = self.conn.cursor()
        # cmd = "SELECT User FROM T_UserAccountSettings"
        # result = self.c.execute(cmd)
        # ButtonNames = []
        # for name in result:
        #     ButtonNames.append(name[0])
        # self.c.close()
        # self.conn.close()

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

    def showErrormsg(self,title,msg):
        QMessageBox.information(None,title,msg)
    def login(self,admin):
        self.Admin = admin
        if self.Admin == "1":
            self.AdminUnMask()
        self.main_window.show()

    # Functions used in main page
    def showHome(self):
        self.ui.stackedWidgetMain.setCurrentWidget(self.ui.Home)
    def ShowDate(self):
        while True:
            DateTime = datetime.now()
            date = DateTime.date()
            time_ = DateTime.strftime("%H:%M:%S")
            self.ui.lb_DateDisplay.setText(str(date))
            self.ui.lb_TimeDisplay.setText(str(time_))
    def WeightDisplay(self, w):
        self.ui.lb_home_WeightDisplay.setText(w)

    # Functions used in Vehicle Entry page
    def showVehicleEntry(self):
        self.ui.stackedWidgetMain.setCurrentWidget(self.ui.VehicleEntry)
        self.getLableNameFromDB()
        self.setParameters()

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
                    self.ui.combo_VehicleEntry_agentName.setHidden(False)
                else:
                    self.ui.lb_VehicleEntry_code2_agentName.setHidden(True)
                    self.ui.combo_VehicleEntry_agentName.setHidden(True)
                if ex:
                    self.ui.lb_VehicleReEntry_code2_agentName_3.setHidden(False)
                else:
                    self.ui.lb_VehicleReEntry_code2_agentName_3.setHidden(True)
            elif i ==2 :
                if en:self.ui.lb_VehicleEntry_code3_placeOfLoading.setHidden(False)
                else:self.ui.lb_VehicleEntry_code3_placeOfLoading.setHidden(True)
                if ex:self.ui.lb_VehicleReEntry_code3_placeOfLoading_3.setHidden(False)
                else:self.ui.lb_VehicleReEntry_code3_placeOfLoading_3.setHidden(True)
            elif i ==3 :
                if en:self.ui.lb_VehicleEntry_code4_moistureValue.setHidden(False)
                else:self.ui.lb_VehicleEntry_code4_moistureValue.setHidden(True)
                if ex:self.ui.lb_VehicleReEntry_code4_moistureValue.setHidden(False)
                else:self.ui.lb_VehicleReEntry_code4_moistureValue.setHidden(True)
            elif i ==4 :
                if en:self.ui.lb_VehicleEntry_code5_size.setHidden(False)
                else:self.ui.lb_VehicleEntry_code5_size.setHidden(True)
                if ex:self.ui.lb_VehicleReEntry_code5_size.setHidden(False)
                else:self.ui.lb_VehicleReEntry_code5_size.setHidden(True)
            elif i ==5 :
                continue
            elif i ==6 :
                if en:self.ui.lb_VehicleEntry_header2_supervisorName.setHidden(False)
                else:self.ui.lb_VehicleEntry_header2_supervisorName.setHidden(True)
                if ex:self.ui.lb_VehicleReEntry_header2_supervisorName_3.setHidden(False)
                else:self.ui.lb_VehicleReEntry_header2_supervisorName_3.setHidden(True)
            elif i ==7 :
                if en:self.ui.lb_VehicleEntry_header3_count.setHidden(False)
                else:self.ui.lb_VehicleEntry_header3_count.setHidden(True)
                if ex:self.ui.lb_VehicleReEntry_header3_count_3.setHidden(False)
                else:self.ui.lb_VehicleReEntry_header3_count_3.setHidden(True)
            elif i ==8 :
                if en:self.ui.lb_VehicleEntry_header4_msezDeliverNo.setHidden(False)
                else:self.ui.lb_VehicleEntry_header4_msezDeliverNo.setHidden(True)
                if ex:self.ui.lb_VehicleReEntry_header4_msezDeliverNo_3.setHidden(False)
                else:self.ui.lb_VehicleReEntry_header4_msezDeliverNo_3.setHidden(True)
            elif i ==9 :
                if en:self.ui.lb_VehicleEntry_header5_supplierChalanNo.setHidden(False)
                else:self.ui.lb_VehicleEntry_header5_supplierChalanNo.setHidden(True)
                if ex:self.ui.lb_VehicleReEntry_header5_supplierChalanNo_3.setHidden(False)
                else:self.ui.lb_VehicleReEntry_header5_supplierChalanNo_3.setHidden(True)



        self.c.close()
        self.conn.close()
    def getLableNameFromDB(self):
        self.conn = sqlite3.connect('WeighBridge.db')
        self.c = self.conn.cursor()
        names = []
        ens = []
        exs = []
        result = self.c.execute("SELECT Name,EN_ED,EX_ED FROM T_CodeAndHeader")
        for name,en,ex in result:
            names.append(name)
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
    # Functions used in Vehicle ReEntry page
    def showVehicleReEntry(self):
        self.ui.stackedWidgetMain.setCurrentWidget(self.ui.VehicleExit)
        self.getLableNameFromDB()
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
                print(codes[cd])
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


        print(self.en_ed)
        print(self.ex_ed)


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
        print("here ",self.Code1code)
        print("row ",row)
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

    def showCommPortSettings(self):
        self.ui.stackedWidgetSettings.setCurrentWidget(self.ui.CommPortSettings)
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
        self.ui.combo_settings_CommPortDisplay.addItems(self.ports)
        #self.s = self.ui.combo_settings_CommPortDisplay.setCurrentText()

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

        print("yes")
        for id,user,password,active,admin in result:
            self.idList.append(id)
            self.userList.append(user)
            self.passwordList.append(password)
            self.activeList.append(active)
            self.adminList.append(admin)
        self.setButtonName()
        print(self.userList[0])
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

        self.ui.lb_header1.setText(headers[0])
        self.ui.lb_header2.setText(headers[1])
        self.ui.lb_header3.setText(headers[2])
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
            self.ui.lb_header1.setText(header1)
            self.c.execute("UPDATE T_HeaderSettings SET Header=? WHERE Sno=?", (header1,1))
        if len(header2)>1:
            self.ui.lb_header2.setText(header2)
            self.c.execute("UPDATE T_HeaderSettings SET Header=? WHERE Sno=?", (header2, 2))
        if len(header3)>1:
            self.ui.lb_header3.setText(header3)
            self.c.execute("UPDATE T_HeaderSettings SET Header=? WHERE Sno=?", (header3, 3))
        self.conn.commit()
        self.c.close()
        self.conn.close()

    # Functions used in Report page
    def showReport(self):
        self.ui.stackedWidgetMain.setCurrentWidget(self.ui.Report)

class Serial(QThread):
    def __init__(self):
        super(Serial, self).__init__()

    WeightUpdate = pyqtSignal(str)

    def decode(self, x):
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

    def run(self):
        ip = serial.Serial(port="COM5", baudrate=9600, bytesize=8, parity=serial.PARITY_NONE,
                           stopbits=serial.STOPBITS_ONE)

        while True:
            l = str(ip.read(13))

            val = l[2:15]
            # print(val)
            x = val[4:11]
            weight = self.decode(x)
            self.WeightUpdate.emit(str(weight))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # loginwindow = LoginWindowcls()
    ui = UI()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")