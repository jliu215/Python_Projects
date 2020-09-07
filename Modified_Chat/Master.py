import Login_Window
import threading
import sys
from PyQt5 import QtWidgets
import socket

HeaderSize = 10

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app = QtWidgets.QApplication(sys.argv)
    lw = Login_Window.LoginWindow()
    lw.update()
    lw.recvInfo(s, HeaderSize)
    app.exec_()