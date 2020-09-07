import sys
import os
import socket

from PyQt5 import QtCore, QtGui, QtWidgets


CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Initializing the window
        self.setObjectName("MainWindow")
        self.resize(425,327)
        self.setWindowIcon(QtGui.QIcon(CURRENT_DIRECTORY + "/WidgetsIcons/" + "qq_icon.png"))
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background-color:white; border-radius:5px")
        self.statusBar().hide()

        # Setting a centralWidget to be on the window
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # The background color of the window
        self.backgroundColor=QtWidgets.QLabel(self.centralwidget)
        self.backgroundColor.setGeometry(QtCore.QRect(0,0,425,130))
        
        # Manual Close Button
        self.closebutton = QtWidgets.QPushButton(self.centralwidget)
        self.closebutton.setGeometry(393, 0, 32, 32)
        self.closebutton.setObjectName("closebutton")
        self.closebutton.setStyleSheet("QPushButton:hover""{""background-color :#FF431B;""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.closebutton.clicked.connect(lambda: self.closeItself(True))

        # Manual Min Button
        self.minbutton = QtWidgets.QPushButton(self.centralwidget)
        self.minbutton.setGeometry(361, 0, 32, 32)
        self.minbutton.setObjectName("minbutton")
        self.minbutton.setStyleSheet("QPushButton:hover""{""background-color :rgba(255, 255, 255, 50);""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.minbutton.clicked.connect(self.MinimizeWindow)

        # A Logo at the center of the window
        self.image = QtGui.QImage(CURRENT_DIRECTORY + "/WidgetsIcons/" +"qq_logo.png")
        self.centerlogo = QtWidgets.QLabel(self)
        self.centerlogo.setGeometry(180,93,60,60)
        self.centerlogo.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.centerlogo.setScaledContents(True)
        self.centerlogo.setStyleSheet("background-color: transparent")

        # A Logo on the top left of the window
        self.imagelogo_top_left = QtGui.QImage(CURRENT_DIRECTORY + "/WidgetsIcons/" +"qq_logo_top_left.png")
        self.labellogo_top_left = QtWidgets.QLabel(self)
        self.labellogo_top_left.setGeometry(20,10,25,40)
        self.labellogo_top_left.setPixmap(QtGui.QPixmap.fromImage(self.imagelogo_top_left))
        self.labellogo_top_left.setScaledContents(True)
        self.labellogo_top_left.setStyleSheet("background-color:transparent")
        
        # Username lineEdit
        self.usernameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.usernameEdit.setGeometry(QtCore.QRect(95, 160, 240, 30))
        self.usernameEdit.setObjectName("usernameEdit")
        self.usernameEdit.setFont(QtGui.QFont("Arial", 11))
        self.usernameEdit.setTextMargins(22 ,0, 0, 0)
        self.usernameEdit.setFrame(False)
        self.usernameEdit.setStyleSheet("QLineEdit{""border-width: 0.5px; border-style: solid; border-color: white white grey white""}" "QLineEdit:hover{""border-width:1.3px; border-color: white white #0184b0 white""}")

        # Password lineEdit
        self.passwordEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordEdit.setGeometry(QtCore.QRect(95, 200, 240, 30))
        self.passwordEdit.setObjectName("passwordEdit")
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setTextMargins(22 ,0, 0, 0)
        self.passwordEdit.setFont(QtGui.QFont("Arial", 11))
        self.passwordEdit.setFrame(False)
        self.passwordEdit.setStyleSheet("QLineEdit{""border-width: 0.5px; border-style: solid; border-color: white white grey white""}" "QLineEdit:hover{""border-width:1.3px; border-color: white white #0184b0 white""}")

       

        # A logo for username lineEdit for visual purpose
        self.imagePathusername = CURRENT_DIRECTORY + "/WidgetsIcons/" + "qq_username.png"
        self.imageusername = QtGui.QImage(self.imagePathusername)
        self.labelusername = QtWidgets.QLabel(self)
        self.labelusername.setGeometry(100,163,20,25)
        self.labelusername.setPixmap(QtGui.QPixmap.fromImage(self.imageusername))
        self.labelusername.setScaledContents(True)

        # A logo for password lineEdit for visual purpose
        self.imagePathlock = CURRENT_DIRECTORY + "/WidgetsIcons/" + "qq_lock.png"
        self.imagelock = QtGui.QImage(self.imagePathlock)
        self.labellock = QtWidgets.QLabel(self)
        self.labellock.setGeometry(100,203,20,25)
        self.labellock.setPixmap(QtGui.QPixmap.fromImage(self.imagelock))
        self.labellock.setScaledContents(True)
       
        # PushButton for redirecting to the Main Window
        self.confirmButton = QtWidgets.QPushButton(self.centralwidget)
        self.confirmButton.setGeometry(QtCore.QRect(95, 270, 240, 40))
        self.confirmButton.setObjectName("confirmButton")
        self.confirmButton.setStyleSheet("QPushButton:hover""{""background-color : #4bace1;""}" "QPushButton""{""background-color:#009ce6; color: white; border-style:outset; border-width:1px; border-radius:5px; border-color:#01aef0; min-width:10em; padding: 6px;""}" "QPushButton:pressed""{""background-color:#2782bb""}")
        self.confirmButton.setFont(QtGui.QFont("Arial", 10))
        self.confirmButton.clicked.connect(self.reconnect)

       # PushButton for redirecting to registration window
        self.signupButton = QtWidgets.QPushButton(self.centralwidget)
        self.signupButton.setGeometry(QtCore.QRect(5, 300, 73, 23))
        self.signupButton.setObjectName("signupButton")
        self.signupButton.clicked.connect(lambda: self.closeItself(False))
        self.signupButton.setStyleSheet("QPushButton{""border:none; color:grey""}" "QPushButton:hover{""color:black""}")
        self.signupButton.setFont(QtGui.QFont("Arial", 9))
        self.signupButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(95, 270, 240, 40))
        self.cancelButton.setStyleSheet("QPushButton:hover""{""background-color :rgba(255, 255, 255, 50);""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.cancelButton.clicked.connect(self.cancelConnection)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.hide()


        # Finally setting centralwidget on the window
        self.setCentralWidget(self.centralwidget)
        
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # set original position for dragging frameless window
        self.oldPos = self.pos()

        self.ireverse = False
        self.jreverse = True
        self.i = 255
        self.j = 0
        self.ioutputcolor = ""
        self.joutputcolor = ""

        

        # Show the window
        self.show()

    # Renaming some items
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "QQ登录"))
        self.confirmButton.setText(_translate("confirmButton", "登录"))
        self.signupButton.setText(_translate("signupButton", "注册账号"))
        self.closebutton.setText(_translate("closebutton", u'\u2715'))
        self.minbutton.setText(_translate("minbutton", u'\u2015'))
        self.cancelButton.setText(_translate("cancelButton", "取消"))
        self.usernameEdit.setPlaceholderText("账号")
        self.passwordEdit.setPlaceholderText("密码")
        



    # Mouse Dragging Window Functions
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def MinimizeWindow(self):
        self.showMinimized()

    # Save the user inputs and send to server for authentication
    def saveinfo(self):
        self.Username = self.usernameEdit.text()
        self.PassWord = self.passwordEdit.text()
        if len(self.Username) != 0 and len(self.PassWord) != 0:
            msg = 'L' + f'{len(self.Username):<{self.HeaderSize}}' + self.Username + f'{len(self.PassWord):<{self.HeaderSize}}' + self.PassWord
            try:
                self.s.send(bytes(msg,'utf-8'))
            except:
                self.s.close()

    def reconnect(self):
        if len(self.usernameEdit.text()) == 0 or len(self.passwordEdit.text()) == 0:
            return
        self.LoadingPage()
        self.reconnectTimer = QtCore.QTimer()
        self.reconnectTimer.timeout.connect(self.reconnecting)
        self.reconnectTimer.setSingleShot(True)
        self.reconnectTimer.start(4000)

    def reconnecting(self):
        try:
            self.s.connect((socket.gethostname(), 1234))
            self.saveinfo()
            self.closescreenAnimationTimer()
        except:
            self.prompting("登录超时，请检查你的网络或者本地防火墙的设置")
            self.cancelConnection()

    def screenAnimationTimer(self, isDown):
        self.animationTimer = QtCore.QTimer()
        if not isDown:
            self.animationTimer.timeout.connect(self.slideDownBackground)
        else:
            self.animationTimer.timeout.connect(self.slideUpBackground)
        self.animationTimer.start(10)

    def closescreenAnimationTimer(self):
        self.csAnimationTimer = QtCore.QTimer()
        self.csAnimationTimer.timeout.connect(self.slideRightWindow)
        self.csAnimationTimer.start(15)

    def slideDownBackground(self):
        if(self.backgroundColor.height() <= self.height()):
            self.backgroundColor.resize(self.width(),self.backgroundColor.height() + 10)
        else:
            self.animationTimer.stop()
    def slideUpBackground(self):
        if(self.backgroundColor.height() > 130):
            self.backgroundColor.resize(self.width(),self.backgroundColor.height() - 10)
        else:
            self.animationTimer.stop()

    def slideRightWindow(self):
        print(self.width())
        if self.width() > 5:
            self.resize(self.width()-10, self.height())
        elif self.height() > 0 :
            self.resize(self.width(), self.height()-10)
        else:
            self.csAnimationTimer.stop()
            self.close()

    def LoadingPage(self):
        self.screenAnimationTimer(False)
        self.labelusername.hide()
        self.labellock.hide()
        self.confirmButton.hide()
        self.signupButton.hide()
        self.usernameEdit.hide()
        self.passwordEdit.hide()
        self.cancelButton.show()

    def cancelConnection(self):
        self.reconnectTimer.stop()
        self.screenAnimationTimer(True)
        self.labelusername.show()
        self.labellock.show()
        self.confirmButton.show()
        self.signupButton.show()
        self.usernameEdit.show()
        self.passwordEdit.show()
        self.cancelButton.hide()

    def closeItself(self, disconnect):
        if disconnect:
            self.s.close()
            QtCore.QCoreApplication.instance().quit()
            sys.exit()
        else:
            QtCore.QCoreApplication.instance().quit()
    
    def dynamicBackgroundColor(self):
        icolor = ""
        jcolor = ""
        
        if not self.ireverse:
            self.i += 5
        else:
            self.i -= 5

        if self.jreverse:
            self.j += 5
        else:
            self.j -= 5

        icolor = hex(self.i).lstrip("0x").rstrip("L")
        jcolor = hex(self.j).lstrip("0x").rstrip("L")
        if len(icolor) == 1:
            self.ioutputcolor = "#FF000" + icolor
        if len(icolor) == 2:
            self.ioutputcolor = "#FF00" + icolor
        if len(jcolor) == 1:
            self.joutputcolor =  "#0" + jcolor + "00FF"
        if len(jcolor) == 2:
            self.joutputcolor = "#" + jcolor + "00FF"

        self.backgroundColor.setStyleSheet("background: qlineargradient( x1:0 y1:0, x2:1 y2:1, stop:0" + self.ioutputcolor + ", stop:1 " + self.joutputcolor +")")
        if len(icolor) == 3:
            self.ireverse = True
        if len(icolor) == 0:
            self.ireverse = False
        if len(jcolor) == 3:
            self.jreverse = False
        if len(jcolor) == 0:
            self.jreverse = True

    def prompting(self, promptMessage):
        self.usernameEdit.clear()
        self.passwordEdit.clear()
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Error")
        msgbox.setText(promptMessage)
        msgbox.setIcon(QtWidgets.QMessageBox.Critical)
        msgbox.setStyleSheet("color: red; font-weight: bold; font: 16px")
        msgbox.setFont(QtGui.QFont("Times font", 20))
        msgbox.exec_()

    def update(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.dynamicBackgroundColor)
        self.timer.start(100)

        # update all info needed for connections
    def recvInfo(self, socket, headersize):
        self.s = socket
        self.HeaderSize = headersize

    def eventFromServer(self, shouldClose, shouldPrompt, promptMsg = ""):
        if shouldClose:
            self.closeItself(False)
        if shouldPrompt:
            self.prompting(promptMsg)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HeaderSize = 10
    app = QtWidgets.QApplication(sys.argv)
    lw = LoginWindow()
    lw.update()
    lw.recvInfo(s, HeaderSize)
    app.exec_()
