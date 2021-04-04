
import sys
import configparser
import requests
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPlainTextEdit,QLabel
from functools import partial
from firstScreen import Ui_introscreen
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget




class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.open_windows = []
        self.user = "postgres"
        self.password = "password"
        self.host = "127.0.0.1"
        self.port = "5432"
        self.db = "TPC-H"
        
    def updateDBconnection(self):
        print("")
        
    def setupUi(self, widget):
        self.setObjectName("MainWindow")
        screen_width = (self.available_width -
                        60) if self.available_width < 1200 else 1200
        screen_height = (self.available_height -
                         60) if self.available_height < 716 else 716
        self.resize(screen_width, screen_height)

        self.centralwidget = QtWidgets.QStackedWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.addWidget(widget)
        self.centralwidget.setCurrentWidget(widget)

        

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Query visualizer ", "Query visualizer"))

    
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.available_width = app.desktop().availableGeometry().width()
    ui.available_height = app.desktop().availableGeometry().height()
    
    intro_screen = Ui_introscreen()
    intro_screen.window = ui
    intro_screen.setupUi()

    ui.setupUi(intro_screen)

    ui.setGeometry(
        QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight,
            QtCore.Qt.AlignCenter,
            ui.size(),
            app.desktop().availableGeometry()
        )   
    )

    ui.showMaximized()

    sys.exit(app.exec_())