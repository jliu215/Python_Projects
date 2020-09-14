import sys
import os
import socket

from PyQt5 import QtCore, QtGui, QtWidgets


CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class RegisterWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Set Window properties
        self.setObjectName("MainWindow")
        self.resize(460, 610)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.statusBar().hide()
        self.setStyleSheet("border-radius:3px;" )
        
        

        # top_left logo
        self.imagelogo_top_left = QtGui.QImage(CURRENT_DIRECTORY +"/WidgetsIcons/" + "qq_sign_up_logo.png")
        self.labellogo_top_left = QtWidgets.QLabel(self)
        self.labellogo_top_left.setGeometry(0,-13,60,60)
        self.labellogo_top_left.setPixmap(QtGui.QPixmap.fromImage(self.imagelogo_top_left))
        self.labellogo_top_left.setScaledContents(True)
        self.labellogo_top_left.setStyleSheet("background-color:transparent; border-color:transparent")

        self.borderShadow = QtWidgets.QWidget(self)
        self.borderShadow.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))
        self.borderShadow.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        # centralwidget
        self.centralwidget = QtWidgets.QWidget(self.borderShadow)
        self.centralwidget.setGeometry(self.borderShadow.x()+5, self.borderShadow.y()+5, 450, 600)

        eff = QtWidgets.QGraphicsDropShadowEffect()
        eff.setBlurRadius(11)
        eff.setOffset(0, 0)
        self.centralwidget.setGraphicsEffect(eff)


        # labels for background images
        self.imagebackground = QtGui.QImage(CURRENT_DIRECTORY + "/Images/" + "qq_sign_up_background.png")
        self.labelbackground = QtWidgets.QLabel(self.centralwidget)
        self.labelbackground.setGeometry(0,0,self.width(),self.height())
        self.labelbackground.setPixmap(QtGui.QPixmap.fromImage(self.imagebackground))
        self.labelbackground.setScaledContents(True)
        

        self.imagebackground2 = QtGui.QImage(CURRENT_DIRECTORY + "/Images/" + "qq_sign_up_background2.png")
        self.labelbackground2 = QtWidgets.QLabel(self.centralwidget)
        self.labelbackground2.setGeometry(0,0,self.width(),self.height())
        self.labelbackground2.setPixmap(QtGui.QPixmap.fromImage(self.imagebackground2))
        self.labelbackground2.setScaledContents(True)

        self.imagebackground3 = QtGui.QImage(CURRENT_DIRECTORY + "/Images/" + "qq_sign_up_back_ground3.png")
        self.labelbackground3 = QtWidgets.QLabel(self.centralwidget)
        self.labelbackground3.setGeometry(0,0,self.width(),self.height())
        self.labelbackground3.setPixmap(QtGui.QPixmap.fromImage(self.imagebackground3))
        self.labelbackground3.setScaledContents(True)

        self.backgroundimageList = []
        self.backgroundimageList.append(self.labelbackground)
        self.backgroundimageList.append(self.labelbackground2)
        self.backgroundimageList.append(self.labelbackground3)

        
        # Text be shown on the screen
        self.bigtext = QtWidgets.QLabel(self.centralwidget)
        self.bigtext.setGeometry(QtCore.QRect(15,30,180,50))
        self.bigtext.setObjectName("bigtext")
        self.bigtext.setFont(QtGui.QFont("Times font", 22))
        self.bigtext.setStyleSheet(" font-weight: bold; color: black; border-color:transparent")

        self.smalltext = QtWidgets.QLabel(self.centralwidget)
        self.smalltext.setGeometry(QtCore.QRect(15,70,220,30))
        self.smalltext.setObjectName("smalltext")
        self.smalltext.setFont(QtGui.QFont("Times font", 18))
        self.smalltext.setStyleSheet("color: black; border-color:transparent")

        # Redesigned Close Button
        self.closebutton = QtWidgets.QPushButton(self.centralwidget)
        self.closebutton.setGeometry(418, 0, 32, 32)
        self.closebutton.setObjectName("closebutton")
        self.closebutton.setStyleSheet("QPushButton:hover""{""background-color :#FF431B;""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.closebutton.clicked.connect(lambda: self.closewindow(True))

        # Redesigned Minimized Button
        self.minbutton = QtWidgets.QPushButton(self.centralwidget)
        self.minbutton.setGeometry(386, 0, 32, 32)
        self.minbutton.setObjectName("minbutton")
        self.minbutton.setStyleSheet("QPushButton:hover""{""background-color :rgba(255, 255, 255, 50);""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.minbutton.clicked.connect(self.MinimizeWindow)

        # LineEdit for typing new username
        self.newaccount = QtWidgets.QLineEdit(self.centralwidget)
        self.newaccount.setGeometry(QtCore.QRect(105, 260, 240, 30))
        self.newaccount.setFont(QtGui.QFont("Arial", 11))
        self.newaccount.setTextMargins(5 ,0, 0, 0)
        self.newaccount.setFrame(False)
        self.newaccount.setStyleSheet("QLineEdit{""border-width: 0.5px; border-style: solid; border-color:#7c7d82  ""}" "QLineEdit:hover{""border-width:1.3px; border-color: #0184b0""}")

        # LineEdit for typing new password
        self.newpassword = QtWidgets.QLineEdit(self.centralwidget)
        self.newpassword.setGeometry(QtCore.QRect(105, 300, 240, 30))
        self.newpassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newpassword.setTextMargins(5 ,0, 0, 0)
        self.newpassword.setFont(QtGui.QFont("Arial", 11))
        self.newpassword.setFrame(False)
        self.newpassword.setStyleSheet("QLineEdit{""border-width: 0.5px; border-style: solid; border-color:#7c7d82""}" "QLineEdit:hover{""border-width:1.3px; border-color: #0184b0 ""}")

        # LineEdit for typing new password replication
        self.newpassword_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.newpassword_2.setGeometry(QtCore.QRect(105, 340, 240, 30))
        self.newpassword_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newpassword_2.setTextMargins(5 ,0, 0, 0)
        self.newpassword_2.setFont(QtGui.QFont("Arial", 11))
        self.newpassword_2.setFrame(False)
        self.newpassword_2.setStyleSheet("QLineEdit{""border-width: 0.5px; border-style: solid; border-color:#7c7d82""}" "QLineEdit:hover{""border-width:1.3px; border-color: #0184b0""}")

        # Pushbutton for confirmation
        self.confirmButton = QtWidgets.QPushButton(self.centralwidget)
        self.confirmButton.setGeometry(QtCore.QRect(105, 385, 240, 40))
        self.confirmButton.setObjectName("confirmButton")
        self.confirmButton.setStyleSheet("QPushButton:hover""{""background-color : #4bace1;""}" "QPushButton""{""background-color:#009ce6; color: white; border-style:outset; border-radius:5px; min-width:10em; padding: 6px; ""}" "QPushButton:pressed""{""background-color:#2782bb""}")
        self.confirmButton.setFont(QtGui.QFont("Arial", 12))
        self.confirmButton.clicked.connect(self.saveinfo)

        # PushButton for redircting back to login window
        self.returnButton = QtWidgets.QPushButton(self.centralwidget)
        self.returnButton.setGeometry(QtCore.QRect(155, 460, 75, 30))
        self.returnButton.setObjectName("returnButton")
        self.returnButton.setStyleSheet("QPushButton:hover""{""background-color : #7c7d82;""}" "QPushButton""{""background-color:#6b6e77; color: white; border-radius:5px; min-width:10em; padding: 6px;""}" "QPushButton:pressed""{""background-color:#2b2a30""}")
        self.returnButton.setFont(QtGui.QFont("Arial", 10))
        self.returnButton.clicked.connect(self.windowSlideDownTimerFunc)

        # set the centralwidget on the window
        self.setCentralWidget(self.borderShadow)

        # Call for retranslation
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # Variable to enable dragging window
        self.oldPos = self.pos()

        # User input info
        self.username = ""
        self.password = ""


        self.SignupWinIsOff = False

        self.show()

    # Mouse Events for dragging window
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "注册"))
        self.confirmButton.setText(_translate("confirmButton", "立即注册"))
        self.returnButton.setText(_translate("returnButton", "登录"))
        self.closebutton.setText(_translate("closebutton", u'\u2715'))
        self.minbutton.setText(_translate("minbutton", u'\u2015'))
        self.bigtext.setText(_translate("bigtext","欢迎注册QQ"))
        self.smalltext.setText(_translate("smalltext","每一天，乐在沟通。"))
        self.newaccount.setPlaceholderText("新账号")
        self.newpassword.setPlaceholderText("密码")
        self.newpassword_2.setPlaceholderText("确认密码")

    # Window Minmize function
    def MinimizeWindow(self):
        self.showMinimized()

    # Function for timer to slide window
    def windowSlideDownTimerFunc(self):
        self.windowSlideDownTimer = QtCore.QTimer()
        self.windowSlideDownTimer.timeout.connect(self.windowSlideUp)
        self.windowSlideDownTimer.start(15)

    def windowSlideUp(self):
        if self.height() > 0:
            self.resize(self.width(), self.height()-10)
        else:
            if not self.SignupWinIsOff:
                if self.loginwin is None:
                    self.close()
                    self.windowSlideDownTimer.stop()
                    return
                self.loginwin.show()
                self.loginwin.move(self.pos())
                self.s.close()
                self.SignupWinIsOff = True
            if self.loginwin.height() < 337:
                self.loginwin.resize(self.loginwin.width(),self.loginwin.height()+10)
            else:
                self.SignupWinIsOff = False
                self.hide()
                self.windowSlideDownTimer.stop()
        


    # Timer for changing background image
    def backgroundtimer(self):
        self.counter = 0
        self.newtimer = QtCore.QTimer()
        self.newtimer.timeout.connect(self.changeBackground)
        self.newtimer.start(5000)

    # Function to change background image
    def changeBackground(self):
        self.backgroundimageList[self.counter].raise_()
        #self.centralwidget.raise_()
        self.bigtext.raise_()
        self.smalltext.raise_()
        self.closebutton.raise_()
        self.minbutton.raise_()
        self.newaccount.raise_()
        self.newpassword.raise_()
        self.newpassword_2.raise_()
        self.confirmButton.raise_()
        self.returnButton.raise_()
        self.labellogo_top_left.raise_()
        self.counter += 1
        if self.counter == len(self.backgroundimageList):
            self.counter = 0
        
        
    # Save the information
    def saveinfo(self):
        self.username = self.newaccount.text()
        self.password = self.newpassword.text()
        if len(self.username) != 0 and len(self.password) != 0:
            pass2 = self.newpassword_2.text()
            if self.password != pass2:
                newmsg = "密码不匹配"
                self.messagesbox(newmsg, True)
            else:
                msg = 'R' + f'{len(self.username):<{self.HeaderSize}}' + self.username + f'{len(self.password):<{self.HeaderSize}}' + self.password
                try:
                    self.s.send(bytes(msg,'utf-8'))
                except:
                    self.s.close()

    # Close the window
    def closewindow(self, disconnect):
        if disconnect:
            self.s.close()
            if self.loginwin is None:
                QtCore.QCoreApplication.instance().quit()
                return
            self.loginwin.close()
        QtCore.QCoreApplication.instance().quit()
        

    # A prompt box to display MsgBox
    def messagesbox(self, msg, isCritical):
        self.newpassword.clear()
        self.newpassword_2.clear()
        msgbox = QtWidgets.QMessageBox()
        
        msgbox.setText(msg)
        if isCritical:
            msgbox.setWindowTitle("Error")
            msgbox.setIcon(QtWidgets.QMessageBox.Critical)
            msgbox.setStyleSheet("color: red; font-weight: bold; font: 16px")
        else:
            msgbox.setWindowTitle("Success")
            msgbox.setIcon(QtWidgets.QMessageBox.Information)
            self.newaccount.clear()
            msgbox.setStyleSheet("color: Blue; font-weight: bold; font: 16px")
        
        msgbox.setFont(QtGui.QFont("Times font", 20))
        msgbox.exec_()

    # update all info needed for connections
    def recvInfo(self, socket, headersize, loginwin):
        self.s = socket
        self.HeaderSize = headersize
        self.loginwin = loginwin

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HeaderSize = 10
    app = QtWidgets.QApplication(sys.argv)
    rw = RegisterWindow()
    rw.recvInfo(s, HeaderSize, None)
    rw.backgroundtimer()
    app.exec_()
