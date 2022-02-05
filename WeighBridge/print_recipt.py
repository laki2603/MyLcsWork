# imports module
import os
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle,Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A5,letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas as canvas2
from datetime import *

companyname = "LCS control pvt ltd"
contact = "0123456789"
date = date.today()
time = datetime.now().strftime("%H:%M:%S")
Sno = "1"
material ="coal"
gross = "100"
net = "200"
vechicle_no = "TN 05 A 9877"
Amount = "200"
MOP = "phonepay"
Txn = "abcdefgh"
status = "success"
Agent = "kabilan"


def PDF():
    canvas = canvas2.Canvas("recipt.pdf", pagesize=letter)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 12)
    canvas.drawString(280, 750, "INVOICE")
    canvas.line(50, 740, 580, 740)  # FROM TOP 1ST LINE
    canvas.drawString(260, 720, companyname)
    canvas.line(50, 715, 580, 715)
    canvas.drawString(60, 695, "CHENNAI")
    canvas.drawString(500, 695, contact)
    canvas.line(50, 690, 580, 690)
    canvas.drawString(450, 720, "DATE : " + str(date))
    canvas.line(50, 740, 50, 50)  # LEFT LINE
    # canvas.line(400, 640, 400, 50)  # MIDDLE LINE
    canvas.line(580, 740, 580, 50)  # RIGHT LINE

    #### left data
    canvas.drawString(100, 650, "S.NO")
    canvas.drawString(150, 650,  ": "+Sno)
    canvas.drawString(100, 630, "Material" )
    canvas.drawString(150, 630, ": "+material)
    canvas.drawString(100, 610, "Gross" )
    canvas.drawString(150, 610, ": "+gross)
    canvas.drawString(100, 590, "Amount")
    canvas.drawString(150, 590, ": "+Amount)
    canvas.drawString(100, 570, "txn id" )
    canvas.drawString(150, 570, ": "+Txn)

    #### right data
    canvas.drawString(300, 650, "Vehicle_no")
    canvas.drawString(400, 650, ": " + vechicle_no)
    canvas.drawString(300, 630, "Agent")
    canvas.drawString(400, 630, ": " + Agent)
    canvas.drawString(300, 610, "NET.wt")
    canvas.drawString(400, 610, ": " + net)
    canvas.drawString(300, 590, "Mode of payment")
    canvas.drawString(400, 590, ": " + MOP)
    canvas.drawString(300, 570, "Status")
    canvas.drawString(400, 570, ": " + status)
    # canvas.drawString(475, 615, 'TOTAL AMOUNT')
    # canvas.drawString(100, 615, 'PRODUCT')
    # canvas.line(50, 600, 580, 600)  # FROM TOP 3rd LINE
    # canvas.drawString(60, 550, "productpdf")
    # canvas.drawString(500, 550, "amountpdf")
    # TOTAL = int(34) * ((int("12")) / 100)
    # canvas.drawString(60, 500, "SERVICE TAX (" + "staxpdf" + "%)")
    # canvas.drawString(500, 500, str(TOTAL))
    # canvas.line(50, 100, 580, 100)  # FROM TOP 4th LINE
    # canvas.drawString(60, 80, " TOTAL AMOUNT")
    # canvas.drawString(500, 80, str("finalstaxpdf"))
    # canvas.line(50, 50, 580, 50)  # FROM TOP LAST LINE
    canvas.save()

# print(date.today(),datetime.now().strftime("%H:%M:%S"))
# # data which we are going to display as tables
# DATA = [
#     ["","","LCS"],
#     ["chennai","","","7894561230"],
#     ["S.NO:","     ","Vechicle:","    "],
#     ["Material:","    ","Agent:","    "],
#     ["Gross:","    ","NET:","    "],
#     ["Amount:","    ","Mode of txn:","    "],
#     ["txn id:","    ","Status:","     "]
# ]
#
# # creating a Base Document Template of page size A4
# pdf = SimpleDocTemplate("receipt.pdf", pagesize=A5)
#
# # standard stylesheet defined within reportlab itself
# styles = getSampleStyleSheet()
#
# # fetching the style of Top level heading (Heading1)
# title_style = styles["Heading1"]
#
# # 0: left, 1: center, 2: right
# title_style.alignment = 1
#
# # creating the paragraph with
# # the heading text and passing the styles of it
# title = [Paragraph("LCS CONTROL PVT LTD ", title_style),
#             Paragraph("chennai    1234567890"),
#          ]
#
#
# # creates a Table Style object and in it,
# # defines the styles row wise
# # the tuples which look like coordinates
# # are nothing but rows and columns
# style = TableStyle(
#     [
#         ("BOX", (0, 0), (-1,-1), 1, colors.black),
#         ("GRID", (0, 2), (-1, -1), 1, colors.black),
#         ("GRID", (0, 1), (4, 0), 1, colors.black),
#         ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
#         ("ALIGN", (0, 0), (0, 0), "CENTER"),
#         ("BACKGROUND", (0, 0), (-1, -1), colors.beige),
#     ]
# )
#
# s = Spacer(1,2)
#
# # creates a table object and passes the style to it
# table = Table(DATA, style=style)
# # final step which builds the
# # actual pdf putting together all the elements
# pdf.build([table])


PDF()
os.startfile("recipt.pdf")