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
conn = sqlite3.connect('WeighBridge.db')
c = conn.cursor()
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
codes = {"lcs": "lcs control",
         "HP":"Hindustan Plate",
         "Sntl":"Sintal",
         "Hcl": "Hindustan Corp"}
for i in codes:


    # c.execute("INSERT INTO T_Code5 (Code,Name) VALUES (?,?) ",(i,codes[i]))
    pass
conn.commit()
# result = c.execute("SELECT EN_ED, EX_ED FROM T_CodeAndHeader")
# for i,en in enumerate(result):
#     print(i,en[1],sep = " ")
c.close()
conn.close()
