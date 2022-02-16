from PyQt5.uic import loadUiType
from main import *
from PyQt5.QtGui import QFont


#
# class SplashScreen(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setFixedSize(1024, 600)
#         self.setWindowFlag(Qt.FramelessWindowHint)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.counter = 0
#         self.n = 100
#         self.initUI()
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.loading)
#         self.timer.start(30)
#     def initUI(self):
#         # layout to display splash scrren frame
#         layout = QVBoxLayout()
#         self.setLayout(layout)
#         # splash screen frame
#         self.frame = QFrame()
#         layout.addWidget(self.frame)
#         # splash screen title
#         self.title_label = QLabel(self.frame)
#         self.title_label.setObjectName('title_label')
#         self.title_label.resize(690, 120)
#         self.title_label.move(0, 5) # x, y
#         self.title_label.setText('LCS CONTROL PVT LTD')
#         self.title_label.setAlignment(Qt.AlignCenter)
#         # splash screen title description
#         self.description_label = QLabel(self.frame)
#         self.description_label.resize(690, 40)
#         self.description_label.move(0, self.title_label.height())
#         self.description_label.setObjectName('desc_label')
#         self.description_label.setText('<b>Weight_Bridge_Automation</b>')
#         self.description_label.setAlignment(Qt.AlignCenter)
#         # splash screen pogressbar
#         self.progressBar = QProgressBar(self.frame)
#         self.progressBar.resize(self.width() - 200 - 10, 50)
#         self.progressBar.move(100, 450) # self.description_label.y()+130
#         self.progressBar.setAlignment(Qt.AlignCenter)
#         self.progressBar.setFormat('%p%')
#         self.progressBar.setTextVisible(True)
#         self.progressBar.setRange(0, self.n)
#         self.progressBar.setValue(20)
#         # spash screen loading label
#         self.loading_label = QLabel(self.frame)
#         self.loading_label.resize(self.width() - 10, 50)
#         self.loading_label.move(0, self.progressBar.y() + 70)
#         self.loading_label.setObjectName('loading_label')
#         self.loading_label.setAlignment(Qt.AlignCenter)
#         self.loading_label.setText('Loading...')
#     def loading(self):
#         # set progressbar value
#         self.progressBar.setValue(self.counter)
#         # stop progress if counter
#         # is greater than n and
#         # display main window app
#         if self.counter >= self.n:
#             self.timer.stop()
#             # self.close()
#             app.setStyleSheet("")
#             self.WindowApp = UI()
#             time.sleep(1)
#             self.close()
#
#
#         self.counter += 1
# # class WindowApp(QMainWindow):
# #     def __init__(self):
# #         super().__init__()
# #         self.setWindowTitle("Main Window")
# #         self.setGeometry(400, 200, 320, 315)
# #         self.show()
# app = QApplication(sys.argv)
# app.setStyleSheet('''
#         #title_label {
#             font-size: 50px;
#             color: white;
#         }
#         #desc_label {
#             font-size: 20px;
#             color: #c2ced1;
#         }
#         #loading_label {
#             font-size: 30px;
#             color: #e8e8eb;
#         }
#         QFrame {
#             background-color: #625899;
#             color: #c8c8c8;
#         }
#         QProgressBar {
#             background-color: #000000;
#             color: #c8c8c8;
#             border-style: none;
#             border-radius: 5px;
#             text-align: center;
#             font-size: 25px;
#         }
#         QProgressBar::chunk {
#             border-radius: 5px;
#             background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #44DD44);
#         }
# ''')
# splash = SplashScreen()
# splash.show()
# sys.exit(app.exec_())

SplashImage = "WeighBridgeScreens\splash\SplashScreen.png"
FromSplash, _ = loadUiType("SplashScreen.ui")

class ThreadProgress(QThread):
    mysignal = pyqtSignal(int)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        i = 0
        while i < 101:
            time.sleep(0.1)
            self.mysignal.emit(i)
            i += 5

class SplashScreen(QMainWindow, FromSplash):
    def __init__(self, parent=None):
        super(SplashScreen, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.SetSplashImage()
        self.UiComponents()
        self.ProgressBar()

    def SetSplashImage(self):
        pixmap = QPixmap(SplashImage)
        self.splah_image.setPixmap(pixmap.scaled(1024, 600))

    def ProgressBar(self):
        progress = ThreadProgress(self)
        progress.mysignal.connect(self.progress)
        progress.start()

    @pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i)
        if i == 100:

            self.objmain = UI()
            self.hide()

    def handle_data(self):
        print(self)

    def UiComponents(self):
        self.progressBar.setStyleSheet("QProgressBar"
                                       "{"
                                       "border: solid grey;"
                                       "border-radius: 6px;"
                                       # "color: black; "
                                       "}"
                                       "QProgressBar::chunk "
                                       "{background-color: rgb(96, 135, 197);"
                                       "border-radius :6px;"
                                       "}"
                                       )
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFont(QFont('MS Shell Dlg 2', 12))


def Main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""QLabel
            {
            color: White;
            }
            QMessageBox QLabel
            {
            color: black
            }
            QLineEdit
            {
            boder-style: outset;
            border-wiidth: 2px;
            border-radius: 8px;
            border-color: red;
            font:  16px;
            }
            """
                      )
    window = SplashScreen()
    window.show()
    app.exec_()


if __name__ == '__main__':
    Main()