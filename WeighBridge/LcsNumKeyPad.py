import os
import sys
import time
from subprocess import *
from PyQt5.QtCore import QPoint, pyqtSignal, QEvent, QCoreApplication, QTimer
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QFont, QKeyEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QKeyEvent
from PyQt5 import QtCore

SourceDirectory = os.path.join(os.path.dirname(__file__), "../Images/KeyboardImages")


class LcsNumKeyPad(QDialog):
    KeyboardSignal = pyqtSignal(str, bool)
    path = ":/Icons/assets_keyboard/"

    proportion = 1

    size = [1024, 350]

    keyboard = []
    keyboard_keys = []
    keyboard_numbers_keys = []
    keyboard_symbols_keys = []
    keyboard_on = []
    keyboard_on_upper = []
    keyboard_off = []
    keyboard_off_upper = []

    keyboard_numbers = []
    keyboard_numbers_on = []
    keyboard_numbers_off = []

    keyboard_symbols = []
    keyboard_symbols_on = []
    keyboard_symbols_off = []

    h_row1 = None
    w_row1 = None
    h_row2 = None
    w_row2 = None
    h_row3 = None
    w_row3 = None
    h_row4 = None
    w_row4 = None
    h_row5 = None
    w_row5 = None
    v_container = None
    w_container = None

    __receiver = None

    oldPos = None
    selected = False

    button_caps_lock = None
    button_letters = None
    button_numbers = None
    button_symbols = None

    general_widget_letters = None
    general_widget_numbers = None
    general_widget_symbols = None
    general_container = None

    upper_case = False

    style_on = ""
    style_off = ""

    buttons_size = [44, 43]

    # Suba Added for Text
    GetLettersText = ""
    GetNumbersText = ""
    GetSymbolsText = ""

    def __init__(self):
        super(LcsNumKeyPad, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint| Qt.Popup)
        #self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: black;')

        # _size = [int(650*self.proportion), int(250*self.proportion)]
        self.oldPos = self.pos()
        self.selected = False

        self.upper_case = False

        self.flgLettersPressed = True
        self.flgNumbersPressed = False
        self.flgSymbolsPressed = False

        self.keyboard = []
        self.keyboard_keys = []
        self.keyboard_on = []
        self.keyboard_on_upper = []
        self.keyboard_off = []
        self.keyboard_off_upper = []

        self.keyboard_numbers = []
        self.keyboard_numbers_on = []
        self.keyboard_numbers_off = []

        self.keyboard_symbols = []
        self.keyboard_symbols_on = []
        self.keyboard_symbols_off = []

        self.h_row0 = QHBoxLayout()
        self.w_row0 = QWidget()
        self.h_row1 = QHBoxLayout()
        self.w_row1 = QWidget()
        self.h_row2 = QHBoxLayout()
        self.w_row2 = QWidget()
        self.h_row3 = QHBoxLayout()
        self.w_row3 = QWidget()
        self.h_row4 = QHBoxLayout()
        self.w_row4 = QWidget()
        self.h_row5 = QHBoxLayout()
        self.w_row5 = QWidget()
        self.v_container = QVBoxLayout()
        self.w_container = QWidget()
        self.general_widget_letters = QWidget()
        self.general_container = QStackedLayout()

        self.text_inputNum = QLineEdit()
        self.text_inputNum.setStyleSheet("QLineEdit { color:rgb(255, 255, 255) }")
        self.text_inputNum.setFont(QFont('TimesNewRoman', 15))
        self.text_inputNum.resize(700, 100)
        self.text_inputNum.setFixedWidth(1000)
        self.text_inputNum.setFixedHeight(40)

        self.button_backspace = QPushButton()
        self.button_backspace.setIcon(QIcon(SourceDirectory + '/backspace.png'))
        self.button_backspace.setIconSize(
            QSize(self.buttons_size[0], self.buttons_size[1]))
        # self.button_backspace.pressed.connect(self.pressed_close)

        self.button_Enter = QPushButton("Enter")
        self.button_Enter.pressed.connect(self.Pressed_Enter)
        self.button_Enter.setFont(QFont('Cambria', 16))

        self.button_clear = QPushButton("clr")
        self.button_clear.pressed.connect(self.Pressed_Clear)
        self.button_clear.setFont(QFont('Cambria', 20))
        self.button_space = QPushButton("Space")
        self.button_space.pressed.connect(self.Pressed_Space)
        self.button_space.setFont(QFont('Cambria', 15))

        self.button_Close = QPushButton()
        self.button_Close.setIcon(QIcon(SourceDirectory + '/hidekeyboard.png'))
        self.button_Close.setIconSize(
            QSize(self.buttons_size[0], self.buttons_size[1]))
        self.button_Close.pressed.connect(self.Pressed_Close)

        self.style_on = """
                    border-width: 1px;
                                border-radius: 5px;
                                border-color: rgb(169,248,253);
                                color: rgb(169,248,253);                                
                               background-color: rgb(102,144,158,2);
                """
        self.style_off = """
                  border-width: 1px;
                    border-radius: 5px;
                    border-color: rgb(169,248,253);
                    color: rgb(169,248,253);                                
                    background-color: rgb(102,144,158,2);
               """
        self.flgNumKeyIsActivated = False
        self.init_ui()
        self.counter = 0
        self.count = 5
        self.CheckIsActive = QTimer()
        self.CheckIsActive.setInterval(500)
        self.CheckIsActive.setSingleShot(False)
        self.CheckIsActive.timeout.connect(self.CheckKeyActive)
        self.CheckIsActive.start()
        
    def LinkToBuzzer(self):
        call("echo " + str(1) + " > /dev/buzzer", shell=True)
        time.sleep(0.1)
        call("echo " + str(0) + " > /dev/buzzer", shell=True)


    def CheckKeyActive(self):
        if self.flgNumKeyIsActivated:
            if not self.underMouse():
                self.counter += 1
                if self.counter >= self.count:
                    self.hide()
                    self.flgNumKeyIsActivated = False
                    self.CheckIsActive.stop()
                    self.counter = 0
            else:
                self.counter = 0

    def init_ui(self):
        self.set_up_keyboard_keys()
        self.set_up_keyboard_on()
        self.set_up_keyboard_off()
        self.set_up_keyboard()
        self.set_up_layout()

    def set_up_keyboard_keys(self):

        row_1 = [Qt.Key_1, Qt.Key_2, Qt.Key_3,Qt.Key_Slash ,Qt.Key_Backspace]

        row_2 = [Qt.Key_4, Qt.Key_5, Qt.Key_6,Qt.Key_Asterisk, Qt.Key_Backspace]

        row_3 = [Qt.Key_7, Qt.Key_8, Qt.Key_9,Qt.Key_Minus, Qt.Key_Left]
        row_4 = [Qt.Key_Aring, Qt.Key_0, Qt.Key_Aring,Qt.Key_Comma, Qt.Key_Aring]

        self.keyboard_keys = [row_1, row_2, row_3, row_4]

    def set_up_keyboard_on(self):
        # row_1 = ['◄', 'clr', 'backspace']
        row_1 = ['1', '2', '3','/','backspace']
        row_2 = ['4', '5', '6','*', 'clr']
        row_3 = ['7', '8', '9','-','Enter']
        row_4 = ['.', '0',',', ' ','KB']
        self.keyboard_on = [row_1, row_2, row_3, row_4]
        row_1 = ['1', '2', '3', '/', 'backspace']
        row_2 = ['4', '5', '6', '*', 'clr']
        row_3 = ['7', '8', '9', '-', 'Enter']
        row_4 = ['.', '0', ',', ' ', 'KB']
        self.keyboard_on_upper = [row_1, row_2, row_3, row_4]

    def set_up_keyboard_off(self):
        row_1 = ['1', '2', '3', '/', 'backspace']
        row_2 = ['4', '5', '6', '*', 'clr']
        row_3 = ['7', '8', '9', '-', 'Enter']
        row_4 = ['.', '0', ',', ' ', 'KB']
        self.keyboard_off = [row_1, row_2, row_3, row_4]
        row_1 = ['1', '2', '3', '/', 'backspace']
        row_2 = ['4', '5', '6', '*', 'clr']
        row_3 = ['7', '8', '9', '-', 'Enter']
        row_4 = ['.', '0', ',', ' ', 'KB']
        self.keyboard_off_upper = [row_1, row_2, row_3, row_4]

    def set_up_keyboard(self):

        self.keyboard = []
        normal_size = [int(180 * self.proportion), int(60 * self.proportion)]
        backspace_size1 = [int(122 * self.proportion), int(60 * self.proportion)]

        _size = [int(50 * self.proportion), int(50 * self.proportion)]

        style = """
                    border-width: 1px;
                     border-radius: 5px;
                    border-color: rgb(169,248,253);
                    color: rgb(169,248,253);                                
                    background-color: rgb(102,144,158,2); """

        self.button_backspace.setFixedSize(normal_size[0],
                                           normal_size[1])
        self.button_backspace.setStyleSheet(style)

        self.button_Enter.setFixedSize(normal_size[0],
                                       normal_size[1])
        self.button_Enter.setStyleSheet(style)

        self.button_clear.setFixedSize(normal_size[0],
                                       normal_size[1])
        self.button_clear.setStyleSheet(style)
        self.button_space.setFixedSize(normal_size[0],
                                       normal_size[1])
        self.button_space.setStyleSheet(style)

        self.button_Close.setFixedSize(normal_size[0],
                                       normal_size[1])
        self.button_Close.setStyleSheet(style)

        self.button_backspace.setCursor(QCursor(Qt.PointingHandCursor))

        self.button_clear.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_Close.setCursor(QCursor(Qt.PointingHandCursor))

        i, j = 0, 0
        for row in self.keyboard_on:
            row_n = []
            j = 0
            for key in row:
                if key == "backspace":
                    _size = normal_size
                elif key == "Enter":
                    _size = normal_size
                elif key == " ":
                    _size = normal_size
                elif key == "&123":
                    _size = backspace_size1
                elif key == "KB":
                    _size = normal_size
                else:
                    _size = normal_size
                if key == "Enter":
                    row_n.append(
                        self.button_Enter
                    )
                elif key == "clr":
                    row_n.append(
                        self.button_clear
                    )
                elif key == " ":
                    row_n.append(
                        self.button_space
                    )
                elif key == "KB":
                    row_n.append(
                        self.button_Close
                    )
                elif key == "backspace":
                    row_n.append(
                        KeyboardKey(
                            """
                                border-width: 1px;
                                border-radius: 5px;
                                border-color: rgb(169,248,253);
                                color: rgb(169,248,253);                                
                               background-color: rgb(102,144,158,2);
                            """,
                            self.keyboard_on[i][j], self.keyboard_off[i][j],
                            True,
                            _size,
                            self.__receiver,
                            self.keyboard_keys[i][j], self.keyboard_on[i][j]
                        )
                    )
                elif key == "Enter":
                    row_n.append(
                        KeyboardKey(
                            """
                                border-width: 5px;
                                border-radius: 5px;
                                border-color: white;
                                color: white;                                
                                background-color: rgb(37,43,52);
                            """,
                            self.keyboard_on[i][j], self.keyboard_off[i][j],
                            True,
                            _size,
                            self.__receiver,
                            self.keyboard_keys[i][j], self.keyboard_on[i][j]
                        )
                    )
                else:
                    row_n.append(
                        KeyboardKey(
                            """
                                 border-width: 1px;
                                border-radius: 5px;
                                border-color: rgb(169,248,253);
                                color: rgb(169,248,253);                                
                               background-color: rgb(102,144,158,2);
                            """,
                            self.keyboard_on[i][j], self.keyboard_off[i][j],
                            True,
                            _size,
                            self.__receiver,
                            self.keyboard_keys[i][j], self.keyboard_on[i][j]
                        )
                    )

                j += 1
            self.keyboard.append(row_n)
            i += 1

    def set_up_layout(self):
        self.setFixedSize(int(self.size[0] * self.proportion),
                          int(350 * self.proportion))
        self.setGeometry(0, 240, 1024, 350)

        self.v_container.setSpacing(0)
        self.v_container.setContentsMargins(1, 1, 1, 1)
        self.v_container.setAlignment(Qt.AlignTop)

        self.h_row1.setSpacing(27)
        self.h_row2.setSpacing(27)
        self.h_row3.setSpacing(27)
        self.h_row4.setSpacing(27)
        self.h_row5.setSpacing(27)

        self.h_row1.setContentsMargins(int(10 * self.proportion), 5, 0, 20)
        self.h_row2.setContentsMargins(int(10 * self.proportion), 5, 0, 20)
        self.h_row3.setContentsMargins(int(10 * self.proportion), 5, 0, 20)
        self.h_row4.setContentsMargins(int(10 * self.proportion), 5, 0, 20)
        self.h_row5.setContentsMargins(int(30 * self.proportion), 5, 0, 0)

        self.h_row0.setAlignment(Qt.AlignBottom)
        self.h_row1.setAlignment(Qt.AlignBottom)
        self.h_row2.setAlignment(Qt.AlignBottom)
        self.h_row3.setAlignment(Qt.AlignBottom)
        self.h_row4.setAlignment(Qt.AlignBottom)
        self.h_row5.setAlignment(Qt.AlignBottom)

        self.general_container.addWidget(self.general_widget_letters)
        self.general_widget_letters.setLayout(self.v_container)

        self.setLayout(self.general_container)
        self.v_container.addWidget(self.w_row0)
        self.v_container.addWidget(self.w_row1)
        self.v_container.addWidget(self.w_row2)
        self.v_container.addWidget(self.w_row3)
        self.v_container.addWidget(self.w_row4)
        self.v_container.addWidget(self.w_row5)
        self.w_row0.setLayout(self.h_row0)
        self.w_row1.setLayout(self.h_row1)
        self.w_row2.setLayout(self.h_row2)
        self.w_row3.setLayout(self.h_row3)
        self.w_row4.setLayout(self.h_row4)
        self.w_row5.setLayout(self.h_row5)

        style = """
            QWidget{               
                background-color: 'black';
            }
            QPushButton{
                 border:1px solid ;
                border-radius: 1px;
                border-color: rgb(169,248,253);
                color: rgb(169,248,253);                                
                background-color: rgb(102,144,158,2);
            }
	QLineEdit{
                 border:1px solid ;
                border-radius: 1px;
                border-color: rgb(169,248,253);
                color: rgb(169,248,253);                                
                background-color: rgb(102,144,158,2);
            }
        """
        self.w_row0.setStyleSheet(style)
        self.w_row1.setStyleSheet(style)
        self.w_row2.setStyleSheet(style)
        self.w_row3.setStyleSheet(style)
        self.w_row4.setStyleSheet(style)
        self.w_row5.setStyleSheet(style)

        self.h_row0.addWidget(self.text_inputNum)
        for key in self.keyboard[0]:
            self.h_row1.addWidget(key)
        for key in self.keyboard[1]:
            self.h_row2.addWidget(key)
        for key in self.keyboard[2]:
            self.h_row3.addWidget(key)
        for key in self.keyboard[3]:
            self.h_row4.addWidget(key)
        # for key in self.keyboard[4]:
        #     self.h_row5.addWidget(key)

        self.h_row1.addStretch(1)
        self.h_row2.addStretch(1)
        self.h_row3.addStretch(1)
        self.h_row4.addStretch(1)
        self.h_row5.addStretch(1)

    def set_receiver(self, receiver):
        self.__receiver = receiver
        self.update_key_receivers()

    def update_key_receivers(self):
        for row in self.keyboard:
            for key in row:
                if isinstance(key, KeyboardKey):
                    key.set_receiver(self.__receiver)
        for row in self.keyboard_numbers:
            for key in row:
                if isinstance(key, KeyboardKey):
                    key.set_receiver(self.text_inputNum)
        for row in self.keyboard_symbols:
            for key in row:
                if isinstance(key, KeyboardKey):
                    key.set_receiver(self.text_inputNum)

    def Pressed_Enter(self):
        self.LinkToBuzzer()
        self.GetData = self.text_inputNum.text()
        self.KeyboardSignal.emit(self.GetData, self.flgLettersPressed)
        self.hide()
        self.text_inputNum.setText("")

    def Pressed_Clear(self):
        self.LinkToBuzzer()
        self.text_inputNum.setText("")

    def Pressed_Space(self):
        self.LinkToBuzzer()
        self.text_inputNum.setText(self.text_inputNum.text() + " ")

    def Pressed_Close(self):
        self.LinkToBuzzer()
        self.text_inputNum.setText("")
        self.hide()

    def update_keyboard(self):
        i, j = 0, 0
        for row in self.keyboard:
            j = 0
            for key in row:
                if isinstance(key, KeyboardKey):
                    if self.upper_case:
                        key.set_str_key(self.keyboard_on_upper[i][j])
                    else:
                        key.set_str_key(self.keyboard_on[i][j])
                j += 1
            i += 1

    def resizeEvent(self, event):
        super(LcsNumKeyPad, self).resizeEvent(event)

    def mousePressEvent(self, evt):
        self.selected = True
        self.oldPos = evt.globalPos()
        super(LcsNumKeyPad, self).mousePressEvent(evt)

    def mouseMoveEvent(self, evt):
        if self.selected:
            delta = QPoint(evt.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = evt.globalPos()

    def mouseReleaseEvent(self, event):
        self.selected = False
        super(LcsNumKeyPad, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        for row in self.keyboard:
            for key in row:
                if isinstance(key, KeyboardKey):
                    if key.get_key() == event.key():
                        if key.get_key() == '197':
                            self.hide()
                        else:
                            key.key_pressed()
        for row in self.keyboard_numbers:
            for key in row:
                if isinstance(key, KeyboardKey):
                    if key.get_key() == event.key():
                        if key.get_key() == '197':
                            self.hide()
                        else:
                            key.key_pressed()
        for row in self.keyboard_symbols:
            for key in row:
                if isinstance(key, KeyboardKey):
                    if key.get_key() == event.key():
                        if key.get_key() == '197':
                            self.hide()
                        else:
                            key.key_pressed()

    def keyReleaseEvent(self, event):
        for row in self.keyboard:
            for key in row:
                if isinstance(key, KeyboardKey):
                    if key.get_key() == event.key():
                        key.key_released2()
        for row in self.keyboard_numbers:
            for key in row:
                if isinstance(key, KeyboardKey):
                    if key.get_key() == event.key():
                        key.key_released2()
        for row in self.keyboard_symbols:
            for key in row:
                if isinstance(key, KeyboardKey):
                    if key.get_key() == event.key():
                        key.key_released2()


class KeyboardKey(QPushButton):
    __path = ""

    __size = [30, 30]
    __style = ""
    __icon_on = ""
    __icon_off = ""
    __auto_repeat = True
    __receiver = None
    __key = None
    __str_key = None

    __upper_case = False

    def __init__(self, style, str_icon_on, str_icon_off, auto_repeat, size,
                 receiver, key, str_key):
        super(KeyboardKey, self).__init__()
        self.__size = size
        self.__style = style
        self.__icon_on = str_icon_on
        self.__icon_off = str_icon_off
        self.__auto_repeat = auto_repeat
        self.__receiver = receiver
        self.__key = key
        self.__str_key = str_key
        self.set_up_button(style, str_icon_on, str_icon_off, auto_repeat, size,
                           receiver, key, str_key)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def LinkToBuzzer(self):
        call("echo " + str(1) + " > /dev/buzzer", shell=True)
        time.sleep(0.1)
        call("echo " + str(0) + " > /dev/buzzer", shell=True)

    def set_up_button(self, style, str_icon_on, str_icon_off, auto_repeat,
                      size, receiver, key, str_key):
        self.__size = size
        self.__style = style
        self.__icon_on = str_icon_on
        self.__icon_off = str_icon_off
        self.__auto_repeat = auto_repeat
        self.__receiver = receiver
        self.__key = key
        self.__str_key = str_key
        if str_key not in ['◄', '►', 'backspace', ' ', 'Enter', 'KB']:
            self.setText(str_key)
            self.setFont(QFont('Cambria', 18))
        elif str_key == 'clr':
            self.setText('clr')
            self.setFont(QFont('Cambria', 20))
        elif str_key == ' ':
            self.setText('space')
        self.setFixedSize(size[0], size[1])
        self.setStyleSheet(style)
        self.setIconSize(QSize(size[0], size[1]))
        self.setAutoRepeat(auto_repeat)
        # pix_map = QPixmap(self.__path + str_icon_off + ".png")
        # self.setMask(pix_map.mask())
        if self.__str_key == 'backspace':
            self.setIcon(QIcon(SourceDirectory + '/backspace.png'))
        elif self.__str_key == '◄':
            self.setIcon(QIcon(SourceDirectory + '/leftarrow.png'))
        elif self.__str_key == '►':
            self.setIcon(QIcon(SourceDirectory + '/rightarrow.png'))
        else:
            self.setIcon(QIcon(self.__path + str_icon_off + ".png"))
        self.pressed.connect(self.key_pressed)
        self.released.connect(self.key_released)

    def set_receiver(self, receiver):
        self.__receiver = receiver

    def key_pressed(self):
        self.LinkToBuzzer()
        self.setStyleSheet("""
                            border-width: 5px;
                            border-radius: 5px;
                            color: white;
                            background-color: rgb(0, 187, 255);
                        """)
        if self.__str_key == 'KB':  # Suba Added to remove kB
            self.__str_key = ''

    def key_released(self):
        self.setStyleSheet(self.__style)
        if self.__str_key == "&&":
            self.__str_key = "&"
        event = QKeyEvent(QEvent.KeyPress, self.__key, Qt.NoModifier,
                          self.__str_key, False)
        QCoreApplication.postEvent(self.__receiver, event)

    def key_released2(self):
        self.setStyleSheet(self.__style)

    def set_str_key(self, key):
        self.__str_key = key
        if self.__str_key not in ['KB', '▲A', 'A▲', '◄', '►', 'backspace', ' ', 'Enter']:
            self.setText(self.__str_key)

    def get_name(self):
        if self.__str_key == 'KB':
            self.__str_key = ''
        return self.__str_key

    def get_key(self):
        return self.__key

    def keyPressEvent(self, evt):
        event = QKeyEvent(QEvent.KeyPress, evt.key(), evt.modifiers(),
                          evt.text(), False)
        QCoreApplication.postEvent(self.__receiver, event)
        evt.ignore()

    def keyReleaseEvent(self, event):
        super(KeyboardKey, self).keyReleaseEvent(event)
        event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = LcsNumKeyPad()
    mw.show()
    sys.exit(app.exec())
