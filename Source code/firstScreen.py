import configparser
import ast
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPlainTextEdit,QLabel
import psycopg2
from pyqtgraph.flowchart import Flowchart, Node
import numpy as np
import pyqtgraph.flowchart.library as fclib
from node_editor_wnd import NodeEditorWnd
from node_scene import Scene
from node_node import Node
from node_graphics_view import QDMGraphicsView
import json
import pprint
import itertools
import copy
from functools import partial
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget
from PyQt5.QtWidgets import QPlainTextEdit,QLabel, QMessageBox
import sys

class ImageViewNode(Node):
    """Node that displays image data in an ImageView widget"""
    nodeName = 'ImageView'
    
    def __init__(self, name):
        self.view = None
        ## Initialize node with only a single input terminal
        Node.__init__(self, name, terminals={'data': {'io':'in'}})
        
    def setView(self, view):  ## setView must be called by the program
        self.view = view
        
    def process(self, data, display=True):
        ## if process is called with display=False, then the flowchart is being operated
        ## in batch processing mode, so we should skip displaying to improve performance.
        
        if display and self.view is not None:
            ## the 'data' argument is the value given to the 'data' terminal
            if data is None:
                self.view.setImage(np.zeros((1,1))) # give a blank array to clear the view
            else:
                self.view.setImage(data)



class Ui_introscreen(QtWidgets.QWidget):
    def __init__(self, window=None):
        QtWidgets.QWidget.__init__(self)
        self.window = window
        self.user = "postgres"
        self.password = "password"
        self.host = "127.0.0.1"
        self.port = "5432"
        self.db = "TPC-H"

    def updateDBconnection(self,user,password,host,port,db):
        print("change")
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db

    def setupUi(self):
        self.setObjectName("introscreen")
        screen_width = (self.window.available_width -
                        50) if self.window.available_width < 700 else 700
        screen_height = (self.window.available_height -
                         50) if self.window.available_height < 700 else 700
        self.resize(screen_width, screen_height)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")

        filemenu = self.menubar.addMenu("&Setting")

        new_action = QtWidgets.QAction('&Connection', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Change database connection settings')
        new_action.triggered.connect(partial(self.start_new))
        filemenu.addAction(new_action)


        # helpbar = self.menubar.addMenu('Help')
        # shortcut_action = QtWidgets.QAction('Shortcut Keys', self)
        # shortcut_action.setShortcut('?')
        # shortcut_action.setStatusTip('Display various shortcut keys')
        # helpbar.addAction(shortcut_action)

        # about_action = QtWidgets.QAction('About', self)
        # about_action.setStatusTip('About the application')
        # helpbar.addAction(about_action)

        self.window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.window.setStatusBar(self.statusbar)
        self.parent_hboxLayout = QtWidgets.QHBoxLayout(self)
        self.parent_hboxLayout.setObjectName('parentlayout')
        self.parent_hboxLayout.insertStretch(0, 10)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.textlayout = QtWidgets.QHBoxLayout()
        self.textlayout.setObjectName("textlayout")
        self.textview = QLabel (self)
        self.textview.setFixedSize(100, 40)
        self.textview.setText("Enter your query here : ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textview.sizePolicy().hasHeightForWidth())
        self.textlayout.addWidget(self.textview)
        self.verticalLayout.addLayout(self.textlayout)

        
        # text box for query
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,280)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textbox.sizePolicy().hasHeightForWidth())
        self.textbox.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(self.textbox)
        
          # text box for reason
        self.reason = QtGui.QTextEdit(self)
        self.reason.setReadOnly(True)
        self.reason.move(20, 20)
        self.reason.resize(280,280)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.reason.sizePolicy().hasHeightForWidth())
        self.reason.setSizePolicy(sizePolicy)
        self.reason.setLineWrapMode(QtGui.QTextEdit.LineWrapMode.NoWrap);
        self.verticalLayout.addWidget(self.reason)

        self.buttonlayout = QtWidgets.QHBoxLayout()
        self.buttonlayout.setObjectName("buttonlayout")

        self.query = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.query.sizePolicy().hasHeightForWidth())
        self.query.setSizePolicy(sizePolicy)
        self.query.setObjectName("Query plan")
        self.buttonlayout.addWidget(self.query)
        
        # self.last_button = QtWidgets.QPushButton(self)
        # sizePolicy = QtWidgets.QSizePolicy(
        #     QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(
        #     self.last_button.sizePolicy().hasHeightForWidth())
        # self.last_button.setSizePolicy(sizePolicy)
        # self.last_button.setObjectName("last_button")
        # self.buttonlayout.addWidget(self.last_button)

        # self.load_button = QtWidgets.QPushButton(self)
        # sizePolicy = QtWidgets.QSizePolicy(
        #     QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(
        #     self.load_button.sizePolicy().hasHeightForWidth())
        # self.load_button.setSizePolicy(sizePolicy)
        # self.load_button.setObjectName("load_button")
        # self.buttonlayout.addWidget(self.load_button)

        # self.audio_button = QtWidgets.QPushButton(self)
        # sizePolicy = QtWidgets.QSizePolicy(
        #     QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(
        #     self.audio_button.sizePolicy().hasHeightForWidth())
        # self.audio_button.setSizePolicy(sizePolicy)
        # self.audio_button.setObjectName("audio_button")
        # self.buttonlayout.addWidget(self.audio_button)

        # self.restore_button = QtWidgets.QPushButton(self)
        # sizePolicy = QtWidgets.QSizePolicy(
        #     QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(
        #     self.restore_button.sizePolicy().hasHeightForWidth())
        # self.restore_button.setSizePolicy(sizePolicy)
        # self.restore_button.setObjectName("restore_button")
        # self.buttonlayout.addWidget(self.restore_button)

        self.verticalLayout.addLayout(self.buttonlayout)

        self.parent_hboxLayout.addLayout(self.verticalLayout,1200)
        
        self.verticalLayoutRight = QtWidgets.QVBoxLayout()
        self.verticalLayoutRight.setObjectName("verticalLayoutRight")
       
        
        self.textview2 = QLabel (self)
        self.textview2.setFixedSize(100, 40)
        self.textview2.setText("List of plans")
        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.move(50, 250)
        
        self.hlayout = QtWidgets.QHBoxLayout()
        self.hlayout.setObjectName("combobox")
        
        self.hlayout.addWidget(self.textview2)
        self.hlayout.addWidget(self.comboBox)
        
        #self.verticalLayoutRight.addWidget(self.textview2)
        self.verticalLayoutRight.addLayout(self.hlayout)

        self.wnd = NodeEditorWnd()
        self.verticalLayoutRight.addWidget(self.wnd)  
        
        self.parent_hboxLayout.addLayout(self.verticalLayoutRight,2000)

        

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.query.clicked.connect(self.query_handler)
        self.comboBox.currentIndexChanged.connect(self.changePlan)

        # self.last_button.clicked.connect(self.last_button_handler)
        # self.load_button.clicked.connect(self.load_button_handler)
        # self.audio_button.clicked.connect(self.audio_button_handler)
        # self.restore_button.clicked.connect(self.restore_button_handler)
    
    def start_new(self):
        self.exPopup = WinTable(self)
        self.exPopup.show()
        self.exPopup.setupUi(self.exPopup)
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("introscreen", "Form"))
        self.query.setText(_translate("introscreen", "Query Plan"))
        # self.last_button.setText(_translate("introscreen", "Last"))
        # self.load_button.setText(_translate("introscreen", "Load"))
        # self.audio_button.setText(_translate("introscreen", "File Mode"))
        # self.restore_button.setText(_translate(
        #     "introscreen", "Transcription Mode"))
        
    def changePlan(self):
        planNumber = self.comboBox.currentIndex() 
        if planNumber == -1:
            return
        self.wnd.changePlan(planNumber)
        
    def queryPlan(self,query):
        #query = "select l_orderkey, sum(l_extendedprice * (1 - l_discount)) as revenue, o_orderdate,o_shippriority from customer, orders, lineitem where c_mktsegment = 'BUILDING' and c_custkey = o_custkey and l_orderkey = o_orderkey group by l_orderkey, o_orderdate, o_shippriority order by revenue desc, o_orderdate "
        #query = "select l_returnflag, l_linestatus, sum(l_quantity) as sum_qty, sum(l_extendedprice) as sum_base_price, sum(l_extendedprice * (1 - l_discount)) as sum_disc_price, sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge, avg(l_quantity) as avg_qty, avg(l_extendedprice) as avg_price, avg(l_discount) as avg_disc, count(*) as count_order from lineitem where l_extendedprice >0 group by l_returnflag, l_linestatus order by l_returnflag, l_linestatus"
        #query = "select p_brand, p_type, p_retailprice, count(distinct ps_suppkey) as supplier_cnt from partsupp, part where p_partkey = ps_partkey and p_retailprice >0 and ps_suppkey in ( select s_suppkey from supplier where s_acctbal >0 ) group by p_brand, p_type, p_retailprice order by supplier_cnt desc, p_brand, p_type, p_retailprice"
        #query = "select c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity) from customer, orders, lineitem where o_orderkey in ( select l_orderkey from lineitem where l_extendedprice >0 group by l_orderkey having sum(l_quantity) > 300 ) and c_custkey = o_custkey and o_orderkey = l_orderkey and c_acctbal >0 group by c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice order by o_totalprice desc, o_orderdate"
        config = self.listOfConfig()
        planList = []
        errormessage = ""
        for setting in config:
            try:
                connection = psycopg2.connect(user = self.user,
                                              password = self.password,
                                              host = self.host,
                                              port = self.port,
                                              database = self.db)
                cursor = connection.cursor()
                # Print PostgreSQL Connection properties
                print ( connection.get_dsn_parameters(),"\n")
                # Print PostgreSQL version
                cursor.execute( setting + " set enable_bitmapscan = false; EXPLAIN (FORMAT JSON) "  + query)
                plan = cursor.fetchall() 
                result = []
                for row in plan:
                    result.append(row[0])
                json_output = json.dumps(result[0][0])
                jsonObject = json.loads(json_output)
                planList.append(jsonObject)

            except (Exception, psycopg2.Error) as error :
                print ("Error while connecting to PostgreSQL", error)
                errormessage = error
                connection=False
                break
            finally:
                #closing database connection.
                    if(connection):
                        cursor.close()
                        connection.close()
                        #print("PostgreSQL connection is closed")
                
        if(connection):
            temp = copy.deepcopy(planList)
            for pl in planList:         
                if "Plans" in pl["Plan"]:
                    self.removeItems(pl["Plan"]["Plans"])
                self.removeroot(pl["Plan"])
                
            uplanList = []
            upIndex = []
            index = 0
            for x in planList:
                if x not in uplanList:
                    uplanList.append(x)
                    upIndex.append(index)
                index += 1
                
            unqiuePlanList = []
            for ip in upIndex:
                unqiuePlanList.append(temp[ip])
            
            self.comboBox.clear()
            self.wnd.clearData()
            self.wnd.buildPlan(unqiuePlanList,self.comboBox)
            self.wnd.addTable(self.reason)
        else:
            self.reason.setText(str(errormessage))
    def query_handler(self):
        if(self.textbox.toPlainText() == ""):
            self.open_dialog()       
        else:
            self.queryPlan(self.textbox.toPlainText())
        return
    
    def open_dialog(self):
        msg = QMessageBox()        
        msg.setWindowTitle("Error")
        msg.setText("Please input a query")
        msg.setIcon(QMessageBox.Information)
        msg.exec_() 
        return
    def load_button_handler(self):
        return
    def last_button_handler(self):
        return

    def restore_button_handler(self):
        return

    def validate_configurationfile(self, filename=None):
        return

    def audio_button_handler(self):
        return
    
    def listOfConfig(self):
        settings1 = []
        settings1.append("set enable_hashjoin ")
        settings1.append("set enable_mergejoin ")
        settings1.append("set enable_nestloop ")
        
        settings2 = []
        settings2.append("set enable_indexscan ")
        settings2.append("set enable_seqscan ")
        
        settings3 = []
        #settings3.append("set enable_sort ")
        lst3 = list(itertools.product([False, True], repeat=3))
        lst3 = lst3[1:-1]
        lst2 = list(itertools.product([False, True], repeat=2))
        lst2 = lst2[1:-1]
        lst1 = list(itertools.product([False, True], repeat=1))
        
        configList = []
        for slist3 in lst3:
            configQuery = ""
            for i in range(len(slist3)):
                if(not slist3[i]):
                    configQuery = configQuery +  str(settings1[i]) + " = false; "
            configList.append(configQuery)
                
        configList2 = []   
        for slist2 in lst2:
            configQuery = ""
            for i in range(len(slist2)):
                if(not slist2[i]):
                    configQuery = configQuery +  str(settings2[i]) + " = false; " 
            for c in configList:  
                configList2.append(c+configQuery)     
        
        # configList3 = []   
        # configList4 = ["set enable_sort  = false;"]
        # for slist1 in lst1:
        #     configQuery = ""
        #     for i in range(len(slist1)):
        #         if(not slist1[i]):
        #             configQuery = configQuery +  str(settings3[i]) + " = false; " 
        #     for c in configList:  
        #         configList3.append(c+configQuery)  
        
        configList5 =  configList2 +  configList
        configList6 = [] 
        for i in configList5: 
            if i not in configList6: 
                configList6.append(i) 
        configList6.insert(0,"")
        return configList6
    
    def removeItems(self,node):
        for item in node:
            if 'Parent Relationship' in item:
                del item['Parent Relationship']   
            if 'Parallel Aware' in item:
                del item['Parallel Aware']   
            if 'Index Name' in item:
                del item['Index Name'] 
            if 'Alias' in item:
                del item['Alias'] 
            if 'Scan Direction' in item:
                del item['Scan Direction'] 
            if 'Plan Width' in item:
                del item['Plan Width'] 
            if 'Index Cond' in item:
                del item['Index Cond'] 
            if 'Strategy' in item:
                del item['Strategy']  
            if 'Group Key' in item:
                del item['Group Key']     
            if 'Partial Mode' in item:
                del item['Partial Mode']  
            if 'Inner Unique' in item:
                del item['Inner Unique']  
            if 'Join Type' in item:
                del item['Join Type']  
            if 'Presorted Key' in item:
                del item['Presorted Key']  
            if 'Sort Key' in item:
                del item['Sort Key']     
            if 'Total Cost' in item:
                del item['Total Cost']
            if 'Startup Cost' in item:
                del item['Startup Cost']
            if 'Workers Planned' in item:
                del item['Workers Planned']
            if 'Plan Rows' in item:
                del item['Plan Rows']
            if 'Filter' in item:
                del item['Filter']
                
            if "Plans" in item:
                self.removeItems(item["Plans"])
       
    def removeroot(self,item):
        if 'Parent Relationship' in item:
            del item['Parent Relationship']   
        if 'Parallel Aware' in item:
            del item['Parallel Aware']   
        if 'Index Name' in item:
            del item['Index Name'] 
        if 'Alias' in item:
            del item['Alias'] 
        if 'Scan Direction' in item:
            del item['Scan Direction'] 
        if 'Plan Width' in item:
            del item['Plan Width'] 
        if 'Index Cond' in item:
            del item['Index Cond'] 
        if 'Strategy' in item:
            del item['Strategy']  
        if 'Group Key' in item:
            del item['Group Key']     
        if 'Partial Mode' in item:
            del item['Partial Mode']  
        if 'Inner Unique' in item:
            del item['Inner Unique']  
        if 'Join Type' in item:
            del item['Join Type']  
        if 'Presorted Key' in item:
            del item['Presorted Key']  
        if 'Sort Key' in item:
            del item['Sort Key']     
        # if 'Total Cost' in item:
        #     del item['Total Cost']
        if 'Startup Cost' in item:
            del item['Startup Cost']
        if 'Workers Planned' in item:
            del item['Workers Planned']
        if 'Plan Rows' in item:
            del item['Plan Rows']
        if 'Filter' in item:
            del item['Filter']
            
class WinTable(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.password = ""
        self.port = ""
        self.db = ""
        self.host = ""
        
    def setupUi(self, MainWindow):
            MainWindow.setObjectName("Change database connection ")
            MainWindow.resize(384, 269)
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.formLayoutWidget.setGeometry(QtCore.QRect(20, 10, 331, 211))
            self.formLayoutWidget.setObjectName("formLayoutWidget")
            self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
            self.formLayout.setContentsMargins(0, 0, 0, 0)
            self.formLayout.setObjectName("formLayout")
            self.label = QtWidgets.QLabel(self.formLayoutWidget)
            self.label.setObjectName("label")
            self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
            self.textEdit_9 = QtWidgets.QTextEdit(self.formLayoutWidget)
            self.textEdit_9.setObjectName("textEdit_9")
            self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.textEdit_9)
            self.label_9 = QtWidgets.QLabel(self.formLayoutWidget)
            self.label_9.setObjectName("label_9")
            self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_9)
            self.textEdit_4 = QtWidgets.QTextEdit(self.formLayoutWidget)
            self.textEdit_4.setObjectName("textEdit_4")
            self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.textEdit_4)
            self.label_10 = QtWidgets.QLabel(self.formLayoutWidget)
            self.label_10.setObjectName("label_10")
            self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_10)
            self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
            self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
            self.lineEdit.setObjectName("lineEdit")
            self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
            self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
            self.label_4.setObjectName("label_4")
            self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
            self.textEdit_11 = QtWidgets.QTextEdit(self.formLayoutWidget)
            self.textEdit_11.setObjectName("textEdit_11")
            self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.textEdit_11)
            self.label_8 = QtWidgets.QLabel(self.formLayoutWidget)
            self.label_8.setObjectName("label_8")
            self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_8)
            self.textEdit_10 = QtWidgets.QTextEdit(self.formLayoutWidget)
            self.textEdit_10.setObjectName("textEdit_10")
            self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.textEdit_10)
            self.horizontalLayout = QtWidgets.QHBoxLayout()
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.pushButton = QtWidgets.QPushButton(self.formLayoutWidget)
            self.pushButton.setObjectName("pushButton")
            self.horizontalLayout.addWidget(self.pushButton)
            self.pushButton_2 = QtWidgets.QPushButton(self.formLayoutWidget)
            self.pushButton_2.setObjectName("pushButton_2")
            self.horizontalLayout.addWidget(self.pushButton_2)
            self.formLayout.setLayout(5, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 384, 26))
            self.menubar.setObjectName("menubar")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            self.pushButton.clicked.connect(self.pushButton_click)
            self.pushButton_2.clicked.connect(self.pushButton_2_click)
            MainWindow.setStatusBar(self.statusbar)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)
            
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Host :"))
        self.label_9.setText(_translate("MainWindow", "User :"))
        self.label_10.setText(_translate("MainWindow", "Password :"))
        self.label_4.setText(_translate("MainWindow", "Database :"))
        self.label_8.setText(_translate("MainWindow", "Port :"))
        self.pushButton.setText(_translate("MainWindow", "Save"))
        self.pushButton_2.setText(_translate("MainWindow", "Cancel"))
        
        
        self.textEdit_9.setText(self.parent.host)
        self.textEdit_11.setText(self.parent.db)
        self.lineEdit.setText(self.parent.password)
        self.textEdit_4.setText(self.parent.user)
        self.textEdit_10.setText(self.parent.port)
        
    def pushButton_2_click(self):
        
        
        self.close() 
        
    def pushButton_click(self):
        self.parent.updateDBconnection(self.textEdit_4.toPlainText(),self.lineEdit.text(),
                                       self.textEdit_9.toPlainText(),self.textEdit_10.toPlainText(), 
                                       self.textEdit_11.toPlainText())
        self.textEdit_9.setText(self.parent.host)
        self.textEdit_11.setText(self.parent.db)
        self.lineEdit.setText(self.parent.password)
        self.textEdit_4.setText(self.parent.user)
        self.textEdit_10.setText(self.parent.port)
        

        
        self.close() 
          
    def center(self):
       # geometry of the main window
       qr = self.frameGeometry()

       # center point of screen
       cp = QDesktopWidget().availableGeometry().center()

       # move rectangle's center point to screen's center point
       qr.moveCenter(cp)

       # top left of rectangle becomes top left of window centering it
       self.move(qr.topLeft())