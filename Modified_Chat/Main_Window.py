import sys
import os
import socket

from PyQt5 import QtCore, QtGui, QtWidgets
import qtmodern.styles
import qtmodern.windows
MsgNameWin = []
MsgWinWidDict = {}
FriendCateNameLayout = {}
CateList = []
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(345, 810)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.statusBar().hide()
        self.setStyleSheet("background-color:white; border-radius:3px;" )

        self.borderShadow = QtWidgets.QWidget(self)
        self.borderShadow.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))
        self.borderShadow.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        
        self.centralwidget = QtWidgets.QWidget(self.borderShadow)
        self.centralwidget.setGeometry(self.borderShadow.x()+5, self.borderShadow.y()+5, 335, 800)

        eff = QtWidgets.QGraphicsDropShadowEffect()
        eff.setBlurRadius(11)
        eff.setOffset(0, 0)
        self.centralwidget.setGraphicsEffect(eff)

        # The background color of the window
        self.backgroundColor=QtWidgets.QLabel(self.centralwidget)
        self.backgroundColor.setGeometry(QtCore.QRect(0,0,self.centralwidget.width(),135))
        self.backgroundColor.setStyleSheet("background: qlineargradient(x1:0 y1:0, x2:1 y2:0, stop:0 #4C8BFF, stop:1 #20D1FE ); border-color:transparent; border-bottom-right-radius: 0px; border-bottom-left-radius:0px")
    
        # set the centralwidget on the window
        self.setCentralWidget(self.borderShadow)

        # Redesigned Close Button
        self.closebutton = QtWidgets.QPushButton(self.centralwidget)
        self.closebutton.setGeometry(self.centralwidget.width()-32, 0, 32, 32)
        self.closebutton.setObjectName("closebutton")
        self.closebutton.setStyleSheet("QPushButton:hover""{""background-color :#FF431B;""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.closebutton.clicked.connect(lambda: self.closewindow(True))

        # Redesigned Minimized Button
        self.minbutton = QtWidgets.QPushButton(self.centralwidget)
        self.minbutton.setGeometry(self.centralwidget.width()-64, 0, 32, 32)
        self.minbutton.setObjectName("minbutton")
        self.minbutton.setStyleSheet("QPushButton:hover""{""background-color :rgba(255, 255, 255, 50);""}" "QPushButton""{""color: white; font: 18px; background-color : transparent; border:none;""}")
        self.minbutton.clicked.connect(self.MinimizeWindow)

        # SearchBar
        self.searchBarWidget = QtWidgets.QWidget(self.centralwidget)
        self.searchBarWidget.setGeometry(0,self.backgroundColor.height()-30, self.centralwidget.width(), 30)
        self.searchBarWidget.setStyleSheet("QWidget{background-color: rgba(255, 255, 255, 50); border-radius:0px;}" )
        self.searchBarQHBox = QtWidgets.QHBoxLayout()
        self.searchBarQHBox.setSpacing(7)
        self.searchBarQHBox.setContentsMargins(12,0,12,0)

        self.searchBarIcon = QtWidgets.QLabel(self.centralwidget)
        self.searchBarIcon.setFixedSize(14,14)
        self.searchBarImage = QtGui.QImage(CURRENT_DIRECTORY + "/WidgetsIcons/" + "searchBar.png")
        self.searchBarIcon.setPixmap(QtGui.QPixmap.fromImage(self.searchBarImage))
        self.searchBarIcon.setScaledContents(True)
        self.searchBarIcon.setStyleSheet("background-color:transparent; border-radius:0px")

        self.searchBarCancel_Icon = QtWidgets.QPushButton(self.centralwidget)
        self.searchBarCancel_Icon.setFixedSize(16,16)
        self.searchBarCancel_Icon.setIcon(QtGui.QIcon(CURRENT_DIRECTORY + "/WidgetsIcons/" + "searchBar_close_button.png"))
        self.searchBarCancel_Icon.setStyleSheet("background-color:transparent; border-radius:0px")
        self.searchBarCancel_Icon.clicked.connect(self.searchBarCancelLink)
        self.searchBarCancel_Icon.hide()

        self.searchBar = QtWidgets.QLineEdit(self.centralwidget)
        self.searchBar.setObjectName("searchBar")
        self.searchBar.setFont(QtGui.QFont("Helvetica",9))
        self.searchBar.setPlaceholderText("搜索")
        self.searchBar.setToolTip("输入用户名、姓名/昵称查询联系人，\n还可以通过完整的用户名来查找陌生\n人")
        self.searchBar.setToolTipDuration(4000)
        self.searchBar.setStyleSheet("""QLineEdit{background-color: transparent; color:white;}""" """QToolTip { background-color: white; color: #575757; border-width: 1px; border-style:solid;  border-color:#7C7C7C; border-radius:0px}""")
        self.searchBar.setMaxLength(32)
        self.searchBar.installEventFilter(self)

        self.centralwidget.installEventFilter(self)

        self.searchBarQHBox.addWidget(self.searchBarIcon)
        self.searchBarQHBox.addWidget(self.searchBar)
        self.searchBarQHBox.addWidget(self.searchBarCancel_Icon)

        self.searchBarWidget.setLayout(self.searchBarQHBox)

        # Scroll Area Setup
        self.scrollarea1 = QtWidgets.QScrollArea()
        self.scrollarea2 = QtWidgets.QScrollArea()
        #self.scrollarea3 = QtWidgets.QScrollArea()
        self.scrollarea3 = SA()

        self.widget1 = QtWidgets.QWidget()
        self.widget2 = QtWidgets.QWidget()
        self.widget3 = QtWidgets.QWidget()

        self.vbox1 = QtWidgets.QVBoxLayout()
        self.vbox2 = QtWidgets.QVBoxLayout()
        self.vbox3 = QtWidgets.QVBoxLayout()
        self.vbox3.addStretch()

        self.widget1.setLayout(self.vbox1)
        
        self.widget2.setLayout(self.vbox2)
        self.widget3.setLayout(self.vbox3)

        self.scrollBar1 = QtWidgets.QScrollBar(QtCore.Qt.Vertical, self.scrollarea1)
        self.scrollBar2 = QtWidgets.QScrollBar(QtCore.Qt.Vertical, self.scrollarea2)
      

        self.scrollarea1.setVerticalScrollBar(self.scrollBar1)
        self.scrollarea2.setVerticalScrollBar(self.scrollBar2)

        self.scrollarea1.setWidget(self.widget1)
        self.scrollarea2.setWidget(self.widget2)
        self.scrollarea3.setWidget(self.widget3)

        self.scrollarea3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollarea3.setWidgetResizable(True)

    
        # Tabs
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setFont(QtGui.QFont("Arial", 11))
        self.tabs.setStyleSheet("QTabBar::tab {font-weight:450; height: 35px; width: 80 px; background: 'white'; color:#828282; margin-left:20; margin-right:10}" "QTabWidget::pane {background-color:white;border-style:solid; border-width:1px; border-color:#F0F0F0 white white white; background: white;}" "QTabBar::tab:selected {background-color: white;color:#26BDF6;border-style:solid; border-width:0px; border-color: #26BDF6;}")
        

        self.tab1_subWidget = QtWidgets.QWidget()
        self.tab1_subTab = QtWidgets.QTabWidget(self.tab1_subWidget)
        self.tab1_subTab.setFont(QtGui.QFont("Arial", 10))
        self.tab1_subTab.setStyleSheet("QTabBar::tab {font-weight:450; height: 28px; width: 65 px; background: transparent; color:#828282; margin-left:18px; margin-right:0px;margin-top:8; margin-bottom:0; border-radius:3px}" "QTabWidget::pane {background-color:transparent;border-width:0px; }" "QTabBar::tab:selected {background-color: #ECFAFF;color:#26BDF6;border-width:0px;}")
        
        self.tab1_subtab1_scrollarea = SA()
        self.tab1_subtab1_vbox = QtWidgets.QVBoxLayout()
        self.tab1_subtab1_vbox.addStretch()
        self.tab1_subtab1_vbox.setSpacing(0)
        self.tab1_subtab1_widget = QtWidgets.QWidget()
        self.tab1_subtab1_widget.setLayout(self.tab1_subtab1_vbox)
        self.tab1_subtab1_scrollarea.setWidget(self.tab1_subtab1_widget)
        self.tab1_subtab1_scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab1_subtab1_scrollarea.setWidgetResizable(True)
        self.tab1_subtab1_vbox.setAlignment(QtCore.Qt.AlignTop)
        
        self.tab1_subtab2_scrollarea = SA()
        self.tab1_subtab2_vbox = QtWidgets.QVBoxLayout()
        self.tab1_subtab2_vbox.addStretch()
        self.tab1_subtab2_widget = QtWidgets.QWidget()
        self.tab1_subtab2_widget.setLayout(self.tab1_subtab2_vbox)
        self.tab1_subtab2_scrollarea.setWidget(self.tab1_subtab2_widget)
        self.tab1_subtab2_scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tab1_subtab2_scrollarea.setWidgetResizable(True)
        
        self.tab1_subTab.addTab(self.tab1_subtab1_scrollarea, "好友")
        self.tab1_subTab.addTab(self.tab1_subtab2_scrollarea, "群聊")

        self.tabs.addTab(self.tab1_subWidget, "联系人")
        self.tabs.addTab(self.scrollarea2, "空间")
        self.tabs.addTab(self.scrollarea3, "消息")

        self.AppendFriendCategory("新朋友")
        self.AppendFriendCategory("我的设备")
        
        
        self.tabs.setGeometry(-10, self.backgroundColor.height(), self.centralwidget.width()+10,self.centralwidget.height()-self.backgroundColor.height())

        
        name = "精神病院"
        self.AppendMsgWidget(CURRENT_DIRECTORY+"/Images/"+"TestPic.jpg", name, "晕车:不奇怪啊 之前买显卡都送怪物猎人", True)

        hugo_name = "久"
        xc_name = "Numb，"

        self.AppendMsgWidget(CURRENT_DIRECTORY+"/Images/"+"Hugo_Head.jpg", hugo_name, "我是大逗比", True)
        self.AppendMsgWidget(CURRENT_DIRECTORY+"/Images/"+"XC_Head.jpg", xc_name, "我是大傻逼", False)

        self.generateSingleFriendWidget(CURRENT_DIRECTORY+"/Images/"+"Hugo_Head.jpg", hugo_name, "我是大逗比", True)
        self.generateSingleFriendWidget(CURRENT_DIRECTORY+"/Images/"+"XC_Head.jpg", xc_name, "我是大傻逼", False)


        # Call for retranslation
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # Variable to enable dragging window
        self.oldPos = self.pos()

        self.searchBarFocusOnTimer = QtCore.QTimer()

        #mw = qtmodern.windows.ModernWindow(self)
        #mw.show()
        self.show()


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.closebutton.setText(_translate("closebutton", u'\u2715'))
        self.minbutton.setText(_translate("minbutton", u'\u2015'))

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.globalPos().y() < self.pos().y() + self.backgroundColor.height():
            delta = QtCore.QPoint (event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()


    def insertFriendLayout(self, category_name):
        pass

    def generateSingleFriendWidget(self, path, friend_name, current_msg, isVIP):
        curhbox_widget = QtWidgets.QLabel()
        curhbox_widget.setFixedSize(self.centralwidget.width(),45)
        hbox = QtWidgets.QHBoxLayout()
        avatar = QtWidgets.QLabel()
        avatar.setFixedSize(30,30)
        imgdata = self.getLocalImgData(path)
        current_img_data = self.mask_image(imgdata, 128)
        avatar.setPixmap(current_img_data)
        avatar.setScaledContents(True)
        avatar.setStyleSheet("background-color:transparent;")
        friend_name_label = QtWidgets.QLabel()
        friend_name_label.setText(friend_name)
        friend_name_label.setFixedHeight(30)
        friend_name_label.adjustSize()
        friend_name_label.setFont(QtGui.QFont("Arial",10))
        friend_name_label.setStyleSheet("background-color:transparent;")
        fm = QtGui.QFontMetrics(QtGui.QFont("Arial",10))
        friend_name_label.setFixedWidth(int(fm.width(friend_name)))
        if isVIP:
            friend_name_label.setStyleSheet("color:red;background-color:transparent;")
        current_msg_label = QtWidgets.QLabel()
        current_msg_label.setText(current_msg)
        current_msg_label.setFixedHeight(30)
        current_msg_label.setAlignment(QtCore.Qt.AlignVCenter)
        current_msg_label.adjustSize()
        current_msg_label.setFont(QtGui.QFont("Arial",9))
        current_msg_label.setStyleSheet("color:#757575;background-color:transparent;")
        #hbox.setSpacing(7)
        hbox.addWidget(avatar)
        hbox.addWidget(friend_name_label)
        hbox.addWidget(current_msg_label)
        curhbox_widget.setLayout(hbox)
        #self.tab1_subtab1_vbox.insertWidget(self.tab1_subtab1_vbox.count()-1, curhbox_widget)
        curhbox_widget.setStyleSheet("QLabel:hover{background-color:#EBEBEB}")
        return curhbox_widget

    def appendFriendInToFriendLayout(self, path, category_name, friend_name, isVIP):
        category_layout_widget = QtWidgets.QWidget()
        category_layout = QtWidgets.QVBoxLayout()
        category_layout_widget.setLayout(category_layout)
        nameWidget = self.generateSingleFriendWidget(path, friend_name, "", isVIP)
        category_layout.addStretch()

        

    def AppendFriendCategory(self, name):
        nameWidget = QtWidgets.QLabel()
        nameHbox = QtWidgets.QHBoxLayout()
        nameWidget.setLayout(nameHbox)
        nameLabel = QtWidgets.QLabel()
        nameLabel.setText(name)
        nameLabel.setStyleSheet("background-color:transparent")
        nameLabel.setFont(QtGui.QFont("Times", 10))
        nameHbox.addWidget(nameLabel)
        nameWidget.setStyleSheet("QLabel:hover{background-color:#EBEBEB}" "QLabel{border-radius:0px}" )
        nameWidget.setFixedSize(self.centralwidget.width(), 38)
        self.tab1_subtab1_vbox.insertWidget(self.tab1_subtab1_vbox.count()-1, nameWidget)
        CateList.append(name)
        
        

    def AppendMsgWidget(self, path, name, msg, isVIP):
        keyToDel = None
        for key in MsgWinWidDict.keys():
            if MsgWinWidDict[key][0] == name:
                self.vbox3.removeWidget(key)
                keyToDel = key
        if keyToDel != None:
            del MsgWinWidDict[key]
        currentWidget = QtWidgets.QLabel()
        currentWidget.installEventFilter(self)
        currentWidget.setFixedSize(self.centralwidget.width(), 55)
        currentHBoxLayout = QtWidgets.QHBoxLayout()
        currentHBoxLayout.setAlignment(QtCore.Qt.AlignLeft)
        currentWidget.setLayout(currentHBoxLayout)

        imgdata = self.getLocalImgData(path)
        circularImgData = self.mask_image(imgdata, 128)
        circularAvatar = QtWidgets.QLabel()
        circularAvatar.setPixmap(circularImgData)
        circularAvatar.setScaledContents(True)
        circularAvatar.setStyleSheet("background-color:transparent;")
        circularAvatar.setFixedSize(40,40)
        currentVBoxLayout = QtWidgets.QVBoxLayout()
        NameLabel = QtWidgets.QLabel()
        NameLabel.setText(name)
        NameLabel.setFont(QtGui.QFont("Arial", 11))
        if isVIP:
            NameLabel.setStyleSheet("color:red; padding-top:2px;background-color:transparent")
        else:
            NameLabel.setStyleSheet("color:black; padding-top:2px;background-color:transparent")
        TextLabel = QtWidgets.QLabel()
        TextLabel.setText(msg)
        TextLabel.setFont(QtGui.QFont("Times", 9))
        TextLabel.setStyleSheet("color:#757575; padding-left:3px; padding-bottom:3px; background-color:transparent")
        currentVBoxLayout.addWidget(NameLabel)
        currentVBoxLayout.addWidget(TextLabel)
        currentVBoxLayout.setSpacing(0)
        currentHBoxLayout.addWidget(circularAvatar)
        currentHBoxLayout.addLayout(currentVBoxLayout)
        currentHBoxLayout.setSpacing(7)
        self.vbox3.insertWidget(self.vbox3.count()-1, currentWidget)
        self.vbox3.setSpacing(0)
        currentWidget.setStyleSheet("QLabel:hover{background-color: #EBEBEB}" )


        MsgWindow = QtWidgets.QMainWindow()
        MsgWindow.setWindowTitle(name)

        MsgNameWin.append(name)
        MsgNameWin.append(MsgWindow)
        MsgWinWidDict[currentWidget] = MsgNameWin
        

    def eventFilter(self, obj, event):
        if obj == self.searchBar and event.type() == QtCore.QEvent.MouseButtonPress:
            self.searchBarShowUp()

        if obj != self.searchBar and self.searchBar.text() == "" and event.type() == QtCore.QEvent.MouseButtonPress:
            self.searchBarCancel()

        if obj != self.searchBar and self.searchBar.text() != "" and event.type() == QtCore.QEvent.MouseButtonPress:
            self.searchBar.selectAll()

        if obj == self.searchBar and event.type() == QtCore.QEvent.FocusIn:
            self.searchBarFocusOnTimerFunc()

        if obj == self.searchBar and event.type() == QtCore.QEvent.FocusOut:
            self.searchBarFocusOnTimer.stop()

        if obj in MsgWinWidDict.keys() and event.type() == QtCore.QEvent.MouseButtonPress:
            for others in MsgWinWidDict:
                others.setStyleSheet("QLabel:hover{background-color: #EBEBEB}")
            obj.setStyleSheet("background-color: #EBEBEB")
        if obj in MsgWinWidDict and event.type() == QtCore.QEvent.MouseButtonDblClick:
            MsgWinWidDict[obj][1].show()

        return False

    def searchBarShowUp(self):
        self.searchBarWidget.setStyleSheet("background-color:white;border-radius:0px;")
        self.searchBar.setStyleSheet("""QLineEdit{ color:black;}""" """QToolTip { background-color: white; color: #575757; border-width: 1px; border-style:solid;  border-color:#7C7C7C; border-radius:0px}""")
        self.searchBar.setPlaceholderText("")
        self.searchBarCancel_Icon.show()

    def searchBarCancel(self):
        self.searchBarWidget.setStyleSheet("QWidget{background-color: rgba(255, 255, 255, 50); border-radius:0px;}" )
        self.searchBar.setStyleSheet("""QLineEdit{background-color: transparent; color:white;}""" """QToolTip { background-color: white; color: #575757; border-width: 1px; border-style:solid;  border-color:#7C7C7C; border-radius:0px}""")
        self.searchBar.setPlaceholderText("搜索")
        self.searchBar.clear()
        self.searchBarCancel_Icon.hide()

    def searchBarFocusOnTimerFunc(self):
        self.searchBarFocusOnTimer.timeout.connect(self.checkIfQLineEditEmpty)
        self.searchBarFocusOnTimer.start(100)

    def checkIfQLineEditEmpty(self):
        if self.searchBar.text() != "":
            self.searchBarShowUp()


    def searchBarCancelLink(self):
        self.searchBarCancel()
        self.searchBar.clearFocus()

    def MinimizeWindow(self):
        self.showMinimized()

     # Close the window
    def closewindow(self, disconnect):
        if disconnect:
            self.s.close()
        QtCore.QCoreApplication.instance().quit()

    

    def recvInfo(self, socket, headersize):
        self.s = socket
        self.HeaderSize = headersize


    def getLocalImgData(self, path):
        imgdata = open(path, 'rb').read()
        return imgdata


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

class SA(QtWidgets.QScrollArea):
    def __init__(self):
        super().__init__()

        self.scrollBar3 = QtWidgets.QScrollBar(QtCore.Qt.Vertical, self)
        self.scrollBar3.hide()
        self.scrollBar3.setStyleSheet( """QScrollBar::vertical{border-color: transparent;border-width: 1px;border-style: outset;background-color: transparent;width: 8px;}""" """QScrollBar::handle:vertical {background-color:#D7D7D7 ; border-style:outset; border-radius:3px;}""" """QScrollBar::handle:hover {background-color:#B7B7B7 ;}""" """QScrollBar::add-line:vertical { height: 0px;}""" """QScrollBar::sub-line:vertical { height: 0px;}""")
        self.setVerticalScrollBar(self.scrollBar3)
    def enterEvent(self, event):
        self.scrollBar3.show()
        
    def leaveEvent(self, event):
        self.scrollBar3.hide()

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HeaderSize = 10
    app = QtWidgets.QApplication(sys.argv)
    #qtmodern.styles.dark(app)

    mw = MainWindow()
    mw.recvInfo(s, HeaderSize)
    app.exec_()