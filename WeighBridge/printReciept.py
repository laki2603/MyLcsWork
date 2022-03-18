

import sqlite3
import os
from PyQt5.QtWidgets import *

from printer import *

class Format(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = QtWidgets.QWidget()
        self.printerUi = Ui_Form()
        self.printerUi.setupUi(self.widget)
        self.printerUi.stackedWidget.setCurrentWidget(self.printerUi.MainPage)
        self.printerUi.pb_draw.clicked.connect(self.DrawingPage)
        self.printerUi.pb_Go.clicked.connect(self.GetNoOfParamters)
        self.printerUi.pb_close.clicked.connect(self.ParameterPage)
        self.printerUi.pb_save.clicked.connect(self.Save)
        self.printerUi.pb_reset.clicked.connect(self.Reset)
        self.printerUi.pb_reciept.clicked.connect(self.Reciept)
        self.printerUi.pb_print.clicked.connect(self.printer)
        self.createTable()

    def showErrormsg(self, title, msg):
        QMessageBox.information(None, title, msg)
    def createTable(self):
        self.conn = sqlite3.connect("WeighBridge.db")
        self.c = self.conn.cursor()

        self.c.execute("""CREATE TABLE IF NOT EXISTS "T_Printer" (
                                "Name"	TEXT,
                                "Lines" TEXT,
                                "Spaces"	TEXT
                                
                            );""")
        self.c.close()
        self.conn.close()

    def DeleteTable(self):
        self.conn = sqlite3.connect("WeighBridge.db")
        self.c = self.conn.cursor()
        self.c.execute("DROP TABLE T_Printer")
        print("Deleted")
        self.c.close()
        self.conn.close()

    def ParameterPage(self):
        self.printerUi.stackedWidget.setCurrentWidget(self.printerUi.MainPage)

    def getTheParameterDetails(self):
        self.openDrawingFlag = False
        for i in range(len(self.RadioButtonList)):
            if self.RadioButtonList[i].isChecked():
                self.openDrawingFlag = True
                self.txt = self.LineEditList[i].text()
                self.LineEditList[i].setReadOnly(True)
                self.RadioButtonList[i].setCheckable(False)

    def DrawingPage(self):
        try:
            self.getTheParameterDetails()
            if self.openDrawingFlag == True:
                self.Reset()
                self.printerUi.stackedWidget.setCurrentWidget(self.printerUi.DrawingPage)

        except:
            self.showErrormsg("","Enter the Fields")

    def GetNoOfParamters(self):
        try:
            n = self.printerUi.le_ParameterQuantity.text()
            self.DeleteTable()
            self.createTable()
            formLayout = QFormLayout()
            grpBox = QGroupBox()
            self.LineEditList = []
            self.RadioButtonList = []
            for i in range(int(n)):

                self.LineEditList.append(QLineEdit())
                self.RadioButtonList.append(QRadioButton())
                formLayout.addRow(self.RadioButtonList[i],self.LineEditList[i])

            grpBox.setLayout(formLayout)
            # self.printerUi.scrollArea.setLayout(formLayout)
            self.printerUi.scrollArea.setWidget(grpBox)
            self.printerUi.scrollArea.setWidgetResizable(True)
            self.printerUi.scrollArea.setFixedHeight(319)
        except Exception as e:
            self.showErrormsg("",e)
    def Reset(self):
        self.printerUi.pb_save.setEnabled(True)
        self.printerUi.pb_close.setEnabled(False)
        self.printerUi.pb_reset.setEnabled(False)
        self.printerUi.le_lines.clear()
        self.printerUi.le_spaces.clear()
    def Save(self):
        try:
            self.printerUi.pb_save.setEnabled(False)
            self.printerUi.pb_close.setEnabled(True)
            self.printerUi.pb_reset.setEnabled(True)
            self.conn = sqlite3.connect("WeighBridge.db")
            self.c = self.conn.cursor()
            spaces = self.printerUi.le_spaces.text()
            lines = self.printerUi.le_lines.text()
            r = self.c.execute("""SELECT EXISTS(SELECT * FROM T_Printer WHERE Name=?);""", (self.txt,))
            for i in r:
                cmdType = i[0]
                # print(type(cmdType))
            if cmdType == 0:
                self.c.execute("INSERT INTO T_Printer (Name,Lines,Spaces) VALUES(?,?,?)",
                               (self.txt, lines, spaces))
            elif cmdType == 1:
                self.c.execute("UPDATE T_Printer SET Lines=?,Spaces=? WHERE Name=?",
                               (lines, spaces, self.txt))


            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception as e:
            self.showErrormsg("",e)
    def Reciept(self):
        try:
            self.conn = sqlite3.connect("WeighBridge.db")
            self.c = self.conn.cursor()
            r = self.c.execute("SELECT * FROM T_Printer")
            fo = open("Reciept.txt", "w")
            initial = 0
            for data in r:
                # fo.seek(0)
                name = data[0]
                lines = int(data[1]) - initial
                initial = lines-1
                spaces = int(data[2])
                for i in range(int(lines)-1):
                    fo.writelines("\n")
                for i in range(spaces):
                    fo.write(" ")
                fo.write(name)

            fo.close()
            os.startfile("Reciept.txt")
            self.c.close()
            self.conn.close()
        except Exception as e:
            self.showErrormsg("",str(e))

    def printer(self):
        try:
            os.startfile("Reciept.txt", "print")
        except Exception as e:
            self.showErrormsg("",str(e))
    def Show(self):
        self.widget.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    myApp = Format()
    myApp.Show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')