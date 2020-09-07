import socket
import threading
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import pickle
from collections import OrderedDict
import os,sys,random,string

messages = ""
username = ""
password = ""
msgslen = 0
shouldUpdate = False
newmsg = ""
login = False
regis = False
loginback = False
loginqmsg = False
regisqmsg = False
regisqmsgs = False
updateonlineusers = False
onlineuserslist = []
i = 255
j = 0
ireverse = False
jreverse = True
ioutputcolor = ""
joutputcolor = ""
flag1 = True
flag2 = False
flag3 = False
otherusername = ""
usermessages = []
usermessagesnames = []
usernameavatar = {}
appmsg = False
image = b''
imgtype = ""
appendimage = False
imageclientname = ""
snapflag = False

getSnap = False

finishsending = False

clientMessageMapper = []
clientMessageMapperIndex = []

arraybufflist = []
bufferList = []
ngif = 0

namefontdict = {}

current_group_name = "精神病院"

# Font, fontsize, background-color, font-color, border-color 
defaultFont = ["FZHTJW", 9, "#12b7f5", "white", "#12b7f5"]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("72.14.188.7", 1234))
#s.connect((socket.gethostname(), 1234))
HeaderSize = 10
recvsize = 20

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

    #def setupUi(self, MainWindow):
        self.setObjectName("MainWindow")
        self.setFixedSize(425, 327)
        self.setWindowIcon(QtGui.QIcon("qq_icon.png"))
        self.flag = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(self.flag)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background-color:white; border-radius:5px") 
        self.statusBar().hide()

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.backcolor=QtWidgets.QLabel(self.centralwidget)
        self.backcolor.setGeometry(QtCore.QRect(0,0,425,130))
        self.backcolor.setObjectName("label")
        
        self.closebutton = QtWidgets.QPushButton(self.centralwidget)
        self.closebutton.setGeometry(393, 0, 32, 32)
        self.closebutton.setObjectName("closebutton")
        self.closebutton.setStyleSheet("QPushButton:hover""{""background-color :#FF431B;""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.closebutton.clicked.connect(self.closeitself)


        self.minbutton = QtWidgets.QPushButton(self.centralwidget)
        self.minbutton.setGeometry(361, 0, 32, 32)
        self.minbutton.setObjectName("minbutton")
        self.minbutton.setStyleSheet("QPushButton:hover""{""background-color :rgba(255, 255, 255, 50);""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.minbutton.clicked.connect(self.MinimizeWindow)

        self.imagePath = "qq_logo.png"
        self.image = QtGui.QImage(self.imagePath)
        self.labelreal = QtWidgets.QLabel(self)
        self.labelreal.setGeometry(180,93,60,60)
        self.labelreal.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.labelreal.setScaledContents(True)
        self.labelreal.setStyleSheet("background-color: transparent")

        self.imagePathlogo_top_left = "qq_logo_top_left.png"
        self.imagelogo_top_left = QtGui.QImage(self.imagePathlogo_top_left)
        self.labellogo_top_left = QtWidgets.QLabel(self)
        self.labellogo_top_left.setGeometry(20,10,25,40)
        self.labellogo_top_left.setPixmap(QtGui.QPixmap.fromImage(self.imagelogo_top_left))
        self.labellogo_top_left.setScaledContents(True)
        self.labellogo_top_left.setStyleSheet("background-color:transparent")

        
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(95, 160, 240, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("账号")
        self.lineEdit.setFont(QtGui.QFont("Arial", 11))
        self.lineEdit.setTextMargins(22 ,0, 0, 0)
        self.lineEdit.setFrame(False)
        self.lineEdit.setStyleSheet("QLineEdit{""border-width: 0.5px; border-style: solid; border-color: white white grey white""}" "QLineEdit:hover{""border-width:1.3px; border-color: white white #0184b0 white""}")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(95, 200, 240, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setTextMargins(22 ,0, 0, 0)
        self.lineEdit_2.setFont(QtGui.QFont("Arial", 11))
        self.lineEdit_2.setPlaceholderText("密码")
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setStyleSheet("QLineEdit{""border-width: 0.5px; border-style: solid; border-color: white white grey white""}" "QLineEdit:hover{""border-width:1.3px; border-color: white white #0184b0 white""}")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(95, 270, 240, 40))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("QPushButton:hover""{""background-color : #4bace1;""}" "QPushButton""{""background-color:#009ce6; color: white; border-style:outset; border-width:1px; border-radius:5px; border-color:#01aef0; min-width:10em; padding: 6px;""}" "QPushButton:pressed""{""background-color:#2782bb""}")
        self.pushButton.setFont(QtGui.QFont("Arial", 10))
        self.pushButton.clicked.connect(self.saveinfo)

        self.imagePathusername = "qq_username"
        self.imageusername = QtGui.QImage(self.imagePathusername)
        self.labelusername = QtWidgets.QLabel(self)
        self.labelusername.setGeometry(100,163,20,25)
        self.labelusername.setPixmap(QtGui.QPixmap.fromImage(self.imageusername))
        self.labelusername.setScaledContents(True)

        self.imagePathlock = "qq_lock"
        self.imagelock = QtGui.QImage(self.imagePathlock)
        self.labellock = QtWidgets.QLabel(self)
        self.labellock.setGeometry(100,203,20,25)
        self.labellock.setPixmap(QtGui.QPixmap.fromImage(self.imagelock))
        self.labellock.setScaledContents(True)
       
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(5, 300, 73, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.register)
        self.pushButton_2.setStyleSheet("QPushButton{""border:none; color:grey""}" "QPushButton:hover{""color:black""}")
        self.pushButton_2.setFont(QtGui.QFont("Arial", 9))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 348, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.oldPos = self.pos()

        self.show()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def MinimizeWindow(self):
        self.showMinimized()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "QQ登录"))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.pushButton_2.setText(_translate("MainWindow", "注册账号"))
        self.closebutton.setText(_translate("closebutton", u'\u2715'))
        self.minbutton.setText(_translate("minbutton", u'\u2015'))

    def saveinfo(self):
        global username
        global password
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if len(username) != 0 and len(password) != 0:
            msg = 'L' + f'{len(username):<{HeaderSize}}' + username + f'{len(password):<{HeaderSize}}' + password
            try:
                s.send(bytes(msg,'utf-8'))
                print("sent msg to server")
            except:
                s.close()
        
    def update(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.closewindow)
        self.timer.timeout.connect(self.messagesbox)
        self.timer.start(100)

    def closeitself(self):
        global s
        s.close()
        QtCore.QCoreApplication.instance().quit()
        sys.exit()

    def closewindow(self):
        global login
        if login:
            QtCore.QCoreApplication.instance().quit()

    def register(self):
        global regis
        regis = True
        QtCore.QCoreApplication.instance().quit()

    
    def messagesbox(self):
        global i
        global j
        global ireverse
        global jreverse
        global ioutputcolor
        global joutputcolor
        icolor = ""
        jcolor = ""

        if not ireverse:
            i += 5
        else:
            i -= 5

        if jreverse:
            j += 5
        else:
            j -= 5
        icolor = hex(i).lstrip("0x").rstrip("L")
        jcolor = hex(j).lstrip("0x").rstrip("L")
        if len(icolor) == 1:
            ioutputcolor = "#FF000" + icolor
        if len(icolor) == 2:
            ioutputcolor = "#FF00" + icolor
        if len(jcolor) == 1:
            joutputcolor =  "#0" +jcolor + "00FF"
        if len(jcolor) == 2:
            joutputcolor = "#" + jcolor + "00FF"

        #self.backcolor.setStyleSheet("background-color:" + outputcolor)
        self.backcolor.setStyleSheet("background: qlineargradient( x1:0 y1:0, x2:1 y2:1, stop:0" + ioutputcolor + ", stop:1 " + joutputcolor +")")
        if len(icolor) == 3:
            ireverse = True
        if len(icolor) == 0:
            ireverse = False
        if len(jcolor) == 3:
            jreverse = False
        if len(jcolor) == 0:
            jreverse = True

        global newmsg
        global loginqmsg
        if loginqmsg:
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            loginqmsg = False
            msgbox = QtWidgets.QMessageBox()
            msgbox.setWindowTitle("Error")
            msgbox.setText(newmsg)
            msgbox.setIcon(QtWidgets.QMessageBox.Critical)
            msgbox.setStyleSheet("color: red; font-weight: bold; font: 16px")
            msgbox.setFont(QtGui.QFont("Times font", 20))
            msgbox.exec_()
        

        

class RegisterWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setFixedSize(450, 600)
        self.flag = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(self.flag)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        

        self.imagePathbackground = "qq_sign_up_background.png"
        self.imagebackground = QtGui.QImage(self.imagePathbackground)
        self.labelbackground = QtWidgets.QLabel(self)
        self.labelbackground.setGeometry(0,0,465,545)
        self.labelbackground.setPixmap(QtGui.QPixmap.fromImage(self.imagebackground))
        self.labelbackground.setScaledContents(True)

        self.imagePathbackground2 = "qq_sign_up_background2.png"
        self.imagebackground2 = QtGui.QImage(self.imagePathbackground2)
        self.labelbackground2 = QtWidgets.QLabel(self)
        self.labelbackground2.setGeometry(0,0,465,545)
        self.labelbackground2.setPixmap(QtGui.QPixmap.fromImage(self.imagebackground2))
        self.labelbackground2.setScaledContents(True)

        self.imagePathbackground3 = "qq_sign_up_back_ground3.png"
        self.imagebackground3 = QtGui.QImage(self.imagePathbackground3)
        self.labelbackground3 = QtWidgets.QLabel(self)
        self.labelbackground3.setGeometry(0,0,465,545)
        self.labelbackground3.setPixmap(QtGui.QPixmap.fromImage(self.imagebackground3))
        self.labelbackground3.setScaledContents(True)

        self.imagePathlogo_top_left = "qq_sign_up_logo.png"
        self.imagelogo_top_left = QtGui.QImage(self.imagePathlogo_top_left)
        self.labellogo_top_left = QtWidgets.QLabel(self)
        self.labellogo_top_left.setGeometry(0,-13,60,60)
        self.labellogo_top_left.setPixmap(QtGui.QPixmap.fromImage(self.imagelogo_top_left))
        self.labellogo_top_left.setScaledContents(True)
        self.labellogo_top_left.setStyleSheet("background-color:transparent")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(15,30,180,50))
        self.label.setObjectName("bigtext")
        self.label.setText("欢迎注册QQ")
        self.label.setFont(QtGui.QFont("Times font", 22))
        self.label.setStyleSheet(" font-weight: bold; color: black")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(15,70,220,30))
        self.label_2.setObjectName("smalltext")
        self.label_2.setText("每一天，乐在沟通。")
        self.label_2.setFont(QtGui.QFont("Times font", 18))
        self.label_2.setStyleSheet("color: black")


        self.closebutton = QtWidgets.QPushButton(self.centralwidget)
        self.closebutton.setGeometry(418, 0, 32, 32)
        self.closebutton.setObjectName("closebutton")
        self.closebutton.setStyleSheet("QPushButton:hover""{""background-color :#FF431B;""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.closebutton.clicked.connect(self.closeitself)

        self.minbutton = QtWidgets.QPushButton(self.centralwidget)
        self.minbutton.setGeometry(386, 0, 32, 32)
        self.minbutton.setObjectName("minbutton")
        self.minbutton.setStyleSheet("QPushButton:hover""{""background-color :rgba(255, 255, 255, 50);""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.minbutton.clicked.connect(self.MinimizeWindow)


        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(105, 260, 240, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("新账号")
        self.lineEdit.setFont(QtGui.QFont("Arial", 11))
        self.lineEdit.setTextMargins(5 ,0, 0, 0)
        self.lineEdit.setFrame(False)
        self.lineEdit.setStyleSheet("QLineEdit{""border-width: 0.5px; border-style: solid; border-color:#7c7d82  ""}" "QLineEdit:hover{""border-width:1.3px; border-color: #0184b0""}")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(105, 300, 240, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setTextMargins(5 ,0, 0, 0)
        self.lineEdit_2.setFont(QtGui.QFont("Arial", 11))
        self.lineEdit_2.setPlaceholderText("密码")
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setStyleSheet("QLineEdit{""border-width: 0.5px; border-style: solid; border-color:#7c7d82""}" "QLineEdit:hover{""border-width:1.3px; border-color: #0184b0 ""}")

        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(105, 340, 240, 30))
        self.lineEdit_3.setObjectName("lineEdit_2")
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setTextMargins(5 ,0, 0, 0)
        self.lineEdit_3.setFont(QtGui.QFont("Arial", 11))
        self.lineEdit_3.setPlaceholderText("确认密码")
        self.lineEdit_3.setFrame(False)
        self.lineEdit_3.setStyleSheet("QLineEdit{""border-width: 0.5px; border-style: solid; border-color:#7c7d82""}" "QLineEdit:hover{""border-width:1.3px; border-color: #0184b0""}")
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(105, 385, 240, 40))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("QPushButton:hover""{""background-color : #4bace1;""}" "QPushButton""{""background-color:#009ce6; color: white; border-style:outset; border-radius:5px; min-width:10em; padding: 6px;""}" "QPushButton:pressed""{""background-color:#2782bb""}")
        self.pushButton.setFont(QtGui.QFont("Arial", 12))
        self.pushButton.clicked.connect(self.saveinfo)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(155, 460, 75, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("QPushButton:hover""{""background-color : #7c7d82;""}" "QPushButton""{""background-color:#6b6e77; color: white; border-radius:5px; min-width:10em; padding: 6px;""}" "QPushButton:pressed""{""background-color:#2b2a30""}")
        self.pushButton_2.setFont(QtGui.QFont("Arial", 10))
        self.pushButton_2.clicked.connect(self.back)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 348, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.oldPos = self.pos()
        self.show()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "立即注册"))
        self.pushButton_2.setText(_translate("MainWindow", "登录"))
        self.closebutton.setText(_translate("closebutton", u'\u2715'))
        self.minbutton.setText(_translate("minbutton", u'\u2015'))

    def MinimizeWindow(self):
        self.showMinimized()

    def closeitself(self):
        global s
        s.close()
        QtCore.QCoreApplication.instance().quit()
        sys.exit()

    def changebackground(self):
        global flag1
        global flag2
        global flag3
        if flag1:
            self.labelbackground.raise_()
        if flag2:
            self.labelbackground2.raise_()
        if flag3:             
            self.labelbackground3.raise_()
        self.centralwidget.raise_()
        self.labellogo_top_left.raise_()
        



    def backgroundtimer(self):
        self.newtimer = QtCore.QTimer()
        self.newtimer.timeout.connect(self.changeflag)
        self.newtimer.timeout.connect(self.changebackground)
        self.newtimer.start(5000)

    def changeflag(self):
        global flag1
        global flag2
        global flag3
        if flag1 == True:
            flag1 = False
            flag2 = True
            flag3 = False
        elif flag2 == True:
            flag1 = False
            flag2 = False
            flag3 = True
        elif flag3 == True:
            flag1 = True
            flag2 = False
            flag3 = False
        

    def saveinfo(self):
        global newmsg
        global regisqmsg
        global username
        global password
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if len(username) != 0 and len(password) != 0:
            pass2 = self.lineEdit_3.text()
            if password != pass2:
                newmsg = "密码不匹配"
                regisqmsg = True
            else:
                msg = 'R' + f'{len(username):<{HeaderSize}}' + username + f'{len(password):<{HeaderSize}}' + password
                try:
                    s.send(bytes(msg,'utf-8'))
                    print("sent msg to server")
                except:
                    s.close()
        
    def update(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.closewindow)
        self.timer.timeout.connect(self.messagesbox)
        self.timer.timeout.connect(self.messagesboxs)
        self.timer.start(100)


    def closewindow(self):
        global login
        if login:
            QtCore.QCoreApplication.instance().quit()

    def back(self):
        global loginback
        loginback = True
        QtCore.QCoreApplication.instance().quit()

    def messagesbox(self):
        global newmsg
        global regisqmsg
        if regisqmsg:
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            regisqmsg = False
            msgbox = QtWidgets.QMessageBox()
            msgbox.setWindowTitle("Error")
            msgbox.setText(newmsg)
            msgbox.setIcon(QtWidgets.QMessageBox.Critical)
            msgbox.setStyleSheet("color: red; font-weight: bold; font: 16px")
            msgbox.setFont(QtGui.QFont("Times font", 20))
            msgbox.exec_()

    def messagesboxs(self):
        global newmsg
        global regisqmsgs
        if regisqmsgs:
            regisqmsgs = False
            msgbox = QtWidgets.QMessageBox()
            msgbox.setWindowTitle("Success")
            msgbox.setText(newmsg)
            msgbox.setIcon(QtWidgets.QMessageBox.Information)
            msgbox.setStyleSheet("color: Blue; font-weight: bold; font: 16px")
            msgbox.setFont(QtGui.QFont("Times font", 20))
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            msgbox.exec_()


CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        font_path = os.path.join(CURRENT_DIRECTORY, "FZHTJW.ttf")
        _id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if QtGui.QFontDatabase.applicationFontFamilies(_id) == -1:
            print("problem loading font")
            sys.exit(-1)
        font_path = os.path.join(CURRENT_DIRECTORY, "HanyiSentyCrayon.ttf")
        _id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if QtGui.QFontDatabase.applicationFontFamilies(_id) == -1:
            print("problem loading font")
            sys.exit(-1)
        font_path = os.path.join(CURRENT_DIRECTORY, "OzCaramel.ttf")
        _id = QtGui.QFontDatabase.addApplicationFont(font_path)
        if QtGui.QFontDatabase.applicationFontFamilies(_id) == -1:
            print("problem loading font")
            sys.exit(-1)
        self.setObjectName("MainWindow")
        self.setFixedSize(610, 770)
        self.flag = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(self.flag)
        self.setStyleSheet("background-color:white;")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.backcolor=QtWidgets.QLabel(self.centralwidget)
        self.backcolor.setGeometry(QtCore.QRect(0,0,610,40))
        self.backcolor.setObjectName("label")
        self.backcolor.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.backcolor.setStyleSheet("background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #4C8EFF , stop:1 #20D1FE)")

        self.grouptitle = QtWidgets.QLabel(self.centralwidget)
        self.grouptitle.setText(current_group_name)
        self.grouptitle.setStyleSheet("background-color:transparent; color:white;")
        self.grouptitle.setFont(QtGui.QFont("FZHTJW", 13))
        self.grouptitle.setGeometry(QtCore.QRect(250,5,100,30))
        self.grouptitle.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.grouptitle.setAlignment(QtCore.Qt.AlignCenter)

        self.closebutton = QtWidgets.QPushButton(self.centralwidget)
        self.closebutton.setGeometry(578, 0, 32, 32)
        self.closebutton.setObjectName("closebutton")
        self.closebutton.setStyleSheet("QPushButton:hover""{""background-color :#FF431B;""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.closebutton.clicked.connect(self.closeitself)

        self.minbutton = QtWidgets.QPushButton(self.centralwidget)
        self.minbutton.setGeometry(546, 0, 32, 32)
        self.minbutton.setObjectName("minbutton")
        self.minbutton.setStyleSheet("QPushButton:hover""{""background-color :rgba(255, 255, 255, 50);""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.minbutton.clicked.connect(self.MinimizeWindow)

        
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 90, 411, 571))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setStyleSheet("border-width:0.5px; min-width:1em;border-style:outset; border-color:grey")


        self.imagePath = "qq_logo.png"

        self.scrollarea = QtWidgets.QScrollArea(self.centralwidget)
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.vbox.addStretch()
        self.vbox.setSpacing(10)
        self.widget.setLayout(self.vbox)
        self.scrollarea.setGeometry(0,90,411,571)
        self.verticalScrollBar = QtWidgets.QScrollBar(QtCore.Qt.Vertical, self.scrollarea)
        self.scrollarea.setVerticalScrollBar(self.verticalScrollBar)
        #self.scrollarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.widget)
        self.scrollarea.setStyleSheet("""QScrollArea{border-width: 1px; border-style: solid; border-color: #EBEBEB #EBEBEB #EBEBEB #EBEBEB;}""" """QScrollBar { background-color: transparent; }""" )
        self.verticalScrollBar.setStyleSheet("""QScrollBar::vertical{border-color: transparent;border-width: 1px;border-style: outset;background-color: transparent;width: 10px;margin: 10px 0 10px 0;}""" """QScrollBar::handle:vertical {background-color:#cdcdcd ; border-style:outset; border-radius:3px}""" """QScrollBar::add-line:vertical {background-color: #cdcdcd;border: transparent; height: 10px;subcontrol-position: bottom;subcontrol-origin: margin; border-radius:3px}""" """QScrollBar::sub-line:vertical {background-color: #cdcdcd; border: transparent;height: 10px;subcontrol-position: top;subcontrol-origin: margin;border-radius:3px}""")

        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(411, 90, 200, 181))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_2.setText("群通知")
        self.textBrowser_2.setFont(QtGui.QFont("Times font", 10))
        self.textBrowser_2.setStyleSheet("padding-left:9px; border-width: 1px; border-style: solid; border-color: #EBEBEB #EBEBEB #EBEBEB white;")


        self.scrollarea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.widget_2 = QtWidgets.QWidget()
        self.vbox_2 = QtWidgets.QVBoxLayout()
        self.vbox_2.addStretch()
        self.widget_2.setLayout(self.vbox_2)
        self.scrollarea_2.setGeometry(411, 310, 200, 460)
       # self.scrollarea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.verticalScrollBar_2 = QtWidgets.QScrollBar(QtCore.Qt.Vertical, self.scrollarea_2)
        self.scrollarea_2.setVerticalScrollBar(self.verticalScrollBar_2)
        self.verticalScrollBar_2.setStyleSheet("""QScrollBar::vertical{border-color: transparent;border-width: 1px;border-style: outset;background-color: transparent;width: 10px;margin: 10px 0 10px 0;}""" """QScrollBar::handle:vertical {background-color:#cdcdcd ; border-style:outset; border-radius:3px}""" """QScrollBar::add-line:vertical {background-color: #cdcdcd;border: transparent; height: 10px;subcontrol-position: bottom;subcontrol-origin: margin; border-radius:3px}""" """QScrollBar::sub-line:vertical {background-color: #cdcdcd; border: transparent;height: 10px;subcontrol-position: top;subcontrol-origin: margin;border-radius:3px}""")
        self.scrollarea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollarea_2.setWidgetResizable(True)
        self.scrollarea_2.setWidget(self.widget_2)
        self.scrollarea_2.setStyleSheet("border-width:1px; border-style: solid; border-color: white #EBEBEB #EBEBEB white;")

        self.verticalScrollBar = QtWidgets.QScrollBar(QtCore.Qt.Vertical, self.scrollarea)
        self.scrollarea.setVerticalScrollBar(self.verticalScrollBar)
        #self.scrollarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.widget)
        self.verticalScrollBar.setStyleSheet("""QScrollBar::vertical{border-color: transparent;border-width: 1px;border-style: outset;background-color: transparent;width: 10px;margin: 10px 0 10px 0;}""" """QScrollBar::handle:vertical {background-color:#cdcdcd ; border-style:outset; border-radius:3px}""" """QScrollBar::add-line:vertical {background-color: #cdcdcd;border: transparent; height: 10px;subcontrol-position: bottom;subcontrol-origin: margin; border-radius:3px}""" """QScrollBar::sub-line:vertical {background-color: #cdcdcd; border: transparent;height: 10px;subcontrol-position: top;subcontrol-origin: margin;border-radius:3px}""")


        self.nameflag = {}
        self.nameobj = {}

        self.isShrimp = True

        self.PushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.PushButton_3.setGeometry(411, 270, 200, 40)
        self.PushButton_3.setFont(QtGui.QFont("FZHTJW", 10))
        self.PushButton_3.setStyleSheet("""QPushButton{padding-left: 13px; text-align: left; background-color:transparent; border-style:outset; border-width: 1px; border-style: solid; border-color: #EBEBEB #EBEBEB white white; }""" """QPushButton:hover{background-color:#F5F5F5}""" """QPushButton:pressed{background-color:#E6E6E6}""")
        self.PushButton_3.clicked.connect(self.ExpandOrShrimpScrollarea_2)
 
        self.plainTextEdit = QtWidgets.QLineEdit(self.centralwidget)
        #self.plainTextEdit.setGeometry(QtCore.QRect(0, 691, 410, 80))
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 661, 411, 109))
        self.plainTextEdit.setObjectName("plainTextEdit" )
        self.plainTextEdit.setStyleSheet("padding-top:0px; padding-bottom:20px; border-width: 1px; border-style: solid; border-color: white #EBEBEB #EBEBEB #EBEBEB; ")
        self.plainTextEdit.setFont(QtGui.QFont("FZHTJW", 10))

        self.plainTextEdit.returnPressed.connect(self.changetextbrowsertext)
        

        self.PushButton = QtWidgets.QPushButton(self.centralwidget)
        self.PushButton.setGeometry(QtCore.QRect(310, 732, 90, 28))
        self.PushButton.setObjectName("PushButton")
        self.PushButton.clicked.connect(self.changetextbrowsertext)
        self.PushButton.setStyleSheet("""QPushButton{ background-color:#12B7F5; border-style:outset; border-radius:3px; color:white;}""" """QPushButton:hover{background-color:#47C8F8}""" """QPushButton:pressed{background-color:#0FA3E4}""")
        self.PushButton.setFont(QtGui.QFont("FZHTJW",9))

        self.PushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.PushButton_2.setGeometry(QtCore.QRect(225, 732, 70, 28))
        self.PushButton_2.setObjectName("PushButton_2")
        self.PushButton_2.clicked.connect(self.closewindow)
        self.PushButton_2.setStyleSheet("""QPushButton{background-color:transparent; border-style:outset; border-width:1px;border-radius:3px; border-color:grey}""" """QPushButton:hover{background-color:#C1C1C1}""" """QPushButton:pressed{background-color:#AAAAAA}""")
        self.PushButton_2.setFont(QtGui.QFont("FZHTJW",9))

        self.liaotian = QtWidgets.QPushButton(self.centralwidget)
        self.liaotian.setGeometry(QtCore.QRect(0, 48, 52, 40))
        self.liaotian.setObjectName("liaotian")
        self.liaotian.setStyleSheet("QPushButton""{""background-color:transparent; color:grey; padding-top:10px""}" "QPushButton:hover""{""color:black;""}")
        self.liaotian.setText("聊天")
        
        self.liaotian.setFont(QtGui.QFont("FZHTJW", 13))

       
        self.shuaxin = QtWidgets.QPushButton(self.centralwidget)
        self.shuaxin.setGeometry(QtCore.QRect(52, 48, 52, 40))
        self.shuaxin.setObjectName("shuaxin")
        self.shuaxin.setStyleSheet("QPushButton""{""background-color:transparent; color:grey; padding-top:10px ""}" "QPushButton:hover""{""color:black;""}")
        self.shuaxin.setText("刷新")
        self.shuaxin.setFont(QtGui.QFont("FZHTJW", 13))
        #self.shuaxin.clicked.connect(self.refreshprevmsg)

        self.changebackground = QtWidgets.QPushButton(self.centralwidget)
        self.changebackground.setGeometry(QtCore.QRect(422, 48, 94, 40))
        self.changebackground.setObjectName("gexin")
        self.changebackground.setStyleSheet("QPushButton""{""background-color:transparent; color:grey;padding-top:10px""}" "QPushButton:hover""{""color:black;""}")
        self.changebackground.setText("个性装扮")
        self.changebackground.setFont(QtGui.QFont("FZHTJW", 13))
        self.changebackground.clicked.connect(self.optionforchangingbackground)
        self.backgroundoption = QtWidgets.QMainWindow()
        self.backgroundImage = QtWidgets.QMainWindow()


        self.changeavatar = QtWidgets.QPushButton(self.centralwidget)
        self.changeavatar.setGeometry(QtCore.QRect(516, 48, 94, 40))
        self.changeavatar.setObjectName("shezhi")
        self.changeavatar.setStyleSheet("QPushButton""{""background-color:transparent; color:grey;padding-top:10px""}" "QPushButton:hover""{""color:black;""}")
        self.changeavatar.setText("设置头像")
        self.changeavatar.setFont(QtGui.QFont("FZHTJW", 13))
        self.changeavatar.clicked.connect(self.settingwindow)
        
        self.newwindow = QtWidgets.QMainWindow()
        self.newwindow.setWindowTitle("设置头像")
        self.newwindow.resize(500,500)
        self.newwindowwidget = QtWidgets.QWidget(self.newwindow)
        self.newwindow.setCentralWidget(self.newwindowwidget)

        self.newwindowlayout = QtWidgets.QVBoxLayout()
        self.newwindowphotoframe = QtWidgets.QLabel()
        self.newwindowphotoframe.resize(500,400)
        self.newwindowphotoframe.setAlignment(QtCore.Qt.AlignCenter)
        self.newwindowbutton = QtWidgets.QPushButton("电脑中选择照片")
        self.newwindowbutton_2 = QtWidgets.QPushButton("确认")
        self.newwindowbutton_2.clicked.connect(self.confirmPicture)
        self.newwindowbutton.clicked.connect(self.getPictureFromFileSystem)
        self.newwindowlayout.addWidget(self.newwindowphotoframe)
        self.newwindowlayout.addWidget(self.newwindowbutton)
        self.newwindowlayout.addWidget(self.newwindowbutton_2)
        self.newwindowwidget.setLayout(self.newwindowlayout)
        self.fname = tuple()
        self.fname_2 = tuple()
        

        self.widget_1_flag = False
        self.widget_1_path = "widget_1.png"
        self.widget_1 = QtWidgets.QPushButton(self.centralwidget)
        self.widget_1.setGeometry(1,666,30,30)
        self.widget_1.setIcon(QtGui.QIcon(self.widget_1_path))
        self.widget_1.setIconSize(QtCore.QSize(29,29))
        self.widget_1.setStyleSheet("""QPushButton{border-style:outset;border-radius:3px;}""" """QPushButton:hover{background-color:#F1F1F1}""" """QPushButton:pressed{background-color:#E6E6E6}""")
        self.widget_1.clicked.connect(self.widget_1_f)
        
        self.widget_2_path = "widget_2.png"
        self.widget_2 = QtWidgets.QPushButton(self.centralwidget)
        self.widget_2.setGeometry(31,666,30,30)
        self.widget_2.setIcon(QtGui.QIcon(self.widget_2_path))
        self.widget_2.setIconSize(QtCore.QSize(29,29))
        self.widget_2.setStyleSheet("""QPushButton{border-style:outset;border-radius:3px;}""" """QPushButton:hover{background-color:#F1F1F1}""" """QPushButton:pressed{background-color:#E6E6E6}""")


        self.widget_3_path = "widget_3.png"
        self.widget_3 = QtWidgets.QPushButton(self.centralwidget)
        self.widget_3.setGeometry(61,666,30,30)
        self.widget_3.setIcon(QtGui.QIcon(self.widget_3_path))
        self.widget_3.setIconSize(QtCore.QSize(29,29))
        self.widget_3.setStyleSheet("""QPushButton{border-style:outset;border-radius:3px;}""" """QPushButton:hover{background-color:#F1F1F1}""" """QPushButton:pressed{background-color:#E6E6E6}""")
        #self.widget_3.clicked.connect(self.snap)

        self.widget_4_path = "widget_4.png"
        self.widget_4 = QtWidgets.QPushButton(self.centralwidget)
        self.widget_4.setGeometry(91,666,30,30)
        self.widget_4.setIcon(QtGui.QIcon(self.widget_4_path))
        self.widget_4.setIconSize(QtCore.QSize(29,29))
        self.widget_4.setStyleSheet("""QPushButton{border-style:outset;border-radius:3px;}""" """QPushButton:hover{background-color:#F1F1F1}""" """QPushButton:pressed{background-color:#E6E6E6}""")

        self.widget_5_path = "widget_5.png"
        self.widget_5 = QtWidgets.QPushButton(self.centralwidget)
        self.widget_5.setGeometry(121,666,30,30)
        self.widget_5.setIcon(QtGui.QIcon(self.widget_5_path))
        self.widget_5.setIconSize(QtCore.QSize(29,29))
        self.widget_5.setStyleSheet("""QPushButton{border-style:outset;border-radius:3px;}""" """QPushButton:hover{background-color:#F1F1F1}""" """QPushButton:pressed{background-color:#E6E6E6}""")

        self.widget_6_path = "widget_6.png"
        self.widget_6 = QtWidgets.QPushButton(self.centralwidget)
        self.widget_6.setGeometry(151,666,30,30)
        self.widget_6.setIcon(QtGui.QIcon(self.widget_6_path))
        self.widget_6.setIconSize(QtCore.QSize(29,29))
        self.widget_6.setStyleSheet("""QPushButton{border-style:outset;border-radius:3px;}""" """QPushButton:hover{background-color:#F1F1F1}""" """QPushButton:pressed{background-color:#E6E6E6}""")
        self.widget_6.clicked.connect(lambda: self.getPictureFromFileSystem_2(False, ""))

        self.widget_7_path = "widget_7.png"
        self.widget_7 = QtWidgets.QPushButton(self.centralwidget)
        self.widget_7.setGeometry(181,666,30,30)
        self.widget_7.setIcon(QtGui.QIcon(self.widget_7_path))
        self.widget_7.setIconSize(QtCore.QSize(29,29))
        self.widget_7.setStyleSheet("""QPushButton{border-style:outset;border-radius:3px;}""" """QPushButton:hover{background-color:#F1F1F1}""" """QPushButton:pressed{background-color:#E6E6E6}""")

        self.widget_8_path = "widget_8.png"
        self.widget_8 = QtWidgets.QPushButton(self.centralwidget)
        self.widget_8.setGeometry(211,666,30,30)
        self.widget_8.setIcon(QtGui.QIcon(self.widget_8_path))
        self.widget_8.setIconSize(QtCore.QSize(29,29))
        self.widget_8.setStyleSheet("""QPushButton{border-style:outset;border-radius:3px;}""" """QPushButton:hover{background-color:#F1F1F1}""" """QPushButton:pressed{background-color:#E6E6E6}""")

        self.widget_8.installEventFilter(self)
        self.widget_8_dialog = QtWidgets.QMainWindow()
        self.widget_8_dialog.setWindowOpacity(0.8)
        self.widget_8_dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.widget_8_dialog.installEventFilter(self)
        self.widget_8_dialog.setWindowFlag(QtCore.Qt.Tool)
        self.w8_widget = QtWidgets.QWidget()
        self.widget_8_dialog.setCentralWidget(self.w8_widget)
        self.textedit = QtWidgets.QPushButton("字体选择", self.w8_widget)
        self.textedit.setFont(QtGui.QFont('FZHTJW', 8))
        self.textedit.setFixedSize(110,30)
        self.textedit.clicked.connect(self.poptextedit)
        self.poptextediton = False

        self.fonttype = QtWidgets.QComboBox(self.centralwidget)
        self.fonttype.move(130, 635)
        self.fonttype.addItem("默认字体")
        self.fonttype.addItem("汉仪新蒂蜡笔体")
        self.fonttype.addItem("Oz焦糖下午茶")
        self.fonttype.setFrame(False)
        self.fonttype.setStyleSheet("""QComboBox::drop-down{border-width : 0px; }""" """QComboBox{padding-left:5px; border:1px #ADADAD; border-style:solid; border-radius:3px}""" """QComboBox::hover{border-color: #1583DD}""")
        self.fonttype.setFont(QtGui.QFont("FZHTJW",9))
        self.fonttype.activated[str].connect(self.modifyfont)
        self.fonttype.hide()
        

        self.fontsizehint = QtWidgets.QLabel(self.centralwidget)
        self.fontsizehint.move(245, 638)
        self.fontsizehint.setText("字体大小")
        self.fontsizehint.setStyleSheet("color:#A7A7A7")
        self.fontsizehint.setFont(QtGui.QFont("FZHTJW",9))
        self.fontsizehint.hide()


        self.fontsize = QtWidgets.QComboBox(self.centralwidget)
        self.fontsize.move(300, 635)
        self.fontsize.activated[str].connect(self.modifyfontsize)
        self.fontsize.setFixedWidth(40)
        self.fontsize.setStyleSheet("""QComboBox::drop-down{border-width : 0px; }""" """QComboBox{ border:1px #ADADAD; border-style:solid; border-radius:3px}""" """QComboBox::hover{border-color: #1583DD}""")
        self.fontsize.setFont(QtGui.QFont("FZHTJW",9))
        for i in range(9, 15):
            self.fontsize.addItem(f'{i}')
        self.fontsize.hide()

        self.fontbubble = QtWidgets.QPushButton(self.centralwidget)
        self.fontbubble.move(348,630)
        self.fontbubble.setStyleSheet("""QPushButton{ background-color:#F4F4F4; border-style:outset; border-radius:3px; color:black; border-width:1px; border-color:#ADADAD;}""" """QPushButton:hover{background-color:#BEE7FD}""" """QPushButton:pressed{background-color:#EBECED}""")
        self.fontbubble.setText("选择气泡")
        self.fontbubble.setFont(QtGui.QFont("FZHTJW",9))
        self.fontbubble.setFixedWidth(60)
        self.fontbubble.setFixedHeight(25)
        self.fontbubble.clicked.connect(self.fontbubblechange)
        self.fontbubble.hide()

        self.widget_9_path = "widget_9.png"
        self.widget_9 = QtWidgets.QPushButton(self.centralwidget)
        self.widget_9.setGeometry(335,666,30,30)
        self.widget_9.setIcon(QtGui.QIcon(self.widget_9_path))
        self.widget_9.setIconSize(QtCore.QSize(29,29))
        self.widget_9.setStyleSheet("""QPushButton{border-style:outset;border-radius:3px;}""" """QPushButton:hover{background-color:#F1F1F1}""" """QPushButton:pressed{background-color:#E6E6E6}""")

        self.widget_10_path = "widget_10.png"
        self.widget_10 = QtWidgets.QPushButton(self.centralwidget)
        self.widget_10.setGeometry(375,666,30,30)
        self.widget_10.setIcon(QtGui.QIcon(self.widget_10_path))
        self.widget_10.setIconSize(QtCore.QSize(29,29))
        self.widget_10.setStyleSheet("""QPushButton{border-style:outset;border-radius:3px;}""" """QPushButton:hover{background-color:#F1F1F1}""" """QPushButton:pressed{background-color:#E6E6E6}""")


        self.setCentralWidget(self.centralwidget)
        self.changebackground_flag = False
        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(self)

        self.freeze = False
        self.oldPos = self.pos()
        self.buttondialog = QtWidgets.QMainWindow()
        self.w8_dialog_timer = QtCore.QTimer()
        self.w8_show_flag = False
        self.shoulddrag = False
        self.show()

# Font, fontsize, background-color, font-color, border-color

    def fontbubblechange(self):
        self.bubblechangewindow = QtWidgets.QMainWindow()
        self.bubblechangewindow.resize(400,400)
        self.bubblechangecentralwidget = QtWidgets.QWidget(self.bubblechangewindow)
        self.bubblechangewindow.setCentralWidget(self.bubblechangecentralwidget)
        self.bubblechangewidget = QtWidgets.QWidget()
        self.scrollarea_bubble = QtWidgets.QScrollArea(self.bubblechangecentralwidget)
        self.vbox_bubble = QtWidgets.QVBoxLayout()
        self.vbox_bubble.addStretch()
        self.bubblechangewidget.setLayout(self.vbox_bubble)
        self.scrollarea_bubble.resize(400,400)
        self.scrollarea_bubble.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollarea_bubble.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollarea_bubble.setWidgetResizable(True)
        self.scrollarea_bubble.setWidget(self.bubblechangewidget)
        self.bubbleButton1 = QtWidgets.QPushButton("默认边框")
        self.bubbleButton1.clicked.connect(self.originalframe)
        self.vbox_bubble.insertWidget(self.vbox_bubble.count()-1, self.bubbleButton1)
        self.bubbleButton2 = QtWidgets.QPushButton("蓝色边框")
        self.bubbleButton2.clicked.connect(self.blueframe)
        self.vbox_bubble.insertWidget(self.vbox_bubble.count()-1, self.bubbleButton2)
        self.bubbleButton3 = QtWidgets.QPushButton("灰色背景")
        self.bubbleButton3.clicked.connect(self.greybackground)
        self.vbox_bubble.insertWidget(self.vbox_bubble.count()-1, self.bubbleButton3)
        self.bubbleButton4 = QtWidgets.QPushButton("黑色边框")
        self.bubbleButton4.clicked.connect(self.blackframe)
        self.vbox_bubble.insertWidget(self.vbox_bubble.count()-1, self.bubbleButton4)
        self.bubblechangewindow.show()

    def originalframe(self):
        namefontdict[username] = defaultFont
        datatosend = namefontdict[username]
        datatosend = pickle.dumps(datatosend)
        signalbyte = 'Q'
        fulldata = bytes(signalbyte + f'{len(username):<{HeaderSize}}' + username + f'{len(datatosend):<{HeaderSize}}','utf-8') + datatosend
        try:
            s.send(fulldata)
        except:
            s.close()
            print("server close in Connection")
        
    def blueframe(self):
        namefontdict[username][4] = "#96EBFF"
        namefontdict[username][3] = "#22ADFE"
        namefontdict[username][2] = "#D4F8FF"
        datatosend = namefontdict[username]
        datatosend = pickle.dumps(datatosend)
        signalbyte = 'Q'
        fulldata = bytes(signalbyte + f'{len(username):<{HeaderSize}}' + username + f'{len(datatosend):<{HeaderSize}}','utf-8') + datatosend
        try:
            s.send(fulldata)
        except:
            s.close()
            print("server close in Connection")

    def greybackground(self):
        namefontdict[username][4] = "#E5E5E5"
        namefontdict[username][3] = "black"
        namefontdict[username][2] = "#E5E5E5"
        datatosend = namefontdict[username]
        datatosend = pickle.dumps(datatosend)
        signalbyte = 'Q'
        fulldata = bytes(signalbyte + f'{len(username):<{HeaderSize}}' + username + f'{len(datatosend):<{HeaderSize}}','utf-8') + datatosend
        try:
            s.send(fulldata)
        except:
            s.close()
            print("server close in Connection")

    def blackframe(self):
        namefontdict[username][4] = "#7C7C7C"
        namefontdict[username][3] = "black"
        namefontdict[username][2] = "white"
        datatosend = namefontdict[username]
        datatosend = pickle.dumps(datatosend)
        signalbyte = 'Q'
        fulldata = bytes(signalbyte + f'{len(username):<{HeaderSize}}' + username + f'{len(datatosend):<{HeaderSize}}','utf-8') + datatosend
        try:
            s.send(fulldata)
        except:
            s.close()
            print("server close in Connection")

    def modifyfontsize(self, text):
        namefontdict[username][1] = int(text)
        datatosend = namefontdict[username]
        datatosend = pickle.dumps(datatosend)
        signalbyte = 'Q'
        fulldata = bytes(signalbyte + f'{len(username):<{HeaderSize}}' + username + f'{len(datatosend):<{HeaderSize}}','utf-8') + datatosend
        try:
            s.send(fulldata)
        except:
            s.close()
            print("server close in Connection")

    def modifyfont(self, text):
        if text == "默认字体":
            namefontdict[username][0] = "FZHTJW"
        elif text == "汉仪新蒂蜡笔体":
            namefontdict[username][0] = "HanyiSentyCrayon"
        elif text == "Oz焦糖下午茶":
            namefontdict[username][0] = "OzCaramel"
        datatosend = namefontdict[username]
        datatosend = pickle.dumps(datatosend)
        signalbyte = 'Q'
        fulldata = bytes(signalbyte + f'{len(username):<{HeaderSize}}' + username + f'{len(datatosend):<{HeaderSize}}','utf-8') + datatosend
        try:
            s.send(fulldata)
        except:
            s.close()
            print("server close in Connection")


   # @QtCore.pyqtSlot(QtWidgets.QAction)
    def on_menu_triggered(self, action):
        if action.text() == '字体选择':
            print("打开字体选择窗口")

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.Enter:
            self.widget_8_dialog.setGeometry(self.pos().x()+170, self.pos().y()+630, 110, 30)
            self.w8_show_flag = True
            self.widget_8_dialog.show()
            
           
        elif event.type() == QtCore.QEvent.Leave:
            self.w8_dialog_timer.singleShot(500, self.hidewidget_8_dialog)
            self.w8_show_flag = False
        return False
          

    def hidewidget_8_dialog(self):
        if self.w8_show_flag == False:
            self.widget_8_dialog.hide()

    def poptextedit(self):
        if self.poptextediton == False:
            self.scrollarea.resize(411,537)
            self.plainTextEdit.move(0, 627)
            self.plainTextEdit.resize(411, 143)
            self.plainTextEdit.setStyleSheet("padding-top:33px; padding-bottom:20px; border-width: 1px; border-style: solid; border-color: white #EBEBEB #EBEBEB #EBEBEB; ")
            self.fontsize.show()
            self.fonttype.show()
            self.fontsizehint.show()
            self.fontbubble.show()
        else:
            self.scrollarea.resize(411,571)
            self.plainTextEdit.move(0, 661)
            self.plainTextEdit.resize(411, 109)
            self.plainTextEdit.setStyleSheet("padding-top:0px; padding-bottom:20px; border-width: 1px; border-style: solid; border-color: white #EBEBEB #EBEBEB #EBEBEB; ")
            self.fontsize.hide()
            self.fonttype.hide()
            self.fontsizehint.hide()
            self.fontbubble.hide()
        self.poptextediton = not self.poptextediton



    def snap(self):
        global snapflag
        snapflag = True
        QtCore.QCoreApplication.instance().quit()
       
       
 
    def mousePressEvent(self, event):
       
        self.oldPos = event.globalPos()
        if self.oldPos.y() < self.pos().y() + self.backcolor.height():
            self.shoulddrag = True
        else:
            self.shoulddrag = False
 
    def mouseMoveEvent(self, event):
        if self.shoulddrag:
            
            delta = QtCore.QPoint (event.globalPos() - self.oldPos)
            if self.freeze == False:
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.buttondialog.move(self.buttondialog.x() + delta.x(), self.buttondialog.y() + delta.y())
                self.backgroundoption.move(self.backgroundoption.x() + delta.x(), self.backgroundoption.y() + delta.y())
            else:
                self.move(self.x(), self.y())
                self.buttondialog.move(self.buttondialog.x(), self.buttondialog.y())
            self.oldPos = event.globalPos()
            if self.changebackground_flag:
                if self.x() < self.backgroundImage.x():
                    self.freeze = True
                    self.move(self.backgroundImage.x(), self.y())
                    self.buttondialog.move(self.backgroundImage.x()-self.buttondialog.width(), self.y())
                else:
                    self.freeze = False
                if self.x() > self.backgroundImage.x()+self.backgroundImage.width()-self.width():
                    self.freeze = True
                    self.move(self.backgroundImage.x()+self.backgroundImage.width()-self.width(), self.y())
                    self.buttondialog.move(self.backgroundImage.x()+self.backgroundImage.width()-self.width()-self.buttondialog.width(), self.y())
                else:
                    self.freeze = False
                if self.y() < self.backgroundImage.y():
                    self.freeze = True
                    self.move(self.x(), self.backgroundImage.y())
                    self.buttondialog.move(self.buttondialog.x(), self.backgroundImage.y())
                else:
                    self.freeze = False
                if self.y() > self.backgroundImage.y()+self.backgroundImage.height()-self.backcolor.height():
                    self.freeze = True
                    self.move(self.x(), self.backgroundImage.y()+self.backgroundImage.height()-self.backcolor.height())
                    self.buttondialog.move(self.buttondialog.x(), self.backgroundImage.y()+self.backgroundImage.height()-self.backcolor.height())
                else:
                    self.freeze = False


    def mouseReleaseEvent(self, event):
        self.shoulddrag = False
        

    def refreshprevmsg(self):
        global appmsg
        global ngif
        usermessages.clear()
        usermessagesnames.clear()
        clientMessageMapper.clear()
        clientMessageMapperIndex.clear()
        arraybufflist.clear()
        bufferList.clear()
        ngif = 0
        self.clearLayout(self.vbox)
        self.vbox.addStretch()
        signalbyte = 'M'
        try:
            s.send(bytes(signalbyte,"utf-8"))
            print("sent M signal to server")
        except:
            s.close()
            print("server close in Connection")


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PushButton.setText(_translate("MainWindow", "发送(S)"))
        self.PushButton_2.setText(_translate("MainWindow", "关闭(C)"))
        self.closebutton.setText(_translate("closebutton", u'\u2715'))
        self.minbutton.setText(_translate("minbutton", u'\u2015'))

    

    def confirmPicture(self):
        if len(self.fname) == 0:
            return
        global updateonlineusers
        global usernameavatar
        if len(self.fname) != 0:
            self.imagePath = ''.join(self.fname[0])
            imgdata = open(self.imagePath, 'rb').read()
            imgtype = self.imagePath[len(self.imagePath)-3:]
            usernameavatar[username] = imgdata + bytes(imgtype, "utf-8")
            updateonlineusers = True
            avatartosend = imgdata
            clientMessage = bytes('A' + f'{len(username):<{HeaderSize}}' + username + f'{len(avatartosend):<{HeaderSize}}', "utf-8") + avatartosend + bytes(imgtype,"utf-8")
            try:
                s.send(clientMessage)
            except:
                s.close()
                print("server close in Connection")
                return
            temp = list(self.fname)
            temp.clear()
            self.newwindow.hide()
    def appendPicture(self, img_data, img_type, name, myself):
        self.createwidget_2(img_data, img_type, name, myself)
        self.scrollarea.verticalScrollBar().rangeChanged.connect(self.change_scroll)

    def optionforchangingbackground(self):
        
        self.backgroundoption.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        optbgwid = QtWidgets.QWidget()
        self.backgroundoption.setCentralWidget(optbgwid)
        qvb = QtWidgets.QVBoxLayout()
        b1 = QtWidgets.QPushButton(optbgwid)
        b1.setText("自定义背景")
        b1.setFont(QtGui.QFont("FZHTJW", 11))
        b1.clicked.connect(self.settingbackground)
        b1.setStyleSheet("color:white")
        b2 = QtWidgets.QPushButton(optbgwid)
        b2.setText("恢复默认皮肤")
        b2.setFont(QtGui.QFont("FZHTJW", 11))
        b2.setStyleSheet("color:white")
        b2.clicked.connect(self.restore)
        b3 = QtWidgets.QPushButton(optbgwid)
        b3.setText("取消")
        b3.setFont(QtGui.QFont("FZHTJW", 11))
        b3.setStyleSheet("color:white")
        b3.clicked.connect(self.cancel)
        qvb.addWidget(b1)
        qvb.addWidget(b2)
        qvb.addWidget(b3)
        optbgwid.setLayout(qvb)
        self.backgroundoption.show()
        self.backgroundoption.move(self.pos().x()-self.backgroundoption.width(), self.pos().y())
        self.backgroundoption.setStyleSheet("background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #4C8EFF , stop:1 #1FD2FF); ")


    def restore(self):
        self.backcolor.clear()
        self.backcolor.setStyleSheet("background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #4C8EFF , stop:1 #1FD2FF)")
        self.backgroundoption.close()

    def cancel(self):
        self.backgroundoption.close()
        

    def settingbackground(self):
        self.backgroundoption.close()
        self.backgroundpic = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QWidget(), 'Open file', 'c:\\' ,"Image files (*.jpg)")
        if self.backgroundpic[0] != "":
            self.backgroundLabel = QtWidgets.QLabel()
            self.backgroundLabel.setPixmap(QtGui.QPixmap(''.join(self.backgroundpic[0])))
            self.backgroundImage.setCentralWidget(self.backgroundLabel)
            self.backgroundImage.resize(self.backgroundLabel.width(), self.backgroundLabel.height())
            self.setWindowOpacity(0.7)
            self.backgroundImage.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.FramelessWindowHint)
            centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
            self.backgroundImage.move(centerPoint.x()-self.backgroundLabel.width(), centerPoint.y()-self.backgroundLabel.height())
            self.backcolor.setStyleSheet("background-color:white")
            self.buttondialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.buttondialog.setWindowOpacity(0.9)
            self.qvbox = QtWidgets.QVBoxLayout()
            self.buttonwidget = QtWidgets.QWidget()
            self.buttondialog.setCentralWidget(self.buttonwidget)
            self.backgroundconfirm = QtWidgets.QPushButton(self.buttonwidget)
            self.backgroundconfirm.setText("确定")
            self.backgroundconfirm.clicked.connect(self.bgcf)
            self.backgroundcancel = QtWidgets.QPushButton(self.buttonwidget)
            self.backgroundcancel.setText("取消")
            self.backgroundcancel.clicked.connect(self.bgcl)
            self.qvbox.addWidget(self.backgroundconfirm)
            self.qvbox.addWidget(self.backgroundcancel)
            self.buttonwidget.setLayout(self.qvbox)
            self.backgroundImage.show()
            self.buttondialog.show()
            self.changebackground_flag = True
            self.move(self.backgroundImage.pos())
            self.buttondialog.move(self.pos().x()-self.buttondialog.width(), self.pos().y())

    def bgcf(self):
        imgpath_temp = ''.join(self.backgroundpic[0])
        self.backcolorpixmap = self.mask_background_image(open(imgpath_temp, 'rb').read())
        self.backcolor.setPixmap(self.backcolorpixmap)
        self.setWindowOpacity(1.0)
        self.backgroundImage.close()
        self.buttondialog.hide()
        self.changebackground_flag = False
    def bgcl(self):
        self.backgroundImage.close()
        self.buttondialog.hideEvent()
        self.changebackground_flag = False
        self.setWindowOpacity(1.0)

    def createwidget_2(self, img_data, img_type, name, myself):
        global ngif
        if len(img_data) == 0:
            return
        self.leftbar = QtWidgets.QLabel()
        self.rightbar = QtWidgets.QLabel()
        self.leftbar.setStyleSheet("border-width:0px")
        self.rightbar.setStyleSheet("border-width:0px")
        #name
        self.hbox = QtWidgets.QHBoxLayout()
        self.name = QtWidgets.QLabel()
        self.name.setFont(QtGui.QFont("Times New Roman", 12))
        self.name.setStyleSheet("background-color:transparent; color:grey; border-width:0px")
        self.name.setText(name)
        self.name.setFixedSize(self.name.width(),self.name.height())

        if name not in usernameavatar.keys():
            imagePath = "qq_logo.png"
            imgdata = open(imagePath, 'rb').read()
            imgtype = imagePath[len(imagePath)-3:]
        else:
            imgdataplustype = usernameavatar[name]
            imgdata = imgdataplustype[:len(imgdataplustype)-3]
            imgtype = imgdataplustype[len(imgdataplustype)-3:]
        pixmap = self.mask_image(imgdata, 40, imgtype)

        #self.image = QtGui.QImage(self.imagePath)
        self.labelreal = QtWidgets.QLabel()
        self.labelreal.setPixmap(pixmap)
        self.labelreal.setScaledContents(True)
        self.labelreal.setStyleSheet("background-color: transparent; border-width:0px")
        self.labelreal.setFixedSize(40,40)
        if myself == 0:
            self.rightbar.setMinimumWidth(411 - self.labelreal.width()-self.name.width() -50)
            self.hbox.addWidget(self.labelreal)
            self.hbox.addWidget(self.name)
            self.hbox.addWidget(self.rightbar)
            self.vbox.insertLayout(self.vbox.count()-1, self.hbox)

        lbl = QtWidgets.QLabel()
        #self.lbl.setStyleSheet("border-radius:5px")
        if img_type == "gif":
            bArray = QtCore.QByteArray(img_data)
            arraybufflist.append(bArray)
            bBuffer = QtCore.QBuffer(arraybufflist[ngif])
            bBuffer.open(QtCore.QIODevice.ReadOnly)
            bufferList.append(bBuffer)
            movie = QtGui.QMovie()
            #self.movie.setFormat("GIF")
            movie.setDevice(bufferList[ngif])
            ngif += 1
            lbl.setFixedSize(100,100)
            lbl.setStyleSheet("border-width:0px;")
            #self.lbl.setScaledSize(QtCore.QSize(100,100))
            lbl.setMovie(movie)
            movie.start()

        else:    
            image = QtGui.QImage.fromData(img_data, img_type)
            size = image.width()
            if size > 280:
                size = 280
            pm = QtGui.QPixmap.fromImage(image) 
            oppm = pm.scaled(size, size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            
            lbl.setPixmap(oppm)
            lbl.setFixedSize(oppm.width(), oppm.height())
        #self.lbl.setStyleSheet("background-color:black")

        self.hboxnew = QtWidgets.QHBoxLayout()
        if myself == 0:
            self.name.setFixedHeight(30)
            self.name.setFixedWidth(200)
            self.leftbar.setMinimumWidth(411 - 40 - 280- 70)
            self.newlabel = QtWidgets.QLabel()
            self.newlabel.setStyleSheet("border-width:0px")
            self.newlabel.setFixedWidth(40)
            self.hboxnew.addWidget(self.newlabel)
            self.hboxnew.addWidget(lbl)
            self.hboxnew.addWidget(self.leftbar)
        else:
            self.leftbar.setMinimumWidth(411 - 40 - 280 - 70)

            if lbl.height()-40 < 0:
                self.rightbar.setMaximumHeight(0)
            else:
                self.rightbar.setMinimumHeight(lbl.height()-40)

            self.rightbar.setFixedWidth(40)
            self.rightbar.setAlignment(QtCore.Qt.AlignTop)
            self.rightlayout = QtWidgets.QVBoxLayout()
            self.rightlayout.addWidget(self.labelreal)
            self.rightlayout.addWidget(self.rightbar)
            self.middlelayout = QtWidgets.QVBoxLayout()
            self.middlelabel = QtWidgets.QLabel()
            self.middlelabel.setStyleSheet("border-width:0px")
            self.middlelabel.setMaximumHeight(5)

            self.middlelayout.addWidget(self.middlelabel)
            self.middlelayout.addWidget(lbl)
            self.hboxnew.addWidget(self.leftbar)
            self.hboxnew.addLayout(self.middlelayout)
            self.hboxnew.addLayout(self.rightlayout)

        self.vbox.insertLayout(self.vbox.count()-1, self.hboxnew)

    def getPictureFromFileSystem(self):
        self.fname = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QWidget(), 'Open file', 'c:\\' ,"Image files (*.jpg *.png)")
        if self.fname[0] != "":
            self.newwindowphotoframe.setPixmap(QtGui.QPixmap(''.join(self.fname[0])).scaled(500, 400, QtCore.Qt.KeepAspectRatio))

    def getPictureFromFileSystem_2(self, flag, imgpath):
        if flag == False:
            self.fname_2 = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QWidget(), 'Open file', 'c:\\' ,"Image files (*.jpg *.png *.gif)")
            if self.fname_2[0] == "":
                return
            try:
                self.imagePath_2 = ''.join(self.fname_2[0])
                imgdata = open(self.imagePath_2, 'rb').read()
                imgtype = self.imagePath_2[len(self.imagePath_2)-3:]
                self.appendPicture(imgdata, imgtype, username, 1)
                imgtosend = imgdata
            except:
                return

        else:
            try:
                self.imagePath_2 = imgpath
                print(self.imagePath_2)
                imgdata = open(self.imagePath_2, 'rb').read()
                imgtype = self.imagePath_2[len(self.imagePath_2)-3:]
                print("len of imgtype is " +f'{len(imgtype)}')
                self.appendPicture(imgdata, imgtype, username, 1)
                imgtosend = imgdata
                print("imagelen + imagedata to send is " + f'{len(imgtosend) + len(imgtype)}')
            except:
                print("An Error has occured while retrieving image")
                return
        clientmsg = bytes('I' + f'{len(username):<{HeaderSize}}' + username + f'{len(imgtosend):<{HeaderSize}}', "utf-8") + imgtosend + bytes(imgtype, "utf-8")
        try:
            s.send(clientmsg)
            print("sent image files")
        except:
            s.close()
            print("server close in Connection")
            return

        temp = list(self.fname_2)
        temp.clear()
        #self.refreshprevmsg()
    
    
    def settingwindow(self):
        self.newwindow.show()


    def widget_1_f(self):
        if self.widget_1_flag:
            self.widget_1_flag = not self.widget_1_flag
            self.widget_1.setStyleSheet("""QPushButton{border-style:outset;border-radius:3px;}""" """QPushButton:hover{background-color:#C1C1C1}""" """QPushButton:pressed{background-color:#AAAAAA}""")
        else:
            self.widget_1_flag = not self.widget_1_flag
            self.widget_1.setStyleSheet("border-style:outset;border-radius:3px;background-color:#AAAAAA")
    def ExpandOrShrimpScrollarea_2(self):
        if self.isShrimp:
            #self.scrollarea_2.setGeometry(410, 310, 200, 460)
            self.scrollarea_2.move(411,130)
            self.PushButton_3.move(411,90)
            self.scrollarea_2.resize(200, 641)
            self.textBrowser_2.setVisible(False)
            self.isShrimp = not self.isShrimp
            
        else:
            #self.scrollarea_2.setGeometry(270, 310, 200, 641)
            self.scrollarea_2.move(411,310)
            self.PushButton_3.move(411,270)
            self.scrollarea_2.resize(200, 460)
            self.textBrowser_2.setVisible(True)
            self.isShrimp = not self.isShrimp
            

    def appendlogowidget(self, name):
        self.hbox = QtWidgets.QHBoxLayout()
        uname = QtWidgets.QPushButton(self.centralwidget)
        uname.setFont(QtGui.QFont("FZHTJW", 10))
        uname.setStyleSheet("""QPushButton{text-align:left; background-color:transparent; border-style:outset; border-width:0px; border-radius:0px; border-color:#F2F3F4}""" """QPushButton:hover{background-color:#F5F5F5}""")
        uname.setText(name)
        uname.setFixedHeight(29)
        uname.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.nameobj.update({name:uname})
        uname.clicked.connect(lambda: self.uname_f(name))

        #self.uname.setFixedSize(self.uname.width(),self.uname.height())
        self.uimagePath = "qq_logo.png"
        if name not in usernameavatar.keys():
            imgdata = open(self.uimagePath, 'rb').read()
            imgtype = self.uimagePath[len(self.uimagePath)-3:]
        else:
            imgdataplustype = usernameavatar[name]
            imgdata = imgdataplustype[:len(imgdataplustype)-3]
            imgtype = imgdataplustype[len(imgdataplustype)-3:]
        pixmap = self.mask_image(imgdata, 22, imgtype)

        #self.uimage = QtGui.QImage(self.uimagePath)
        
        self.ulabelreal = QtWidgets.QLabel(self.centralwidget)
        self.ulabelreal.setPixmap(pixmap)
        self.ulabelreal.setScaledContents(True)
        self.ulabelreal.setStyleSheet("border-width:0px")
        self.ulabelreal.setFixedSize(21,21)

        self.uhbox = QtWidgets.QHBoxLayout()
        self.left = QtWidgets.QLabel(self.centralwidget)
        self.left.setFixedWidth(1)
        self.uhbox.addWidget(self.left)
        self.uhbox.addWidget(self.ulabelreal)
        self.uhbox.addWidget(uname)
        
        self.vbox_2.insertLayout(self.vbox_2.count()-1,self.uhbox)


    def uname_f(self, name):
        self.nameflag.update({name : not self.nameflag[name]})
        self.nameobj[name].setStyleSheet("text-align:left; background-color:#E6E6E6; border-style:outset; border-radius:0px;")
        for key in self.nameobj:
            if key is not name:
                self.nameobj[key].setStyleSheet("""QPushButton{text-align:left; background-color:transparent; border-style:outset; border-width:0px; border-radius:0px; border-color:#F2F3F4}""" """QPushButton:hover{background-color:#F5F5F5}""")


 

    def append(self, msg, name, myself):
        self.createwidget(msg,name,myself)
        self.scrollarea.verticalScrollBar().rangeChanged.connect(self.change_scroll)

    def createwidget(self, msg, name, myself):
        if len(msg) == 0:
            return
        self.leftbar = QtWidgets.QLabel()
        self.leftbar.setStyleSheet("border-width:0px")
        self.rightbar = QtWidgets.QLabel()
        self.rightbar.setStyleSheet("border-width:0px")
        #name
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.setSpacing(0)
        self.name = QtWidgets.QLabel()
        self.name.setFont(QtGui.QFont("Times New Roman", 12))
        self.name.setStyleSheet("background-color:transparent; color:grey; border-width:0px")
        self.name.setText(name)
        self.name.setAlignment(QtCore.Qt.AlignBottom)

        if name not in usernameavatar.keys():
            imagePath = "qq_logo.png"
            imgdata = open(imagePath, 'rb').read()
            imgtype = imagePath[len(imagePath)-3:]
        else:
            imgdataplustype = usernameavatar[name]
            imgdata = imgdataplustype[:len(imgdataplustype)-3]
            imgtype = imgdataplustype[len(imgdataplustype)-3:]
        pixmap = self.mask_image(imgdata, 40, imgtype)

        #self.image = QtGui.QImage(self.imagePath)
        self.labelreal = QtWidgets.QLabel()
        self.labelreal.setPixmap(pixmap)
        self.labelreal.setScaledContents(True)
        self.labelreal.setStyleSheet("background-color: transparent; border-width:0px")
        self.labelreal.setFixedSize(40,40)
        self.leftvbox = QtWidgets.QVBoxLayout()
        if myself == 0:
            self.rightbar.setMinimumWidth(411 - self.labelreal.width()-self.name.width() -50)
            self.leftvbox.addWidget(self.labelreal)

        self.lbl = QtWidgets.QLabel()

        # Font, fontsize, background-color, font-color, border-color 
        self.lbl.setFont(QtGui.QFont(namefontdict[name][0], namefontdict[name][1]))
        self.lbl.setStyleSheet("background-color:" + namefontdict[name][2] +";"
                               "border-width: 2px;"
                               "border-style:solid;"
                              "border-radius:10px;"
                              "color:" + namefontdict[name][3] + ";"
                              "padding-left: 6px;"
                              "padding-right: 8px;"
                              "padding-top:4px;"
                              "padding-bottom:4px;"
                              "border-width:1px;"
                              "border-color:" + namefontdict[name][4] +";"
                              )

        font = QtGui.QFont(namefontdict[name][0], namefontdict[name][1])
        fm = QtGui.QFontMetrics(font)
        pixelshigh = fm.height()
        msg, nlines = self.breakmsg(msg, name)
        self.lbl.setText(msg)
        self.hboxnew = QtWidgets.QHBoxLayout()
        self.middlevbox = QtWidgets.QVBoxLayout()
        if myself == 0:
            self.name.setFixedHeight(pixelshigh*2-5)
            self.name.setFixedWidth(200)
            if 411 - 40 - self.lbl.width()- 70 < 0:
                self.leftbar.setMinimumWidth(411 - 40 - 280- 70)
            else:
                self.leftbar.setMinimumWidth(411 - 40 - self.lbl.width()- 70)
            #self.leftbar.setStyleSheet("background-color:black")
            
            self.newlabel = QtWidgets.QLabel()
            self.newlabel.setStyleSheet("border-width:0px")
            self.newlabel.setFixedWidth(45)
            #self.newlabel.setStyleSheet("background-color:black")
            self.leftvbox.addWidget(self.newlabel)
            self.middlevbox.addWidget(self.name)
            self.middlevbox.addWidget(self.lbl)
            self.hboxnew.addLayout(self.leftvbox)
            self.hboxnew.addLayout(self.middlevbox)
            self.hboxnew.addWidget(self.rightbar)

        else:
            if 411 - 40 - self.lbl.width()- 70 < 0:
                self.leftbar.setMinimumWidth(411 - 40 - 280 - 70)
            else:
                self.leftbar.setMinimumWidth(411 - 40 - self.lbl.width()- 70)
            if self.lbl.height()-40 < 0:
                self.rightbar.setMaximumHeight(0)
            else:
                self.rightbar.setMinimumHeight(self.lbl.height()-40)
            self.rightbar.setFixedWidth(40)
            self.rightbar.setAlignment(QtCore.Qt.AlignTop)
            self.rightlayout = QtWidgets.QVBoxLayout()
            self.rightlayout.addWidget(self.labelreal)
            self.rightlayout.addWidget(self.rightbar)
            self.middlelayout = QtWidgets.QVBoxLayout()
            self.middlelabel = QtWidgets.QLabel()
            self.middlelabel.setStyleSheet("border-width:0px")
            self.middlelabel.setMaximumHeight(5)

            self.middlelayout.addWidget(self.middlelabel)
            self.middlelayout.addWidget(self.lbl)
            self.hboxnew.addWidget(self.leftbar)
            self.hboxnew.addLayout(self.middlelayout)
            self.hboxnew.addLayout(self.rightlayout)
            #self.hboxnew.addWidget(self.label)
        
        #self.vbox.addLayout(self.hboxnew)
        self.vbox.insertLayout(self.vbox.count()-1, self.hboxnew)
        
    def breakmsg(self, msg, name):
        if len(msg) == 0:
            return msg
        font = QtGui.QFont(namefontdict[name][0], namefontdict[name][1])
        fm = QtGui.QFontMetrics(font)
        pixelswide = fm.width(msg)
        head = 0
        tail = 0
        msglen = len(msg)
        finalmsg = ""
        nlines = 1
        exceedonelinewide = 0
        while tail < msglen:
            tail += 1
            if msg[tail-1] =="\n":
                nlines+=1
            chunk = msg[head:tail]
            chunkpixelswide = fm.width(chunk)
            if chunkpixelswide > 230:
                exceedonelinewide = chunkpixelswide
                finalmsg += chunk + "\n"
                head = tail
                nlines += 1
            if tail == msglen-1 and chunkpixelswide <= 230:
                chunk = msg[head:]
                finalmsg += chunk
        if nlines == 1:
            self.lbl.setFixedWidth(pixelswide + 20)
            self.lbl.setFixedHeight(fm.height() + 20)
            return msg, int(nlines)
        else:
            self.lbl.setFixedWidth(exceedonelinewide + 20)
            self.lbl.setFixedHeight(fm.height()*nlines + int(nlines*2)+20)
            return finalmsg, int(nlines)

        

    def MinimizeWindow(self):
        self.showMinimized()
        self.cancel()


    def closeitself(self):
        global s
        s.close()
        print("server close in Connection")
        QtCore.QCoreApplication.instance().quit()
        sys.exit()

    def changetextbrowsertext(self):
        global messages
        clientMessage = self.plainTextEdit.text()
        self.append(clientMessage, username, 1)
        #self.scrollarea.verticalScrollBar().rangeChanged.connect(self.change_scroll)
        mymsg = username + " : " + clientMessage
        clientMessage = "T" +  f'{len(username):<{HeaderSize}}' + username  + f'{len(clientMessage):<{HeaderSize}}' + clientMessage
        try:
            s.send(bytes(clientMessage, 'utf-8'))
        except:
            s.close()
            print("server close in Connection")
            return
        self.changetextbrowsertextupdate(mymsg)
        self.plainTextEdit.clear()

    def change_scroll(self, min, max):
        self.scrollarea.verticalScrollBar().setSliderPosition(max)

    def changetextbrowsertextupdate(self, msg):
        self.textBrowser.append(msg)
        self.textBrowser.append("\n")

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())
        

    def display(self):
        global shouldUpdate
        global updateonlineusers
        global onlineuserslist
        global appmsg
        global usermessages
        global username
        global image
        global imgtype
        global appendimage
        global getSnap
        global finishsending
        global login
        self.useless = QtWidgets.QWidget()
        if shouldUpdate:
            self.textBrowser.append(newmsg)
            self.textBrowser.append("\n")
            if otherusername == username:
                self.append(newmsg, otherusername,1)
            else:
                self.append(newmsg, otherusername,0)
            shouldUpdate = False
        if updateonlineusers:
            self.nameflag.clear()
            self.nameobj.clear()
            self.PushButton_3.setText("群成员 " + f'{len(onlineuserslist)}')
            self.clearLayout(self.vbox_2)
            self.vbox_2.setSpacing(2)
            self.vbox_2.addStretch()
            for user in onlineuserslist:
                self.nameflag.update({user:False})
                self.appendlogowidget(user)
            updateonlineusers = False
            print("Finish updating onlineuser")
        if appmsg:
            for i in range(0, len(clientMessageMapperIndex)):
                datatype = clientMessageMapperIndex[i][0]
                if datatype == 'I':
                    name = clientMessageMapperIndex[i][4:]
                elif datatype == 'T':
                    name = clientMessageMapperIndex[i][1:]
                data = clientMessageMapper[i]

                if name == username:
                    if datatype == 'T':
                        self.append(data, name, 1)
                    elif datatype == 'I':
                        imagedata = data
                        imagetype = clientMessageMapperIndex[i][1:4]
                        self.appendPicture(imagedata, imagetype , name, 1)
                else:
                    if datatype == 'T':
                        self.append(data, name, 0)
                    elif datatype == 'I':
                        imagedata = data
                        imagetype = clientMessageMapperIndex[i][1:4] 
                        self.appendPicture(imagedata, imagetype , name, 0)

            appmsg = False
            

        if appendimage:
            self.appendPicture(image, imgtype, imageclientname, 0)
            appendimage = False
            
        if getSnap:
            print("Start getting snap image")
            getSnap = False
            
            self.getPictureFromFileSystem_2(True, 'snapshot.jpg')
            print("Finish getting snap image")
            #login = True
            
            #print("Refresh the page")
            updateonlineusers = True
        if finishsending:
            finishsending = False
            appmsg = True



    def update(self):
        global messages
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.display)
        self.timer.start(100)

    def closewindow(self):
        QtCore.QCoreApplication.instance().quit()


    def mask_background_image(self, imgdata, img_type = 'jpg'):
            # Load image 
        image = QtGui.QImage.fromData(imgdata, img_type) 
    
        # convert image to 32-bit ARGB (adds an alpha  
        # channel ie transparency factor): 
        image.convertToFormat(QtGui.QImage.Format_ARGB32) 
    
        rect =  QtCore.QRect( 
            self.pos().x() - self.backgroundImage.pos().x(),
            self.pos().y() - self.backgroundImage.pos().y(), 
            self.backcolor.width(), 
            self.backcolor.height(), 
        ) 
        image = image.copy(rect)
    
        pm = QtGui.QPixmap.fromImage(image)
        image.save("outputimg.jpg")
        #pm.setDevicePixelRatio(pr) 
       # size *= pr 
        #pm = pm.scaled(self.backcolor.width(), self.backcolor.height(), QtCore.Qt.KeepAspectRatio,  
         #                       QtCore.Qt.SmoothTransformation) 
    
        # return back the pixmap data 
        return pm 

    
    def mask_image(self, imgdata, size = 32 , imgtype_temp ='jpg'):
  
        # Load image 
        image = QtGui.QImage.fromData(imgdata, imgtype_temp) 
    
        # convert image to 32-bit ARGB (adds an alpha 
        # channel ie transparency factor): 
        image.convertToFormat(QtGui.QImage.Format_ARGB32) 
        
        # Crop image to a square: 
        imgsize = min(image.width(), image.height())
        rect = QtCore.QRect( 
            int((image.width() - imgsize) / 2), 
            int((image.height() - imgsize) / 2), 
            int(imgsize), 
            int(imgsize), 
        )
        
        image = image.copy(rect) 
    
        # Create the output image with the same dimensions  
        # and an alpha channel and make it completely transparent: 
        # Format_ARGB32
        out_img = QtGui.QImage(imgsize, imgsize, QtGui.QImage.Format_RGBA64) 
        out_img.fill(QtCore.Qt.transparent) 
        
        # Create a texture brush and paint a circle  
        # with the original image onto the output image: 
        brush = QtGui.QBrush(image) 
    
        # Paint the output image 
        painter = QtGui.QPainter(out_img) 
        painter.setBrush(brush) 
        
        # Don't draw an outline 
        painter.setPen(QtCore.Qt.NoPen) 
    
        # drawing circle 
        painter.drawEllipse(0, 0, imgsize, imgsize) 
    
        # closing painter event 
        painter.end() 
        
        # Convert the image to a pixmap and rescale it.  
        pr = QtGui.QWindow().devicePixelRatio() 
        pm = QtGui.QPixmap.fromImage(out_img) 
        pm.setDevicePixelRatio(pr) 
        size *= pr 
        pm = pm.scaled(int(size), int(size), QtCore.Qt.KeepAspectRatio,  
                                QtCore.Qt.SmoothTransformation) 
    
        # return back the pixmap data 
        return pm

class WScreenShot(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WScreenShot, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet('''background-color:black; ''')
        self.setWindowOpacity(0.6)
        desktopRect = QtWidgets.QDesktopWidget().screenGeometry()
        self.setGeometry(desktopRect)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.blackMask = QtGui.QBitmap(desktopRect.size())
        self.blackMask.fill(QtCore.Qt.black)
        self.mask = self.blackMask.copy()
        self.isDrawing = False
        self.startPoint = QtCore.QPoint()
        self.endPoint = QtCore.QPoint()
 
    def paintEvent(self, event):
        if self.isDrawing:
            self.mask = self.blackMask.copy()
            pp =QtGui.QPainter(self.mask)
            pen =QtGui.QPen()
            pen.setStyle(QtCore.Qt.NoPen)
            pp.setPen(pen)
            brush = QtGui.QBrush(QtCore.Qt.white)
            pp.setBrush(brush)
            pp.drawRect(QtCore.QRect(self.startPoint, self.endPoint))
            self.setMask(QtGui.QBitmap(self.mask))
 
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.startPoint = event.pos()
            self.endPoint = self.startPoint
            self.isDrawing = True
 
    def mouseMoveEvent(self, event):
        if self.isDrawing:
            self.endPoint = event.pos()
            self.update()
 
    def mouseReleaseEvent(self, event):
        global login
        global getSnap
        if event.button() == QtCore.Qt.LeftButton:
            self.endPoint = event.pos()
            screenshot = QtWidgets.QApplication.primaryScreen().grabWindow(QtWidgets.QApplication.desktop().winId())
            rect = QtCore.QRect(self.startPoint, self.endPoint)
            outputRegion = screenshot.copy(rect)
            print(outputRegion)
            outputRegion.save('snapshot.jpg', format='JPG', quality=100)
            print("saved image")
            getSnap = True
            print("set getsnap to True")
            #QtCore.QCoreApplication.instance().quit()
            self.close()
            login = True
            print("successfully close the window")


def getlentext(c):
    usname = ""
    unba = bytearray()
    b = c.recv(HeaderSize)    
    namelen = int(b)
    while True:
        b = c.recv(1)
        unba.extend(b)
        try:
            usname = unba.decode("utf-8")
        except:
            continue
        if len(usname) == namelen:
            break
    return usname

def sendtoserver(msg):
    global s
    try:
        s.send(bytes(msg,'utf-8'))
    except:
        s.close()
        print("server close in Connection")

def getservermessage(s, usname):
    global otherusername
    global recvsize
    global shouldUpdate
    global newmsg
    full_msg = ""
    fullmsginbyte = bytearray()
    try:
        b = s.recv(HeaderSize)
        msglen = int(b)
    except:
        s.close()
        print("server close in Connection")
    while True:
        try:
            b = s.recv(recvsize)
        except:
            s.close()
            print("server close in Connection")
        fullmsginbyte.extend(b)
        try:
            full_msg = fullmsginbyte.decode("utf-8")
        except:
            continue
        if len(full_msg) == msglen:
            newmsg = usname + " : " + full_msg
            newmsg = full_msg
            otherusername = usname
            shouldUpdate = True
            break

def parseonlineusers(s):
    try:
        b = s.recv(HeaderSize)
        numonlineusers = int(b)
    except:
        s.close()
        print("server close in Connection")
        return
    global onlineuserslist
    onlineuserslist.clear()
    while numonlineusers > 0:
        onlineuserslist.append(getlentext(s))
        numonlineusers -= 1

def getAvatar(s, usname):
    global recvsize
    global usernameavatar
    global updateonlineusers
    full_msg = b''
    try:
        b = s.recv(HeaderSize)
        msglen = int(b)
    except:
        s.close()
        print("server close in Connection")
        return
    while True:
        try:
            msg = s.recv(recvsize)
        except:
            s.close()
            print("server close in Connection")
            return
        full_msg += msg
        if len(full_msg)-3 == msglen:
            usernameavatar[usname] = full_msg
            print("got all avatar data and stored")
            updateonlineusers = True
            break 

def appendToAvatarDict(s):
    global recvsize
    global usernameavatar
    try:
        numAvatars = int(s.recv(HeaderSize))
    except:
        s.close()
        print("server close in Connection")
    count = 0
    while count < numAvatars:
        usname = getlentext(s)
        try:
            imgdatalen = int(s.recv(HeaderSize))
            imgdata = s.recv(imgdatalen)
        except:
            s.close()
            print("server close in Connection")
        usernameavatar[usname] = imgdata
        count += 1
    
        
def AppendAllMsgs(s):
    global usermessages
    global clientMessageMapper
    global clientMessageMapperIndex
    global finishsending
    try:
        nmsg = int(s.recv(HeaderSize))
    except:
        s.close()
        print("server close in Connection")
    count = 0
    while count < nmsg:
        #try:
        user = getlentext(s)
        print(user)
        datatype = s.recv(1).decode("utf-8")
        print(datatype)
        msglen = int(s.recv(HeaderSize))
        print(msglen)
        itype = ""
        if datatype == 'T':
            #msg = s.recv(msglen).decode("utf-8")
            msg = ""
            fullmsginbyte = bytearray()
            while True:
                try:
                    b = s.recv(1)
                except:
                    s.close()
                    print("server close in Connection")
                fullmsginbyte.extend(b)
                try:
                    msg = fullmsginbyte.decode("utf-8")
                except:
                    continue
                if len(msg) == msglen:
                    break

        elif datatype == 'I':
            msg = b''
            #tail = 0
            while True:
                msg += s.recv(recvsize)
                #tail += recvsize
                if msglen - 3 <= len(msg) + recvsize:
                    msg += s.recv(msglen - 3 - len(msg))
                    break

            itype = s.recv(3).decode("utf-8")
        #except:
         #   print("Why closed?")
         #   s.close()
        
        if datatype == 'T':
            clientMessageMapperIndex.append('T' + user)
            clientMessageMapper.append(msg)
            print(msg)
        elif datatype == 'I':
            clientMessageMapperIndex.append('I' + itype + user )
            clientMessageMapper.append(msg)
        
        count += 1
    finishsending = True

def getimage(s, usname):
    global image
    global appendimage
    global imgtype
    global finishsending
    full_img_data = b''
    print("ImageUsername is " + usname)
    try:
        imglen = int(s.recv(HeaderSize))
    except:
        s.close()
        print("server close in Connection")
    while True:
        try:
            data = s.recv(recvsize)
        except:
            s.close()
            print("server close in Connection")
            return
        full_img_data += data
        if len(full_img_data) > imglen - recvsize - 3:
            while True:
                try:
                    data = s.recv(1)
                except:
                    s.close()
                    print("server close in Connection")
                    return
                full_img_data+= data
                if len(full_img_data) == imglen:
                    break
            break
    #full_img_data += data
    imgtype = s.recv(3).decode("utf-8")
    #if len(full_img_data) - 3 == imglen:
    image = full_img_data
    appendimage = True
        #break
    finishsending = True

def run():
    global s
    global login
    global username
    global newmsg
    global shouldUpdate
    global loginqmsg
    global regisqmsg
    global regisqmsgs
    global updateonlineusers
    global imageclientname
    global defaultFont
    global namefontdict
    while True:
        try:
            print("Started receiving")
            sig = s.recv(1)
            print("Receive 1 byte")
        except:
            break
        signal = sig.decode("utf-8")
        print("successfully decoded " + signal)
        if signal == 'T':
            usname = getlentext(s)
            getservermessage(s, usname)
        if signal == 'J':
            print("Receive Join Signal")
            usname = getlentext(s)
            if usname != username:
                newmsg = usname + " has joined the chat"
               # shouldUpdate = True
            else:
                print("set login to true")
                login = True
            namefontdict[usname] = defaultFont
        if signal == 'F':
            usname = getlentext(s)
            if usname == username:
                newmsg = getlentext(s)
                loginqmsg = True

        if signal == 'W':
            usname = getlentext(s)
            if usname == username:
                newmsg = getlentext(s)
                regisqmsg = True

        if signal == 'S':
            usname = getlentext(s)
            if usname == username:
                newmsg = getlentext(s)
                regisqmsgs = True

        if signal == 'L':
            usname = getlentext(s)
            if usname != username:
                newmsg = usname + " has left the chat"
               # shouldUpdate = True

        if signal == 'U':
            parseonlineusers(s)
            updateonlineusers = True

        if signal == 'A':
            usname = getlentext(s)
            getAvatar(s, usname)

        if signal == 'V':
            appendToAvatarDict(s)

        if signal == 'M':
            AppendAllMsgs(s)

        if signal == 'I':
            imageclientname = getlentext(s)
            getimage(s, usname)
        if signal == 'Q':
            try:
                usname = getlentext(s)
                sizeofbytes = int(s.recv(HeaderSize))
                fontlistbyte = s.recv(sizeofbytes)
                fontlist = pickle.loads(fontlistbyte)
                namefontdict[usname] = fontlist
            except:
                s.close()
                print("server close in Connection")
        if signal == 'B':
        
            nnamefont = int(s.recv(HeaderSize))
            print(nnamefont)
            count = 0
            while count < nnamefont:
                usname = getlentext(s)
                sizeofbytes = int(s.recv(HeaderSize))
                fontlistbyte = s.recv(sizeofbytes)
                fontlist = pickle.loads(fontlistbyte)
                namefontdict[usname] = fontlist
                count += 1

def loginwin():
    app = QtWidgets.QApplication(sys.argv)
    lw = LoginWindow()
    lw.update()
    app.exec_()

def registerwin():
    app = QtWidgets.QApplication(sys.argv)

    rw = RegisterWindow()
    rw.update()
    rw.backgroundtimer()
    app.exec_()

def chatwin():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.update()
    app.exec_()

def snapwin():
    app = QtWidgets.QApplication(sys.argv)
    ss = WScreenShot()
    ss.show()
    app.exec_()

if __name__ == "__main__":
    MsgThread = threading.Thread(target=run)
    MsgThread.daemon = True
    MsgThread.start()
    loginwin()
    while True:
        if regis:
            regis = False
            registerwin()
        if loginback:
            loginback = False
            loginwin()
        if login:
            login = False
            chatwin()
        if loginqmsg:
            loginqmsg = False
        if snapflag:
            snapflag = False
            snapwin()
            