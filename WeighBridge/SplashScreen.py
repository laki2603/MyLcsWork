import os
import sys
import time

from test2 import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

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


FromSplash, _ = loadUiType(os.path.join(os.path.dirname(__file__), "SplashScreen.ui"))
SplashImage = os.path.join(os.path.dirname(__file__), "SplashScreen.jpeg")


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

    # @pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i)
        if i == 100:
            self.hide()
            objmain = UI()


            # objmain.show()


    def handle_data(self):
        print(self)

    def UiComponents(self):
        self.progressBar.setStyleSheet("QProgressBar"
                                       "{"
                                       "border: solid grey;"
                                       "border-radius: 6px;"
                                       " color: black; "
                                       "}"
                                       "QProgressBar::chunk "
                                       "{background-color: rgb(96, 135, 197);"
                                       "border-radius :6px;"
                                       "}")
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFont(QFont('MS Shell Dlg 2', 12))


def Main():
    app = QApplication(sys.argv)
    window = SplashScreen()
    window.show()
    app.exec_()


if __name__ == '__main__':
    try:
        Main()
    except Exception as why:
        print(why)
