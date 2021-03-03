from PySide2 import QtCore, QtGui, QtWidgets


class GraphicsScene(QtWidgets.QGraphicsScene):
    click = QtCore.Signal(object)


class GraphicsEllipse(QtWidgets.QGraphicsEllipseItem):

    def __init__(self, label, pen, brush, *params):
        super().__init__(*params)
        self.setPen(pen)
        self.setBrush(brush)
        self.label = label
        wlabel = QtWidgets.QLabel(label)
        wlabel.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        wlabel.setStyleSheet("color : black; font-weight: bold; font-size: 30px; ")
        wlabel.setAlignment(QtCore.Qt.AlignCenter)
        proxy = QtWidgets.QGraphicsProxyWidget(self)
        proxy.setWidget(wlabel)
        proxy.setPos(self.boundingRect().center()-wlabel.rect().center())
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.connections = []

    def mousePressEvent(self, event):
        self.scene().click.emit(self)

    def dropEvent(self, event):
        return super().dropEvent(event)

    def mouseMoveEvent(self, event):
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        for conn in self.connections:
            conn.drawLine()

        return super().mouseReleaseEvent(event)

    def getPosition(self):
        offset = QtCore.QPointF(100 + 30, 100 + 30)
        p = self.pos() + offset
        p = p.toTuple()
        return (p[0]/480, 1.0 - p[1]/480)

    def add_connection(self, conn):
        self.connections.append(conn)


class GraphicsLine(QtWidgets.QGraphicsLineItem):
    def __init__(self, a, b, radius):
        super().__init__()
        self.setPen(QtGui.QPen(QtCore.Qt.white,  4))
        self.setZValue(-1)
        self.node_a = a
        self.node_b = b
        self.r = radius
        self.drawLine()

    def drawLine(self):
        offset = QtCore.QPointF(100 + self.r, 100 + self.r)
        pa = self.node_a.pos() + offset
        pb = self.node_b.pos() + offset
        self.setLine(*pa.toTuple(), *pb.toTuple())
