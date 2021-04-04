from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget
from node_socket import *


class Node():
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs = []):
        self.scene = scene
        self.intermediateTable = ""
        self.nodeType =""
        self.nodeTable = ""
        self.title = title
        self.content = QDMNodeContentWidget()
        self.grNode = QDMGraphicsNode(self)
        self.toggle = False
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 22

        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_TOP)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_BOTTOM)
            counter += 1
            self.outputs.append(socket)

    @property
    def pos(self):
        return self.grNode.pos()        # QPointF
    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

    def getSocketPosition(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.grNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = -20+ self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else :
            # start from top
            y = 20+self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing

        return [x, y]

