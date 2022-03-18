# from reportlab.pdfgen import canvas
# import os
# from PyQt5.QtWidgets import *
# from PyQt5.uic import *
# import sys
# class ui(QWidget):
#     def __init__(self):
#         super(ui, self).__init__()
#         loadUi("testCordinates.ui",self)
#         self.show()
#         self.pushButton.clicked.connect(self.createPdfReciept)
#
#     def createPdfReciept(self):
#         from reportlab.lib.units import cm, inch
#         # self.conn = sqlite3.connect("WeighBridge.db")
#         # self.c = self.conn.cursor()
#         # result = self.c.execute("SELECT * FROM T_Printer")
#         # name ,x ,y = [] ,[] ,[]
#         # for data in result:
#         #     name.append(data[0])
#         #     a = round(int(data[1] ) /37.8)
#         #     b = round(int(data[2] ) /37.8)
#         #     x.append(a)
#         #     y.append(b)
#
#         # dimensions = (int(self.width) * cm, int(self.height) * cm)
#         w = 20
#         dimensions = (20 * 37.8, 30 * 37.8)
#         print(dimensions)
#         x = self.x.text()
#         y = self.y.text()
#         c = canvas.Canvas("reciept.pdf" ,pagesize=dimensions)
#         # c.setPageSize((int(self.width),int(self.height)))
#         # for i in range(len(x)):
#         #     c.drawString(x[i],y[i],name[i])
#         #     print(x[i],y[i],name[i],sep=" ")
#         c.drawString(int(x), 30 * 37.8 - int(y), "x")
#         c.save()
#         os.startfile("reciept.pdf")
#         # os.system()
#         # self.c.close()
#         # self.conn.close()
#
# if __name__ == '__main__':
#
#     app = QApplication(sys.argv)
#
#     myApp = ui()
#     try:
#         sys.exit(app.exec_())
#     except SystemExit:
#         print('Closing Window...')
# import os
# import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import cm
#
# pdf_file = 'hello_world_cm.pdf'
#
# can = canvas.Canvas(pdf_file,pagesize=(20*37.8, 30*37.8))
# can.drawString(2 * 37.8, 20 * 37.8, "Hello World!")
# print((20*37.8, 30*37.8))
# can.showPage()
# can.save()
# os.startfile('hello_world_cm.pdf')
# from PyPDF2 import PdfFileReader, PdfFileWriter
# import io
# file_path = 'reciept.pdf'
# pdf = PdfFileReader(file_path)
#
# with open('Lecture Note.txt', 'w') as f:
#     for page_num in range(pdf.numPages):
#         # print('Page: {0}'.format(page_num))
#         pageObj = pdf.getPage(page_num)
#
#         try:
#             txt = pageObj.extractText()
#             print(txt)
#             for line in io.StringIO(txt):
#                 f.write(line)
#
#                 print(line)
#         except:
#             pass
#         else:
#             f.write('Page {0}\n'.format(page_num+1))
#     f.close()
# import os
# os.startfile("reciept.pdf","print")
# import pytesseract
# from pdf2image import convert_from_path
# poppler_path = R'...\pdf2image_poppler\Release-22.01.0-0\poppler-22.01.0\Library\bin'
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# images = convert_from_path('reciept.pdf', poppler_path=poppler_path)
# ocr_text = pytesseract.image_to_string(images[0])
# print(ocr_text)
# from io import StringIO
#
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfparser import PDFParser
#
# output_string = StringIO()
# with open('Aaaaaaaaa.pdf', 'rb') as in_file:
#     parser = PDFParser(in_file)
#     doc = PDFDocument(parser)
#     rsrcmgr = PDFResourceManager()
#     device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     for page in PDFPage.create_pages(doc):
#         interpreter.process_page(page)
#
# print(output_string.getvalue())


# import docx2txt
# my_text = docx2txt.process("Aaaaaaaaa.docx")
# print(my_text)
import os
fo = open("Reciept.txt", "r")
print(len(fo.readlines())
      )
# os.startfile("foo.txt","print")