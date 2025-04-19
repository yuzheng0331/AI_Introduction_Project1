from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRect
# ...existing code...

class GraphCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph_data = {"nodes": [], "edges": []}
        self.showNodeIDs = True
        self.showEdgeWeights = True
        self.addNodeMode = False
        self.searchPath = []
        self.searchOrder = []

    def loadData(self, data):
        self.graph_data = data
        self.update()

    def enableAddNodeMode(self, enabled):
        self.addNodeMode = enabled

    def mousePressEvent(self, event):
        if self.addNodeMode:
            x, y = event.x(), event.y()
            new_id = str(len(self.graph_data["nodes"]) + 1)
            self.graph_data["nodes"].append({"id": new_id, "x": x, "y": y})
            self.addNodeMode = False
            self.update()

    def addEdgeDialog(self):
        start_id, ok1 = QInputDialog.getText(self, "添加边", "输入起点ID", QLineEdit.Normal, "")
        if not ok1 or not start_id:
            return
        end_id, ok2 = QInputDialog.getText(self, "添加边", "输入终点ID", QLineEdit.Normal, "")
        if not ok2 or not end_id:
            return
        weight, ok3 = QInputDialog.getInt(self, "添加边", "输入权重", 1, 1)
        if not ok3:
            return
        direction, ok4 = QInputDialog.getItem(self, "添加边", "方向", ["有向", "无向"], 0, False)
        if not ok4:
            return
        edge_info = {
            "start": start_id,
            "end": end_id,
            "weight": weight,
            "directed": (direction == "有向")
        }
        self.graph_data["edges"].append(edge_info)
        self.update()

    def toggleNodeIDs(self):
        self.showNodeIDs = not self.showNodeIDs
        self.update()

    def toggleEdgeWeights(self):
        self.showEdgeWeights = not self.showEdgeWeights
        self.update()

    def updateSearchVisualization(self, order, path):
        self.searchOrder = order
        self.searchPath = path
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 先画边
        for edge in self.graph_data["edges"]:
            start_node = self.getNodeById(edge["start"])
            end_node = self.getNodeById(edge["end"])
            if not start_node or not end_node:
                continue
            painter.setPen(QPen(Qt.black, 2))
            if edge["start"] in self.searchPath and edge["end"] in self.searchPath:
                painter.setPen(QPen(Qt.blue, 3))
            x1, y1 = start_node["x"], start_node["y"]
            x2, y2 = end_node["x"], end_node["y"]
            painter.drawLine(x1, y1, x2, y2)
            if self.showEdgeWeights:
                midx, midy = (x1 + x2) // 2, (y1 + y2) // 2
                painter.drawText(midx, midy, str(edge["weight"]))
        # 再画节点
        for node in self.graph_data["nodes"]:
            r = 10
            color = Qt.black
            if node["id"] == self.searchOrder[0] or node["id"] == self.searchOrder[-1]:
                color = Qt.red
            elif node["id"] in self.searchPath:
                color = Qt.blue
            elif node["id"] in self.searchOrder:
                color = Qt.yellow
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.black, 1))
            painter.drawEllipse(node["x"] - r, node["y"] - r, 2 * r, 2 * r)
            if self.showNodeIDs:
                painter.drawText(node["x"] - 5, node["y"] + 20, node["id"])

    def getNodeById(self, nid):
        for node in self.graph_data["nodes"]:
            if node["id"] == nid:
                return node
        return None
