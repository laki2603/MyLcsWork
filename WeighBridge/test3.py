import sqlite3


# conn = sqlite3.connect("WeighBridge.db")
# c = conn.cursor()
# user = "admin"
# password = "admin"
# id = 1
# cmd1 = "UPDATE T_UserAccountSettings SET User=?, Password=?  WHERE ID=? "
# ip = (user,password,id)
# c.execute(cmd1, (user,password,id))
# conn.commit()
# cmd2 = "SELECT ID,User,Password FROM T_UserAccountSettings"
# l = c.execute(cmd2)
#
#
# for id,name,pw in l:
#     print(str(name))
#     print(id)
#     print(pw)
# c.close()
# conn.close()

# code1 = "MATERIA"
# code2 = "AGENT NAME"
# code3 = "PLACE OF LOADING"
# code4 = "MOISTURE VALUE"
# code5 = "SIZE"
# codes = {"code1":code1, "code2":code2, "code3":code3, "code4":code4, "code5":code5}

# headers = {
# "header1" : "VEHICLE",
# "header2" : "SUPERVISOR NAME",
# "header3" : "COUNT",
# "header4" : "MSEZ DELIVERY NO",
# "header5" : "SUPPLIER CHALLAN NO"
# }
# codes = {"lcs": "lcs control",
#          "HP":"Hindustan Plate",
#          "Sntl":"Sintal",
#          "Hcl": "Hindustan Corp"}
# for i in codes:
#
#
#     # c.execute("INSERT INTO T_Code5 (Code,Name) VALUES (?,?) ",(i,codes[i]))
#     pass
# conn.commit()
# result = c.execute("SELECT Code FROM T_Code1")
#
#
conn = sqlite3.connect("WeighBridge.db")
c = conn.cursor()
# c.execute("INSERT INTO T_CommSettings (Id,Comm,BaudRate,Controller) VALUES (?,?,?,?)",(1,"com5",9600,"wt"))
# conn.commit()
values = (header1, header2, header3, header4, header5, code1, code2, code3, code4, code5, grosswt, grossunit, grosstime, grossdate,
          tarewt, tareunit, taretime, taredate, netwt, amount, serialno)
result = c.execute("UPDATE T_Entry SET header1=?,header2=?,header3=?,header4=?,header5=?,code1_no=?,code2_no=?,code3_no=?,code4_no=?,code5_no=?,grossWt=?,grossUnit=?,grossTime=?,grossDate=?,tareWt=?,tareUnit=?,tareTime=?,tareDate=?,netWt=?,Amount=? WHERE SerialNo=?",values)
print(result)
if result:

    for i,data in enumerate(result):
        print("s")
        print(data)
        if not data[15]:
            print("s")
else:
    print("no data")
c.close()
conn.close()

# con = sqlite3.connect("myDb.db")
# c = con.cursor()
# c.execute("""CREATE TABLE "T_Code1" (
# 	"Code"	TEXT,
# 	"Name"	TEXT
# );""")
# con.commit()
# c.close()
# con.close()
# s = ""
# if s:
#     print('ok')
# else:
#     print('not ok')

