from PySide2.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QHBoxLayout,\
     QAbstractItemView, QPushButton, QGraphicsView, QLabel, QFileDialog
from PySide2.QtGui import QBrush, QPen
from PySide2.QtCore import Qt

import sys
from graphics import GraphicsEllipse, GraphicsScene, GraphicsLine
import json


NODE_R = 30
NODE_D = NODE_R * 2


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Designer")
        self.setGeometry(300, 200, 840, 720)
        self.current_id = 1
        self.createLayout()

        self.couple = []
        self.show()

    def makeButtonsLayout(self):
        self.button = QPushButton("Add Node", self)
        self.button.clicked.connect(self.addNode)

        self.btn_connection = QPushButton("Add Connection:", self)
        self.btn_connection.clicked.connect(self.addConnection)

        self.button3 = QPushButton("Export Network", self)
        self.button3.clicked.connect(self.file_save)

        self.lbl_connection = QLabel("Connection")

        self.l_btns = QHBoxLayout()
        self.l_btns.addWidget(self.button3)
        self.l_btns.addStretch()
        self.l_btns.addWidget(self.btn_connection)
        self.l_btns.addWidget(self.lbl_connection)
        self.l_btns.addStretch()
        self.l_btns.addWidget(self.button)
        self.btns = QWidget()
        self.btns.setLayout(self.l_btns)
        self.btns.setFixedHeight(40)

    def initializeGview(self):
        self.scene = GraphicsScene()
        self.scene.setSceneRect(0, 0, 480, 480)
        self.scene.click.connect(self.keepNode)
        self.addNode()
        self.view = QGraphicsView(self.scene)
        self.view.setGeometry(0, 0, 500, 500)
        self.view.scale(1, 1)

    def createOrderList(self):
        self.orderList = QListWidget()
        # Enable drag & drop ordering of items.
        self.orderList.setDragDropMode(QAbstractItemView.InternalMove)

    def createLayout(self):
        self.makeButtonsLayout()
        self.initializeGview()
        self.createOrderList()

        l_network = QHBoxLayout()
        l_network.addWidget(self.view)
        l_network.addStretch()
        l_network.addWidget(self.orderList)

        self.l_root = QVBoxLayout()
        self.l_root.addLayout(l_network)
        self.l_root.addStretch()
        self.l_root.addWidget(self.btns)

        # self.l_root.addWidget(self.view)
        self.setLayout(self.l_root)

    def addNode(self):
        greenBrush = QBrush(Qt.green)
        blackPen = QPen(Qt.black)
        # blueBrush = QBrush(Qt.blue)

        blackPen.setWidth(5)
        ellipse = GraphicsEllipse(str(self.current_id), blackPen, greenBrush, 100, 100, NODE_D, NODE_D)
        self.scene.addItem(ellipse)
        self.current_id += 1

    def keepNode(self, node):
        if len(self.couple) < 2:
            self.couple.append(node)
        else:
            self.couple.pop(0)
            self.couple.append(node)
        if len(self.couple) == 2:
            self.lbl_connection.setText(self.couple[0].label + " --> " + self.couple[1].label)

    def addConnection(self):
        line = GraphicsLine(self.couple[0], self.couple[1], NODE_R)
        self.scene.addItem(line)

        for v in self.couple:
            v.add_connection(line)
        self.orderList.addItem(self.lbl_connection.text())

    def getNodes(self):
        positions = {}
        for i in self.scene.items():
            if type(i) is GraphicsEllipse:
                positions[int(i.label)] = i.getPosition()
        return positions

    def getConnections(self):
        connections = []
        for i in range(self.orderList.count()):
            conn = self.orderList.item(i).text().split(" --> ")
            connections.append((int(conn[0]), int(conn[1]), {"label": str(i + 1)}))
        return connections

    def file_save(self):
        positions = self.getNodes()
        connections = self.getConnections()
        network = {}
        network["labels"] = {i: i for i in sorted(list(positions.keys()))}
        network["edges"] = connections
        network["pos"] = positions
        text = json.dumps(network)
        name = QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name[0], 'w')
        # text = "something"
        file.write(text)
        file.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
