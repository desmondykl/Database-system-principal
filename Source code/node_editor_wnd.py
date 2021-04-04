from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
 
from node_scene import Scene
from node_node import Node
from node_edge import Edge, EDGE_TYPE_BEZIER
from node_graphics_view import QDMGraphicsView

class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stylesheet_filename = 'nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)
        self.col = 0
        self.maxvalue = 0
        self.preNodeList = []
        self.preNodeListDict = {}
        self.curNodeList = []
        self.counter = 0
        self.tableNumber = 0
        self.NodeDict = {}
        self.AllNodeDict = {}
        self.BestPlanNode = []
        self.initUI()
        
        
        
    def clearData(self):
        self.col = 0
        self.preNodeList = []
        self.curNodeList = []
        self.preNodeListDict = {}
        self.counter = 0
        self.tableNumber = 0
        self.NodeDict = {}
        self.AllNodeDict = {}
        self.BestPlanNode = []
        self.scene.clearData()
        
    def trytest(self, node,col):
        col = col + 1
        for item in node:
            if "Plans" in item:
                self.trytest(item["Plans"],col)                
            
        print("=========================")
        row = 0
        self.curNodeList = []
        for item in reversed(node):
            print(item["Node Type"] + str(col))
            
    def getMaxTable(self, ListTable):
        for t in ListTable:
            try:
                i = int(t[-1])
                if(self.tableNumber<i):
                    self.tableNumber = i
            except:
                continue
        return self.tableNumber
    
    def traverseNew(self, node,col,rowTest):
        col = col + 1
        temp= 0
        for item in node:
            print(item["Node Type"] +"\t\t\t Row:"+str(rowTest)+" Col:"+str(col))
            tempNode = item.copy()
            #if 'Plans' in tempNode:
                #del tempNode['Plans']
            self.NodeDict[(rowTest,col)] = tempNode

            if "Plans" in item:
                temp = self.traverseNew(item["Plans"],col,rowTest)
            if(temp>rowTest):
                rowTest = temp
            else:
                rowTest =  rowTest + 1
        return  rowTest 
            
        
    def traverse(self, node,col,rowTest):
        col = col + 1
        preRow = 0
        for item in node:
            if "Plans" in item:
                rowTest = self.traverse(item["Plans"],col,rowTest)
            if(len(self.curNodeList)!=0):
                self.preNodeListDict[preRow] = self.curNodeList.copy()
            rowTest = rowTest + 1
            preRow = preRow + 1

            
        if(self.maxvalue<col):
            self.maxvalue=col

        row = 0
        self.curNodeList = []
        reversedcounter = len(node)-1
        notsure = 0
        for item in reversed(node):
            print(item["Node Type"] + " " + str(rowTest-notsure)+ " " + str(col))
            print("=============")
            
            inputs = 0

            if "Plans" in item:
                inputs = len(item["Plans"])
            y = (rowTest-notsure)*170
            notsure +=1
            if inputs == 1:
                node1 = Node(self.scene, item["Node Type"], inputs=[1], outputs=[1])
                node1.setPos(-350+(-(col-self.maxvalue)*250), y)
                if len(self.preNodeList) != 0:
                    #edge1 = Edge(self.scene, self.preNodeList[0].outputs[0], node1.inputs[0], edge_type=EDGE_TYPE_BEZIER)
                    edge1 = Edge(self.scene, self.preNodeListDict[reversedcounter][0].outputs[0], node1.inputs[0], edge_type=EDGE_TYPE_BEZIER)
            elif inputs == 0 :
                node1 = Node(self.scene, item["Node Type"], inputs=[], outputs=[1])
                if len(self.preNodeListDict)>0  and row==0 and len(self.preNodeListDict[0])==2:
                    node1.setPos(-350+(-(col-self.maxvalue)*250),  y)
                else:
                    node1.setPos(-350+(-(col-self.maxvalue)*250),  y)
                if(len(node)==1):
                    self.counter = self.counter-1
            elif inputs == 3 :
                if(len(node)==1):
                    self.counter = self.counter+1
                node1 = Node(self.scene, item["Node Type"], inputs=[1,1,1], outputs=[1])
                node1.setPos(-350+(-(col-self.maxvalue)*250),  y)
                if len(self.preNodeList) != 0:
                    edge1 = Edge(self.scene, self.preNodeListDict[reversedcounter][0].outputs[0], node1.inputs[2], edge_type=EDGE_TYPE_BEZIER)
                    edge1 = Edge(self.scene, self.preNodeListDict[reversedcounter][1].outputs[0], node1.inputs[1], edge_type=EDGE_TYPE_BEZIER)
                    edge1 = Edge(self.scene, self.preNodeListDict[reversedcounter][2].outputs[0], node1.inputs[0], edge_type=EDGE_TYPE_BEZIER)
            else:
                if(len(node)==1):
                    self.counter = self.counter+1
                node1 = Node(self.scene, item["Node Type"], inputs=[1,1], outputs=[1])
                node1.setPos(-350+(-(col-self.maxvalue)*250),   y)
                if len(self.preNodeList) != 0:
                    edge1 = Edge(self.scene, self.preNodeListDict[reversedcounter][0].outputs[0], node1.inputs[1], edge_type=EDGE_TYPE_BEZIER)
                    edge1 = Edge(self.scene, self.preNodeListDict[reversedcounter][1].outputs[0], node1.inputs[0], edge_type=EDGE_TYPE_BEZIER)

                    #edge1 = Edge(self.scene, self.preNodeList[0].outputs[0], node1.inputs[1], edge_type=EDGE_TYPE_BEZIER)
                    #edge1 = Edge(self.scene, self.preNodeList[1].outputs[0], node1.inputs[0], edge_type=EDGE_TYPE_BEZIER)
            
            text = ""
            if(item["Node Type"]=="Seq Scan"):
                table = ""
                if reversedcounter in self.preNodeListDict:
                    for pNode in self.preNodeListDict[reversedcounter]:
                        if pNode.intermediateTable != '':
                            table = (pNode.intermediateTable)
                            break
                relationname = item["Relation Name"]
                text = "Perform sequential scan on "+relationname+""
                if "Filter" in item:
                    self.tableNumber = self.tableNumber +1
                    if( table ==""):
                        
                        text = text + " as table T"+str(self.tableNumber)
                        node1.intermediateTable = "table T"+str(self.tableNumber)
                        
                    else:
                        text = text + " as table T" +str(self.tableNumber)
                        node1.intermediateTable = "table T" +str(self.tableNumber)
                else:
                    node1.intermediateTable = relationname
            elif(item["Node Type"]=="Index Only Scan"):
                relationname = item["Relation Name"]
                text = "Perform Index Only Scan on "+relationname+""
                table = ""
                if reversedcounter in self.preNodeListDict:
                    for pNode in self.preNodeListDict[reversedcounter]:
                        if pNode.intermediateTable != '':
                            table = (pNode.intermediateTable)
                            break
                node1.intermediateTable = relationname
                
            elif(item["Node Type"]=="Index Scan"):
                relationname = item["Relation Name"]
                text = "Perform Index Scan on "+relationname+""
                table = ""
                if reversedcounter in self.preNodeListDict:
                    for pNode in self.preNodeListDict[reversedcounter]:
                        if pNode.intermediateTable != '':
                            table = (pNode.intermediateTable)
                            break
                if "Filter" in item:
                    self.tableNumber = self.tableNumber +1
                    if( table ==""):
                        
                        text = text + " as table T"+str(self.tableNumber)
                        node1.intermediateTable = "table T"+str(self.tableNumber)
                        
                    else:
                        text = text + " as table T" +str(self.tableNumber)
                        node1.intermediateTable = "table T" +str(self.tableNumber)
                else:
                    node1.intermediateTable = relationname
            elif(item["Node Type"]=="Hash"):
                text="Hash " + self.preNodeListDict[reversedcounter][0].intermediateTable
                node1.intermediateTable = self.preNodeListDict[reversedcounter][0].intermediateTable
                self.getMaxTable([self.preNodeListDict[reversedcounter][0].intermediateTable])
                
            elif(item["Node Type"]=="Hash Join"):
                # interTableList = []
                # for pNode in self.preNodeList:
                #     if pNode.intermediateTable != '':
                #         interTableList.append(pNode.intermediateTable)
                hashcondition  =  item["Hash Cond"]
                Listcondition = hashcondition.split("=")
                tablesList = []
                for n in self.preNodeListDict[reversedcounter]:
                    if n.intermediateTable != '' :
                        tablesList.append(n.intermediateTable)
                    
                for con in Listcondition:
                    table = con.split(".")[0]
                    tablesList.append(table)
                text = "Perform hash join on "+ tablesList[0] +" and "+ tablesList[1]
                tableNumber = self.getMaxTable(tablesList)
                text = text +" to get intermediate table T" + str(tableNumber + 1)
                text = text +"\n<html><b>Reason</b></html> hash join because it has better performance when doing equality join"

                node1.intermediateTable = "table T"+ str(tableNumber + 1)
                
            elif(item["Node Type"]=="Nested Loop"):
                tablesList = []
 
                for pNode in self.preNodeListDict[reversedcounter]:
                    if pNode.intermediateTable != '':
                        table = pNode.intermediateTable
                        tablesList.append(table)
                
                text = "Perform nested loop join ON "
                for t in tablesList:
                    text = text + t +" and " 
                text = text[0:len(text)-4]
                tableNumber = self.getMaxTable(tablesList)
                node1.intermediateTable = "table T"+str(tableNumber+1)
                text = text +" to get intermediate table T" + str(tableNumber + 1)
                self.tableNumber = tableNumber + 1

            elif(item["Node Type"]=="Merge Join"):
                tablesList = []
                for n in self.preNodeListDict[reversedcounter]:
                    if n.intermediateTable != '' :
                        tablesList.append(n.intermediateTable)
                
                text = "Perform merge join ON " 
                for t in tablesList:
                    text = text + t +" and " 
                text = text[0:len(text)-4]
                tableNumber = self.getMaxTable(tablesList)
                node1.intermediateTable = "table T"+str(tableNumber+1)
                text = text +" to get intermediate table T" + str(tableNumber + 1)     
                self.tableNumber = tableNumber + 1

            elif(item["Node Type"]=="Sort"):
                table = ""
                for pNode in self.preNodeListDict[reversedcounter]:
                    if pNode.intermediateTable != '':
                        table = (pNode.intermediateTable)
                        break
                text = "Sort on " + table +" ON "
                for sk in item["Sort Key"]:
                    text = text + sk+" "
                text = text +"to get intermediate table T" +str(self.tableNumber + 1)
                node1.intermediateTable = "table T"+str(self.tableNumber + 1)
                self.tableNumber = self.tableNumber + 1
                
            elif(item["Node Type"]=="Aggregate"):
                table = ""
                for pNode in self.preNodeListDict[reversedcounter]:
                    if pNode.intermediateTable != '':
                        table = (pNode.intermediateTable)
                        break
                text = "Perform aggregate ON " + table
                if "Group key" in item:
                    text = text + " with grouping attribute"
                    for sk in item["Group Key"]:
                        text = text + sk+" "
                text = text +"to get intermediate table T" +str(self.tableNumber + 1)
                node1.intermediateTable = "table T"+str(self.tableNumber + 1)
                self.tableNumber = self.tableNumber + 1

            elif(item["Node Type"]=="Gather Merge"):
                table = ""
                for pNode in self.preNodeListDict[reversedcounter]:
                    if pNode.intermediateTable != '':
                        table = (pNode.intermediateTable)
                        break
                text = "Perform Gather Merge"
                node1.intermediateTable = "table T"+str(int(table[-1]))


            text = text + "\nTotal cost: "+str(item["Total Cost"])
            node1.content.textbox.setHtml (text)
            
            self.curNodeList.append(node1)
            row = row + 1  
            reversedcounter = reversedcounter -1
            


        self.col = self.maxvalue
        self.preNodeList = self.curNodeList.copy()
        return rowTest-1
    # def traverse(self, node,counter):
                
    #     row = 0
    #     self.curNodeList = []
    #     toggle = False
    #     for item in node:
    #         print(item["Node Type"])
    #         inputs = 0
    #         if "Plans" in item:
    #             inputs = len(item["Plans"])
    #         if inputs == 1:
    #             node1 = Node(self.scene, item["Node Type"], inputs=[1], outputs=[1])
    #         elif inputs == 0 :
    #             node1 = Node(self.scene, item["Node Type"], inputs=[], outputs=[1])
    #         else:
    #             node1 = Node(self.scene, item["Node Type"], inputs=[1,1], outputs=[1])
    #         text = ""
    #         if(item["Node Type"]=="Seq Scan"):
    #             relationname = item["Relation Name"]
    #             text = "Perform sequential scan on "+relationname+""
                
    #         elif(item["Node Type"]=="Index Scan"):
    #             relationname = item["Relation Name"]
    #             text = "Perform Index Scan on "+relationname+""
                
    #         elif(item["Node Type"]=="Hash"):
    #             text=" Perform hash on Input Table"
                
    #         elif(item["Node Type"]=="Hash Join"):
    #             hashcondition  =  item["Hash Cond"]
    #             Listcondition = hashcondition.split("=")
    #             tablesList = []
    #             for con in Listcondition:
    #                 table = con.split(".")[0]
    #                 tablesList.append(table)
    #             text = "Perform hash join on table "+ tablesList[0]+" and "+tablesList[1]
    #         text = text + "\nTotal cost: "+str(item["Total Cost"])
    #         node1.content.textbox.setText(text)
    #         if toggle:
    #             node1.setPos(800-(self.col*250), -250 + (row+counter+1)*170)
    #         else:
    #             node1.setPos(800-(self.col*250), -250 + (row+counter)*170)
    #         self.curNodeList.append(node1)
    #         row = row + 1   
    #         if(inputs==2):
    #             toggle=True
    #     if len(self.preNodeList) != 0:
    #         preparentnode = self.preNodeList[counter]
    #         edge1 = Edge(self.scene, self.curNodeList[0].outputs[0], preparentnode.inputs[0], edge_type=EDGE_TYPE_BEZIER)
    #         if(len(self.curNodeList)==2):
    #             edge1 = Edge(self.scene, self.curNodeList[1].outputs[0], preparentnode.inputs[1], edge_type=EDGE_TYPE_BEZIER)

    #     self.col = self.col + 1
    #     self.preNodeList = self.curNodeList.copy()

        
        
    #     print("=========================")
    #     counter = 0
    #     for item in node:
    #         if "Plans" in item:
    #             self.traverse(item["Plans"],counter)
    #         counter = counter +1

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # crate graphics scene
        self.scene = Scene()
        # self.grScene = self.scene.grScene

        
        #self.addNodes(None)


        # create graphics view
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)


        self.setWindowTitle("Node Editor")
        self.show()


        # self.addDebugContent()
    def getinputNumber(self, node):
        inputs = 0
        if "Plans" in node:
            inputs = len(node["Plans"])
        ar = []
        for i in range(inputs):
            ar.append(1)
        return ar
    
    def buildPlan(self,planList,comboBox):       
        counter = 0
        for plan in planList:
            self.NodeDict= {}
            self.NodeDict[0,0] = plan["Plan"]
            if "Plans" in plan["Plan"]:
                self.traverseNew(plan["Plan"]["Plans"],self.col,0)
            
            self.AllNodeDict[counter] = self.NodeDict
            if(counter == 0):
                comboBox.addItem("Selected Plan")
            else:
                comboBox.addItem("Alternative Plan" + str(counter))
            counter = counter + 1
        #display First plan
        #self.addNodes(self.AllNodeDict[0])
        
    def changePlan(self, index):
        self.scene.clearData()
        self.addNodes(self.AllNodeDict[index])
    
    def addTable(self,reasonTextbox):
        headers = []
        rows = []
        count = 1
        for item in self.AllNodeDict:
            headers.append("P"+str(count))
            count = count+1
        rowitem = []
        for item in self.AllNodeDict:
            s = self.AllNodeDict[item][0,0]
            num = s["Total Cost"]
            formated = f"{num:,}"
            rowitem.append(formated)
        
        rows.append(rowitem)
        from jinja2 import Template
        table = """
        <style>
        p{
            width = 10px
        }
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width = 100%
        }
        
        td, th {
            border: 1px solid #dddddd;
            text-align: center;
            padding: 8px;
 
        }
        </style>
        
        <table border="1" width = 100%>
            <tr >{% for header in headers %}<th>{{header}}</th>{% endfor %}</tr>
            {% for row in rows %}<tr>
                {% for element in row %}<td>
                    {{element}}
                </td>{% endfor %}
            </tr>{% endfor %}
        </table>
        """
        reasonTextbox.setText(Template(table).render(headers=headers, rows=rows))
        reasonTextbox.append("\n\n")
        reasonTextbox.append("<p style=\" font-size:18px \"><b>Plan 1</b> is selected because it has the least cost amongst other plans.</p>")
        for item in self.AllNodeDict[0]:
            for node in self.AllNodeDict[0][item]:
                nodeType = self.AllNodeDict[0][item][node]
                if nodeType == "Index Scan":
                    nodeTable = self.AllNodeDict[0][item]["Relation Name"]
                    predicate = "predicate"
                    if "Index Cond" in self.AllNodeDict[0][item]:
                        indCon = self.AllNodeDict[0][item]["Index Cond"]
                        predicate = predicate + " "+ indCon 
                    reasonTextbox.append("<p style=\"font-size:18px\">High selectivity of "+predicate+" will make index<br> scan on <b>"+nodeTable+"</b> faster.</p>")
        for item in self.AllNodeDict[0]:
            for node in self.AllNodeDict[0][item]:
                nodeType = self.AllNodeDict[0][item][node]
                if nodeType == "Seq Scan":
                    nodeTable = self.AllNodeDict[0][item]["Relation Name"]
                    predicate = "predicate"
                    if "Filter" in self.AllNodeDict[0][item]:
                        filterCon = self.AllNodeDict[0][item]["Filter"]
                        predicate = predicate + " "+ filterCon 
                        reasonTextbox.append("<p style=\"font-size:18px\">Low selectivity of "+predicate+" will make seq <br> scan on <b>"+nodeTable+"</b> faster.</p>")
        for item in self.AllNodeDict[0]:
            for node in self.AllNodeDict[0][item]:
                nodeType = self.AllNodeDict[0][item][node]
                if nodeType == "Merge Join":
                    if "Merge Cond" in self.AllNodeDict[0][item]:
                        filterCon = self.AllNodeDict[0][item]["Merge Cond"]
                        reasonTextbox.append("<p style=\"font-size:18px\">Merge Joins are preferred if the join condition uses an equality operator and both sides of the join are large</[>")
        reasonTextbox.append("<br>")
        for item in self.AllNodeDict[0]:
            for node in self.AllNodeDict[0][item]:
                nodeType = self.AllNodeDict[0][item][node]
                if nodeType == "Hash Join":
                    if "Hash Cond" in self.AllNodeDict[0][item]:
                        hashcondition = self.AllNodeDict[0][item]["Hash Cond"]
                    reasonTextbox.append("<p style=\"font-size:18px\">Hash join has better performance when doing equality join <b>where</b> hash condition is ")
                    reasonTextbox.append("<p style=\"font-size:18px\">"+hashcondition+" </p>")
        reasonTextbox.append("<br>")
        for item in self.AllNodeDict[0]:
            for node in self.AllNodeDict[0][item]:
                nodeType = self.AllNodeDict[0][item][node]
                if nodeType == "Nested Loop":
                    reasonTextbox.append("<p style=\"font-size:18px\">Nested loop joins are ideal when the driving row source (the records you are looking<br> for) is small and the joined columns of the inner row source are uniquely indexed or<br> have a highly selective nonunique index</p>")
                    return
    def addDetails(self,NodeDict,nodeList):
        for key in nodeList.keys():
            node = nodeList[key]
            skey = str(key)
            skey = skey[1:-1].split(',')
            row = int(skey[0].strip())
            col = int(skey[1].strip())
            nodeDetail = NodeDict[row,col]
            text = ""
            costText =  "<br><br><b>Total cost :</b> "+ str(nodeDetail["Total Cost"])
            nodeType = nodeDetail["Node Type"]
            if  nodeType== "Seq Scan" or nodeType=="Index Scan" or nodeType=="Index Only Scan" or nodeType == "Bitmap Heap Scan":
                relationname = nodeDetail["Relation Name"]
                text = "Perform "+nodeType+" on <b>"+relationname+"</b>"
                text = text + costText
                node.content.textbox.setHtml(text)
            # if  nodeType == "Bitmap Index Scan":
            #     relationname = nodeDetail[""]
            #     text = "Perform "+nodeType+" on <b>"+relationname+"</b>"
            #     text = text + costText
            #     node.content.textbox.setHtml(text)
            if nodeType == "Hash Join":
                text ="<b>Reason :</b> hash join because it has better performance when doing equality join"
                text = text + costText
                node.content.textbox.setHtml(text)
            
    def addNodes(self,NodeDict):
        self.nodes = {}
        for a in NodeDict.keys():
            key = str(a)
            key = key[1:-1].split(',')
            row = int(key[0].strip())
            col = int(key[1].strip())
            print(NodeDict[a]["Node Type"] +" Row: "+str(row) +" Col: "+str(col))
            ar = self.getinputNumber(NodeDict[a])
            if(row == 0 and col == 0):
                node1 = Node(self.scene, NodeDict[a]["Node Type"], inputs=ar, outputs=[])
            else:
                node1 = Node(self.scene, NodeDict[a]["Node Type"], inputs=ar, outputs=[1])
            node1.nodeType = NodeDict[a]["Node Type"]
            if "Relation Name" in NodeDict[a]:
                node1.nodeTable = NodeDict[a]["Relation Name"]
            node1.setPos(600+(-col*250), row*170)
            text =""
            text = text + "<b>Total cost:</b> "+ str(NodeDict[a]["Total Cost"])
            node1.content.textbox.setHtml (text)
            
            self.nodes[str(a)]= node1
        for b in self.nodes.keys():
            node = self.nodes[b]
            key = str(b)
            key = key[1:-1].split(',')
            row = int(key[0].strip())
            col = int(key[1].strip())
            
            #go left look for left node to link
            col1 = col + 1
            keyS ='('+str(row)+', '+str(col1)+')'
            if keyS in self.nodes:
                edge1 = Edge(self.scene, self.nodes[keyS].outputs[0], node.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        
        for c in self.nodes.keys():
            node = self.nodes[c]
            key = str(c)
            key = key[1:-1].split(',')
            row = int(key[0].strip())
            col = int(key[1].strip())
            
            #go right-up look for right-up node to link
            #if dont exist keep go up
            col_right = col - 1
            row_top = row - 1
            if(col_right<0 or row_top<0):
                continue
            else:
                nodeTo_right ='('+str(row)+', '+str(col_right)+')'
                if nodeTo_right in self.nodes:continue
                for r in range(row):
                    node_right ='('+str(row_top)+', '+str(col_right)+')'
                    if node_right in self.nodes:
                        unlinkNode = self.nodes[node_right]
                        if(unlinkNode.toggle == True):
                            edge1 = Edge(self.scene, node.outputs[0], unlinkNode.inputs[2], edge_type=EDGE_TYPE_BEZIER)
                            break
                        else:
                            edge1 = Edge(self.scene, node.outputs[0], unlinkNode.inputs[1], edge_type=EDGE_TYPE_BEZIER)
                            unlinkNode.toggle = True
                            break
                    row_top = row_top -1
        self.addDetails(NodeDict,self.nodes)

        # self.preNaodeListDict[0] = self.curNodeList.copy()
        # c = len(jsonObject["Plan"]["Plans"])
        # if(c==1):
        #     node1 = Node(self.scene, jsonObject["Plan"]["Node Type"], inputs=[1], outputs=[])
        #   a  node1.setPos(-350+(self.col*250), (-1)*170)
        #     if len(self.preNodeList) != 0:
        #         edge1 = Edge(self.scene, self.preNodeList[0].outputs[0], node1.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        # if(c==2):
        #     node1 = Node(self.scene, jsonObject["Plan"]["Node Type"], inputs=[1,1], outputs=[])
        #     node1.setPos(-350+(self.col*250), (-1)*170)
        #     if len(self.preNodeList) != 0:
        #         edge1 = Edge(self.scene, self.preNodeList[0].outputs[0], node1.inputs[1], edge_type=EDGE_TYPE_BEZIER)
        #         edge1 = Edge(self.scene, self.preNodeList[1].outputs[0], node1.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        # firstNode = jsonObject["Plan"]
  
        
        # text = ""
        # reversedcounter = 0
        # if(firstNode["Node Type"]=="Seq Scan"):
        #     table = ""
        #     if reversedcounter in self.preNodeListDict:
        #         for pNode in self.preNodeListDict[reversedcounter]:
        #             if pNode.intermediateTable != '':
        #                 table = (pNode.intermediateTable)
        #                 break
        #     relationname = firstNode["Relation Name"]
        #     text = "Perform sequential scan on "+relationname+""
        #     if "Filter" in firstNode:
        #         self.tableNumber = self.tableNumber + 1
        #         if( table ==""):
        #             text = text + " as table T1"
        #             node1.intermediateTable = "table T1"
        #         else:
        #             text = text + " as table T" +str(self.tableNumber)
        #             node1.intermediateTable = "table T" +str(self.tableNumber)
        #     else:
        #         node1.intermediateTable = relationname
        # elif(firstNode["Node Type"]=="Index Only Scan"):
        #     relationname = firstNode["Relation Name"]
        #     text = "Perform Index Only Scan on "+relationname+""
        #     table = ""
        #     if reversedcounter in self.preNodeListDict:
        #         for pNode in self.preNodeListDict[reversedcounter]:
        #             if pNode.intermediateTable != '':
        #                 table = (pNode.intermediateTable)
        #                 break
        #     node1.intermediateTable = relationname
            
        # elif(firstNode["Node Type"]=="Index Scan"):
        #     relationname = firstNode["Relation Name"]
        #     text = "Perform Index Scan on "+relationname+""
        #     table = ""
        #     if reversedcounter in self.preNodeListDict:
        #         for pNode in self.preNodeListDict[reversedcounter]:
        #             if pNode.intermediateTable != '':
        #                 table = (pNode.intermediateTable)
        #                 break
        #     if "Filter" in firstNode:
        #         self.tableNumber = self.tableNumber + 1
        #         if( table ==""):
        #             text = text + " as table T1"
        #             node1.intermediateTable = "table T1"
        #         else:
        #             text = text + " as table T" +str(self.tableNumber)
        #             node1.intermediateTable = "table T" +  str(self.tableNumber)
        #     else:
        #         node1.intermediateTable = relationname
        # elif(firstNode["Node Type"]=="Hash"):
        #     text="Hash " + self.preNodeListDict[reversedcounter][0].intermediateTable
        #     node1.intermediateTable = self.preNodeListDict[reversedcounter][0].intermediateTable
        #     self.getMaxTable([self.preNodeListDict[reversedcounter][0].intermediateTable])
            
        # elif(firstNode["Node Type"]=="Hash Join"):
        #     # interTableList = []
        #     # for pNode in self.preNodeList:
        #     #     if pNode.intermediateTable != '':
        #     #         interTableList.append(pNode.intermediateTable)
        #     hashcondition  =  firstNode["Hash Cond"]
        #     Listcondition = hashcondition.split("=")
        #     tablesList = []
        #     for n in self.preNodeListDict[reversedcounter]:
        #         if n.intermediateTable != '' :
        #             tablesList.append(n.intermediateTable)
                
        #     for con in Listcondition:
        #         table = con.split(".")[0]
        #         tablesList.append(table)
        #     text = "Perform hash join on "+ tablesList[0] +" and "+ tablesList[1]
        #     tableNumber = self.getMaxTable(tablesList)
        #     text = text +" to get result table T" + str(tableNumber + 1)
            
        #     text = text +"\nReason hash join because it has better performance when doing equality join"

        #     node1.intermediateTable = "table T"+ str(tableNumber + 1)
            
        # elif(firstNode["Node Type"]=="Nested Loop"):
        #     tablesList = []
 
        #     for pNode in self.preNodeListDict[reversedcounter]:
        #         if pNode.intermediateTable != '':
        #             table = pNode.intermediateTable
        #             tablesList.append(table)
            
        #     text = "Perform nested loop join ON "
        #     for t in tablesList:
        #         text = text + t +" and " 
        #     text = text[0:len(text)-4]
        #     tableNumber = self.getMaxTable(tablesList)
        #     node1.intermediateTable = "table T"+str(tableNumber+1)
        #     text = text +" to get result table T" + str(tableNumber + 1)

        # elif(firstNode["Node Type"]=="Merge Join"):
        #     tablesList = []
        #     for n in self.preNodeListDict[reversedcounter]:
        #         if n.intermediateTable != '' :
        #             tablesList.append(n.intermediateTable)
            
        #     text = "Perform merge join ON " 
        #     for t in tablesList:
        #         text = text + t +" and " 
        #     text = text[0:len(text)-4]
        #     tableNumber = self.getMaxTable(tablesList)
        #     node1.intermediateTable = "table T"+str(tableNumber+1)
        #     text = text +" to get result table T" + str(tableNumber + 1)            

        # elif(firstNode["Node Type"]=="Sort"):
        #     table = ""
        #     for pNode in self.preNodeListDict[reversedcounter]:
        #         if pNode.intermediateTable != '':
        #             table = (pNode.intermediateTable)
        #             break
        #     text = "Sort on " + table +" ON "
        #     for sk in firstNode["Sort Key"]:
        #         text = text + sk+" "
        #     text = text +"to get result table T" +str(self.tableNumber + 1)
        #     node1.intermediateTable = "table T"+str(self.tableNumber + 1)
        #     self.tableNumber = self.tableNumber + 1
            
        # elif(firstNode["Node Type"]=="Aggregate"):
        #     table = ""
        #     for pNode in self.preNodeListDict[reversedcounter]:
        #         if pNode.intermediateTable != '':
        #             table = (pNode.intermediateTable)
        #             break
        #     text = "Perform aggregate ON " + table
        #     if "Group key" in firstNode:
        #         text = text + " with grouping attribute"
        #         for sk in firstNode["Group Key"]:
        #             text = text + sk+" "
        #     text = text +"to get intermediate table T" +str(self.tableNumber + 1)
        #     node1.intermediateTable = "table T"+str(self.tableNumber + 1)
            
        # elif(firstNode["Node Type"]=="Gather Merge"):
        #     table = ""
        #     for pNode in self.preNodeListDict[reversedcounter]:
        #         if pNode.intermediateTable != '':
        #             table = (pNode.intermediateTable)
        #             break
        #     text = "Perform Gather Merge"
        #     node1.intermediateTable = "table T"+str(int(table[-1]))


        # text = text + "\nTotal cost: "+str(firstNode["Total Cost"])
        # node1.content.textbox.setText(text)
        
        
        # node1 = Node(self.scene, "Merge Sort", inputs=[1,1], outputs=[1])
        # node2 = Node(self.scene, "Seq Scan", inputs=[1,1], outputs=[1])
        # node3 = Node(self.scene, "Sort", inputs=[1,1], outputs=[1])
        # node1.setPos(-350, -250)
        # node2.setPos(-75, 0)
        # node3.setPos(200, -150)
        # edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        # edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[0], edge_type=EDGE_TYPE_BEZIER)

    def loadStylesheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        #QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

    def removeroot(item):
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