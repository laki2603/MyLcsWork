
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QImage, QFont
from PrinterSettings import *
from PyQt5 import uic
import sys
from PyQt5.QtWidgets import *
import cv2
import sqlite3

from reportlab.pdfgen import canvas
import os
class PrinterFormat(QWidget):
    def __init__(self):
        super().__init__()
        self.my_widget = QtWidgets.QWidget()
        self.printerUi =Ui_Form()

        # self.my_widget.setWindowFlag(Qt.FramelessWindowHint)
        self.printerUi.setupUi(self.my_widget)
        self.printerUi.groupBox.setHidden(True)
        self.printerUi.stackedWidget.setCurrentWidget(self.printerUi.MainPage)
        self.printerUi.lb_WorkingPrinterImage.setScaledContents(True)
        self.printerUi.pb_next.clicked.connect(self.ParameterPage)
        self.printerUi.pb_draw.clicked.connect(self.DrawingPage)
        self.printerUi.pb_browse.clicked.connect(self.browseImage)
        self.printerUi.pb_saveGeometry.clicked.connect(self.SaveGeometry)
        self.printerUi.pb_Go.clicked.connect(self.GetNoOfParamters)
        self.printerUi.pb_close.clicked.connect(self.ParameterPage)
        self.printerUi.pb_pdf.clicked.connect(self.createPdfReciept)
        self.printerUi.pb_pdf_outside.clicked.connect(self.createPdfReciept)
        # self.image = QImage("PrinterFormat/img1.png")
        self.pixmap = QPixmap("PrinterFormat/img1.png")
        self.begin, self.destination = QPoint(), QPoint()
        # self.printerUi.lb_WorkingPrinterImage.setPixmap(QPixmap(self.pixmap))
        self.printerUi.pb_save.clicked.connect(self.getRectangleGeometry)
        self.printerUi.pb_Preview.clicked.connect(self.preview)
        self.printerUi.pb_reDraw.clicked.connect(self.reDraw)
        self.printerUi.lb_WorkingPrinterImage.paintEvent = self.paint_Event
        self.printerUi.lb_WorkingPrinterImage.mousePressEvent = self.mouse_PressEvent
        self.printerUi.lb_WorkingPrinterImage.mouseMoveEvent = self.mouse_MoveEvent
        self.printerUi.lb_WorkingPrinterImage.mouseReleaseEvent = self.mouse_ReleaseEvent
        self.createTable()
        # self.createPdfReciept()

    def showErrormsg(self, title, msg):
        QMessageBox.information(None, title, msg)

    def createTable(self):
        self.conn = sqlite3.connect("WeighBridge.db")
        self.c = self.conn.cursor()


        self.c.execute("""CREATE TABLE IF NOT EXISTS "T_Printer" (
                                "Name"	TEXT,
                                "X"	TEXT,
                                "Y"	TEXT,
                                "Width"	TEXT,
	                            "Height" TEXT
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
    def Show(self):
        self.my_widget.show()

    def ParameterPage(self):
        self.printerUi.stackedWidget.setCurrentWidget(self.printerUi.ParametersPage)

    def SaveGeometry(self):


        self.width = self.printerUi.le_width.text()
        self.height = self.printerUi.le_height.text()
        startpt = self.printerUi.le_startPoint.text()
        endpt = self.printerUi.le_endPoint.text()
        self.w = round(int(self.width)*37.8)
        self.h = round(int(self.height)*37.8)

        print(self.h)
        # self.st = round(int(startpt)*37.8)
        # self.ed = round(int(endpt)*37.8)
    def DrawingPage(self):
        try:
            self.getTheParameterDetails()
            if self.openDrawingFlag == True:
                self.printerUi.pb_save.setEnabled(True)
                self.printerUi.stackedWidget.setCurrentWidget(self.printerUi.DrawingPage)

        except:
            self.showErrormsg("","Enter the Fields")


    def GetNoOfParamters(self):
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

    def getTheParameterDetails(self):
        self.openDrawingFlag = False
        for i in range(len(self.RadioButtonList)):
            if self.RadioButtonList[i].isChecked():
                self.openDrawingFlag = True
                self.txt = self.LineEditList[i].text()
                self.LineEditList[i].setReadOnly(True)
                self.RadioButtonList[i].setCheckable(False)

    def browseImage(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        imgPath = fname[0]
        img = cv2.imread(imgPath)
        img = cv2.resize(img,(950,481),cv2.INTER_AREA)
        cv2.imwrite(imgPath,img)
        self.pixmap = QPixmap(imgPath)
        self.pixmap.scaled(100,100,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.printerUi.lb_WorkingPrinterImage.setPixmap(QPixmap(self.pixmap))
        # self.printerUi.lb_WorkingPrinterImage.setScaledContents(True)
        cv.label.setGeometry(0,0,self.w,self.h)
        cv.label.setPixmap(QPixmap(self.pixmap))

    def paint_Event(self, event):
        # print(self.rect())
        painter = QPainter(self.printerUi.lb_WorkingPrinterImage)
        painter.drawPixmap(QPoint(), self.pixmap)

        if not self.begin.isNull() and not self.destination.isNull():
            # print("paintings")
            rect = QRect(self.begin, self.destination)
            self.geo = rect.getRect()

            painter.drawRect(rect.normalized())
            # self.printerUi.lb_WorkingPrinterImage.setPixmap(QPixmap(self.pixmap))

    def mouse_PressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            # print("press ",event.pos())
            self.begin = event.pos()
            self.destination = self.begin
            self.my_widget.update()

    def mouse_MoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            # print("move ",event.pos())
            self.destination = event.pos()
            self.my_widget.update()

    def mouse_ReleaseEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            rect = QRect(self.begin, self.destination)
            painter = QPainter(self.pixmap)
            painter.drawRect(rect.normalized())

            self.begin, self.destination = QPoint(), QPoint()
            self.my_widget.update()


    def getRectangleGeometry(self):
        self.printerUi.pb_save.setEnabled(False)
        self.createCanvas()

    def preview(self):
        cv.Show()
    def reDraw(self):
        self.printerUi.pb_save.setEnabled(True)
    def saveCoordinates(self,x,y):
        self.conn = sqlite3.connect("WeighBridge.db")
        self.c = self.conn.cursor()
        r = self.c.execute("""SELECT EXISTS(SELECT * FROM T_Printer WHERE Name=?);""",(self.txt,))
        for i in r:
            cmdType = i[0]
            # print(type(cmdType))
        if cmdType == 0:
            self.c.execute("INSERT INTO T_Printer (Name,X,Y,Width,Height) VALUES(?,?,?,?,?)",(self.txt, x, y, self.w, self.h))
        elif cmdType == 1:
            self.c.execute("UPDATE T_Printer SET X=?,Y=?,Width=?,Height=? WHERE Name=?",(x, y, self.w, self.h, self.txt))


        self.conn.commit()
        self.c.close()
        self.conn.close()

    def createCanvas(self):
        # cv = Canvas()
        x = round(self.geo[0]*self.w/950)
        y = round(self.geo[1]*self.h/481)
        # print("y",self.geo[1]," ",y)
        # print("x",self.geo[0]," ",x)
        cv.x,cv.y,cv.w,cv.h =x,y,self.geo[2],self.geo[3]
        cv.setGeometry(0,0,self.w,self.h)
        cv.createLabel(self.txt)
        self.saveCoordinates(x,y)
        # self.my_widget.hide()

    def createPdfReciept(self):
        import win32api
        import win32print
        from reportlab.lib.units import cm, inch

        defaultPrinter = win32print.GetDefaultPrinter()
        print(defaultPrinter)
        self.conn = sqlite3.connect("WeighBridge.db")
        self.c = self.conn.cursor()
        result = self.c.execute("SELECT * FROM T_Printer")
        name,x,y = [],[],[]
        for data in result:
            name.append(data[0])
            a = round(int(data[1]))
            b = round(int(data[2]))
            w = int(data[3])
            h = int(data[4])
            x.append(a)
            y.append(b)

        dimensions = (w, h)
        c = canvas.Canvas("reciept.pdf",pagesize=dimensions)
        c.setFont("Helvetica", 16)
        for i in range(len(x)):
            c.drawString(x[i],h - y[i],name[i])

        c.save()
        os.startfile('reciept.pdf')
        try:
            os.startfile("reciept.pdf","print")
        except Exception as e:
            self.showErrormsg("",str(e))

        self.c.close()
        self.conn.close()

class Canvas(QWidget):
    def __init__(self):
        super(Canvas, self).__init__()
        uic.loadUi("canvas.ui",self)
        self.x,self.y,self.w,self.h = 0,0,0,0
        # self.show()

    def createLabel(self,txt):
        lb = QLabel(txt,self)
        lb.setFont(QFont("Helvetica",16))
        lb.setAlignment(Qt.AlignTop)
        lb.setGeometry(self.x,self.y,self.w,self.h)
        # print(self.x," ",self.y)
        print("label created")
    def Show(self):
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    myApp = PrinterFormat()
    cv = Canvas()
    myApp.Show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

# r = self.c.execute("""SELECT EXISTS(SELECT * FROM T_Code1 WHERE Code=?);""",("m1",))
        # for i in r:
        #     print(i)