import os
import sqlite3
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from tabulate import tabulate
from datetime import datetime
# # i=55
# # pgsize= (20*i , 10*i)
# # doc = SimpleDocTemplate("simple_table.pdf", pagesize=pgsize)
# # # container for the 'Flowable' objects
# # elements = []
# # titles = ["serialno","self.names[5]", "self.names[6]", "self.names[7]", "self.names[8]", "self.names[9]",
# #                                                               "self.names[0]", "self.names[1]", "self.names[2]", "self.names[3]", "self.names[4]",
# #                                                               "grosswt","tarewt", "netwt", "amount"]
# # data= [titles,titles]
# # t=Table(data)
# # t.setStyle(TableStyle(
# #         [
# #             ('BACKGROUND',(0,0),(-1,0),colors.brown),
# #             ('TEXTCOLOR',(0,0),(-1,0),colors.yellow),
# #             ('ALIGN',(0,0),(-1,-1),'CENTER'),
# #             ('FONTNAME',(0,0),(-1,0),'Courier-Bold'),
# #
# #             ('FONTSIZE',(0,0),(-1,-1),8),
# #             ('FONTSIZE', (0, 0), (-1, 0), 9),
# #             ('BOTTOMPADDING',(0,0),(-1,0),12),
# #             ('BOX',(0,0),(-1,-1),2,colors.black),
# #             ('GRID',(0,0),(-1,-1),2,colors.black)
# #         ]
# #         ))
# # elements.append(t)
# # # write the document to disk
# # doc.build(elements)
# # os.startfile("simple_table.pdf")
#
#
# # conn = sqlite3.connect("WeighBridge.db")
# # c = conn.cursor()
# # user = "admin"
# # password = "admin"
# # id = 1
# # cmd1 = "UPDATE T_UserAccountSettings SET User=?, Password=?  WHERE ID=? "
# # ip = (user,password,id)
# # c.execute(cmd1, (user,password,id))
# # conn.commit()
# # cmd2 = "SELECT ID,User,Password FROM T_UserAccountSettings"
# # l = c.execute(cmd2)
# #
# #
# # for id,name,pw in l:
# #     print(str(name))
# #     print(id)
# #     print(pw)
# # c.close()
# # conn.close()
#
# # code1 = "MATERIA"
# # code2 = "AGENT NAME"
# # code3 = "PLACE OF LOADING"
# # code4 = "MOISTURE VALUE"
# # code5 = "SIZE"
# # codes = {"code1":code1, "code2":code2, "code3":code3, "code4":code4, "code5":code5}
#
# # headers = {
# # "header1" : "VEHICLE",
# # "header2" : "SUPERVISOR NAME",
# # "header3" : "COUNT",
# # "header4" : "MSEZ DELIVERY NO",
# # "header5" : "SUPPLIER CHALLAN NO"
# # }
# # codes = {"lcs": "lcs control",
# #          "HP":"Hindustan Plate",
# #          "Sntl":"Sintal",
# #          "Hcl": "Hindustan Corp"}
# # for i in codes:
# #
# #
# #     # c.execute("INSERT INTO T_Code5 (Code,Name) VALUES (?,?) ",(i,codes[i]))
# #     pass
# # conn.commit()
# # result = c.execute("SELECT Code FROM T_Code1")
# #
# #
# # conn = sqlite3.connect("WeighBridge.db")
# # c = conn.cursor()
# # # c.execute("INSERT INTO T_CommSettings (Id,Comm,BaudRate,Controller) VALUES (?,?,?,?)",(1,"com5",9600,"wt"))
# # # conn.commit()
# # # values = (header1, header2, header3, header4, header5, code1, code2, code3, code4, code5, grosswt, grossunit, grosstime, grossdate,
# # #           tarewt, tareunit, taretime, taredate, netwt, amount, serialno)
# # # result = c.execute("UPDATE T_Entry SET header1=?,header2=?,header3=?,header4=?,header5=?,code1_no=?,code2_no=?,code3_no=?,code4_no=?,code5_no=?,grossWt=?,grossUnit=?,grossTime=?,grossDate=?,tareWt=?,tareUnit=?,tareTime=?,tareDate=?,netWt=?,Amount=? WHERE SerialNo=?",values)
# # print(result)
# # if result:
# #
# #     for i,data in enumerate(result):
# #         print("s")
# #         print(data)
# #         if not data[15]:
# #             print("s")
# # else:
# #     print("no data")
# # c.close()
# # conn.close()
# #
# # # con = sqlite3.connect("myDb.db")
# # # c = con.cursor()
# # # c.execute("""CREATE TABLE "T_Code1" (
# # # 	"Code"	TEXT,
# # # 	"Name"	TEXT
# # # );""")
# # # con.commit()
# # # c.close()
# # # con.close()
# # # s = ""
# # # if s:
# # #     print('ok')
# # # else:
# # #     print('not ok')
# #
# # def insertIntoCod1Table(self):
# #     if self.ui.tableWidget_1.rowCount() == 0:
# #         self.conn = sqlite3.connect('WeighBridge.db')
# #         self.c = self.conn.cursor()
# #
# #         result = self.c.execute("SELECT Code,Name FROM T_Code1")
# #         self.ui.tableWidget_1.setRowCount(0)
# #         self.ui.tableWidget_1.setHorizontalHeaderLabels(['Code', 'Name'])
# #         header = self.ui.tableWidget_1.horizontalHeader()
# #         header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
# #         header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
# #         for r_num, r_data in enumerate(result):
# #             self.ui.tableWidget_1.insertRow(r_num)
# #             for c_num, c_data in enumerate(r_data):
# #                 self.ui.tableWidget_1.setItem(r_num, c_num, QtWidgets.QTableWidgetItem(str(c_data)))
# #         # self.ui.tableWidget_1.setSelectionMode(QAbstractItemView.MultiSelection)
# #
# #         self.c.close()
# #         self.conn.close()
# #     else:
# #         pass
# # from datetime import timedelta, date

# # sd = '22-01-22'
# # ed = '25-01-22'
# # sd = list(map(int,sd.split('-')))
# # ed = list(map(int, ed.split('-')))
# # sd[2] = sd[2]+2000
# # ed[2] = ed[2]+2000
# # dates = []
# # # def daterange(date1, date2):
# # #     for n in range(int ((date2 - date1).days)+1):
# # #         yield date1 + timedelta(n)
# #
# # # start_dt = date(sd[2], sd[1], sd[0])
# # # end_dt = date(ed[2], ed[1], ed[0])
# # # for dt in daterange(start_dt, end_dt):
# # #     print(dt.strftime("%d-%m-%y"))
# # start_date = date(sd[2], sd[1], sd[0])
# # end_date = date(ed[2], ed[1], ed[0])
# #
# # delta = end_date - start_date   # returns timedelta
# # print(delta)
# # for i in range(delta.days + 1):
# #     print(timedelta(days=i))
# #     day = start_date + timedelta(days=i)
# #     dates.append(day.strftime("%d-%m-%y"))
# #
# #
# # print(dates)
# # for date in dates:
# #     result = c.execute("""SELECT SerialNo, ReportDate, header1,header2,header3,header4,header5,code1_no,code2_no,code3_no,code4_no,code5_no,grossWt,tareWt,netWt,Amount FROM T_Entry WHERE ReportDate=?""",(date,))
# #     for d in result:
# #         print(d)
#
#

# # date = "25-01-22"
# # conn = sqlite3.connect('WeighBridge.db')
# # c = conn.cursor()
# # cd = 'ssx'
# # header1 = []
# # header2 = []
# # result = c.execute("SELECT header1,header2 FROM T_Entry WHERE SerialNo =? AND header1=?",(1,cd))
# # for i, data in enumerate(result):
# #     header1.append(data[0])
# #     header2.append(data[1])
# # print(header1,header2)
# # c.close()
# # conn.close()
# # print('\033[1m'+"this ins")
# # file = open("Exit.txt",'w')
# # a=10
# # mydata = [( '\033[1m'+"Nikhil "+'\033[0m' , a),
# #           ("Ravi", "Kanpur"),
# #           ("Manish", "Ahmedabad"),
# #           ("Prince", "Bangalore")]
# # file.write(tabulate(mydata,tablefmt="grid"))
# # print(tabulate(mydata))
# # os.startfile("Exit.txt")
# import xlsxwriter
# dt = datetime.now()
# d = dt.strftime("%d%m%y")
# t = dt.strftime("%H%M%S")
#
# workbook = xlsxwriter.Workbook('excelFile'+str(d)+str(t)+str(1)+'.xlsx')
#
# # By default worksheet names in the spreadsheet will be
# # Sheet1, Sheet2 etc., but we can also specify a name.
# worksheet = workbook.add_worksheet("My sheet")
#
# # Some data we want to write to the worksheet.
# scores = (
#     ['f', 1000],
#     ['rahul', 100],
#     ['priya', 300],
#     ['harshita', 50],
# )
#
# # Start from the first cell. Rows and
# # columns are zero indexed.
#
#
# # Iterate over the data and write it out row by row.
# for r_num,r_data  in enumerate(scores):
#     for c_num,c_data in enumerate(r_data):
#         worksheet.write(r_num,c_num, c_data)
#
# # os.startfile('excel')
# workbook.close
# conn = sqlite3.connect("WeighBridge.db")
# c = conn.cursor()
# name = ["Amount","DateTime","GunnyBag","Unit"]
# values = [True,False,True,"kg"]
# for i in range(len(name)):
#     c.execute("UPDATE T_OtherSettings SET Status=? WHERE Name=?",(values[i],name[i]))
#     # pass
# conn.commit()
# c.close()
# conn.close()
# a="ada"
# b="12"
# if not (a or b):
#     print("ss")
# conn = sqlite3.connect("WeighBridge.db")
# c = conn.cursor()
# c.execute("""CREATE TABLE IF NOT EXISTS "T_Code1" (
# 	"Code"	TEXT,
# 	"Name"	TEXT
# );""")
# c.execute("""SELECT EXISTS (SELECT * FROM T_Code1 WHERE Code="C1")
#             BEGIN
#              UPDATE T_Code1 SET Code="C1",Name="new" WHERE Code="C1"
#             END
#             ELSE
#             BEGIN
#              INSERT INTO T_Code1 (Code,Name) VALUES ("c1","CODESS")
#             END;""")
# r = c.execute("""SELECT EXISTS(SELECT * FROM T_Code1 WHERE Code=?);""",("s1",))
#
# for i in r:
#     print(i)
from PyQt5.QtWidgets import *
import sys

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)

        # auto complete options
        names = ["Apple", "Alps", "Berry", "Cherry" ]
        completer = QCompleter(names)

        # create line edit and add auto complete
        self.lineedit = QLineEdit()
        self.lineedit.setCompleter(completer)
        layout.addWidget(self.lineedit, 0, 0)

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())