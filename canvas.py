from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
import math
# ...existing code...

class GraphCanvas(QWidget):
    graphDataChanged = pyqtSignal(dict)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.end_id = None
        self.graph_data = {"nodes": [], "edges": []}
        self.showNodeIDs = True
        self.showEdgeWeights = True
        self.showGrid = True  # 默认显示网格
        self.grid_size = 50   # 网格大小(像素)
        self.addNodeMode = False
        self.searchPath = []
        self.searchOrder = []
        self.addEdgeMode = False
        self.edgeDirected = False
        self.selectedNodes = []
    def loadData(self, data):
        self.graph_data = data
        self.update()

    def enableAddNodeMode(self, enabled):
        self.addNodeMode = enabled


    def snapToGrid(self, x, y):
        """将坐标吸附到最近的网格点"""
        grid_x = round(x / self.grid_size) * self.grid_size
        grid_y = round(y / self.grid_size) * self.grid_size
        return grid_x, grid_y

    def isNodeAtPosition(self, x, y):
        """检查指定位置是否已有节点"""
        for node in self.graph_data["nodes"]:
            if node["x"] == x and node["y"] == y:
                return True
        return False

    def addEdge(self, directed=False):
        """启用添加边模式，允许用户通过点击两个节点来创建边"""
        self.addEdgeMode = True
        self.edgeDirected = directed
        self.selectedNodes = []
        if hasattr(self.parent(), 'statusBar'):
            self.parent().statusBar().showMessage("请选择第一个节点")

    def getNodeAtPosition(self, x, y):
        """检测给定位置是否有节点，有则返回节点对象"""
        for node in self.graph_data["nodes"]:
            # 检查点击位置是否在节点圆形区域内
            dx = x - node["x"]
            dy = y - node["y"]
            if dx*dx + dy*dy <= 100:  # 10*10 节点半径为10
                return node
        return None

    def mousePressEvent(self, event):
        if self.addNodeMode:
            # 原有的添加节点代码保持不变
            x, y = self.snapToGrid(event.x(), event.y())
            if not self.isNodeAtPosition(x, y):
                new_id = str(len(self.graph_data["nodes"]) + 1)
                self.graph_data["nodes"].append({"id": new_id, "x": x, "y": y})
                self.graphDataChanged.emit(self.graph_data)
            self.update()
        elif hasattr(self, 'addEdgeMode') and self.addEdgeMode:
            # 处理添加边模式下的点击
            node = self.getNodeAtPosition(event.x(), event.y())
            if node:
                self.selectedNodes.append(node)
                if len(self.selectedNodes) == 1:
                    if hasattr(self.parent(), 'statusBar'):
                        self.parent().statusBar().showMessage("请选择第二个节点")
                elif len(self.selectedNodes) == 2:
                    # 选择了两个节点，添加边
                    start_node = self.selectedNodes[0]
                    end_node = self.selectedNodes[1]

                    # 计算两点之间的欧氏距离作为权重
                    import math
                    dx = (start_node["x"] - end_node["x"])/50
                    dy = (start_node["y"] - end_node["y"])/50
                    weight = round(float(math.sqrt(dx*dx + dy*dy)), 2)

                    # 创建边
                    edge_info = {
                        "start": start_node["id"],
                        "end": end_node["id"],
                        "weight": weight,
                        "directed": self.edgeDirected
                    }
                    self.graph_data["edges"].append(edge_info)
                    self.graphDataChanged.emit(self.graph_data)
                    # 重置状态
                    self.selectedNodes = []
                    if hasattr(self.parent(), 'statusBar'):
                        self.parent().statusBar().showMessage("边已添加")
                    self.update()

    def toggleNodeIDs(self):
        self.showNodeIDs = not self.showNodeIDs
        self.update()

    def toggleEdgeWeights(self):
        self.showEdgeWeights = not self.showEdgeWeights
        self.update()

    def updateSearchVisualization(self, order, path, end_id):
        self.searchOrder = order
        self.searchPath = path
        self.end_id = end_id
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制网格点
        if self.showGrid:
            painter.setPen(QPen(QColor(200, 200, 200), 1))
            width, height = self.width(), self.height()

            # 计算网格点数量
            cols = width // self.grid_size + 1
            rows = height // self.grid_size + 1

            # 收集节点位置集合，用于检查是否被节点覆盖
            node_positions = {(node["x"], node["y"]) for node in self.graph_data["nodes"]}

            # 绘制网格点
            for i in range(cols):
                for j in range(rows):
                    x = i * self.grid_size
                    y = j * self.grid_size
                    # 如果该网格点没有被节点覆盖，则显示
                    if (x, y) not in node_positions:
                        painter.drawEllipse(x - 2, y - 2, 4, 4)

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

            # 计算向量和长度
            # 计算向量和长度
            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx * dx + dy * dy)

            if length > 0:
                # 单位向量
                ux, uy = dx / length, dy / length

                # 如果是有向边
                if edge.get("directed", False):
                    # 绘制线段到节点中心
                    painter.drawLine(x1, y1, x2, y2)

                    # 绘制箭头
                    arrow_size = 10
                    r = 10  # 节点半径
                    # 箭头底部位置
                    arrow_base_x = x2 - r * ux
                    arrow_base_y = y2 - r * uy

                    angle = math.atan2(uy, ux)
                    ax1 = arrow_base_x - arrow_size * math.cos(angle - math.pi / 6)
                    ay1 = arrow_base_y - arrow_size * math.sin(angle - math.pi / 6)
                    ax2 = arrow_base_x - arrow_size * math.cos(angle + math.pi / 6)
                    ay2 = arrow_base_y - arrow_size * math.sin(angle + math.pi / 6)

                    # 创建并填充箭头三角形，箭头尖端指向节点中心
                    arrow_path = QPainterPath()
                    arrow_path.moveTo(x2, y2)  # 箭头尖端在节点中心
                    arrow_path.lineTo(ax1, ay1)
                    arrow_path.lineTo(ax2, ay2)
                    arrow_path.closeSubpath()

                    # 安全地获取画笔颜色
                    pen = painter.pen()
                    if pen:
                        painter.setBrush(QBrush(pen.color()))
                    else:
                        painter.setBrush(QBrush(Qt.black))

                    painter.drawPath(arrow_path)
                else:
                    # 无向边直接画线
                    painter.drawLine(x1, y1, x2, y2)

                # 显示边权重
                if self.showEdgeWeights:
                    midx = (x1 + x2) // 2
                    midy = (y1 + y2) // 2
                    # 权重文本向上偏移，避免被线遮挡
                    offset = 15
                    painter.drawText(midx, midy - offset, str(edge["weight"]))

        # 再画节点
        for node in self.graph_data["nodes"]:
            r = 10
            # 默认为空心节点（未搜索的节点）
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(Qt.black, 1))

            # 如果节点在搜索路径或搜索顺序中，则使用实心并设置对应颜色
            if self.searchOrder and (node["id"] == self.searchOrder[0] or (node["id"] in self.searchOrder and node["id"] == self.end_id)):
                painter.setBrush(QBrush(Qt.red))
            elif node["id"] in self.searchPath:
                painter.setBrush(QBrush(Qt.blue))
            elif node["id"] in self.searchOrder:
                painter.setBrush(QBrush(Qt.yellow))

            painter.drawEllipse(node["x"] - r, node["y"] - r, 2 * r, 2 * r)

            if self.showNodeIDs:
                painter.drawText(node["x"] - 5, node["y"] + 20, node["id"])

    def getNodeById(self, nid):
        for node in self.graph_data["nodes"]:
            if node["id"] == nid:
                return node
        return None
