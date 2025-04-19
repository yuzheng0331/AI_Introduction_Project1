from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange, QTableWidgetSelectionRange
# ...existing code...
from PyQt5.QtCore import Qt
from canvas import GraphCanvas
from readwrite import GraphIO
from algorithms import GraphAlgorithms

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ...existing code...
        self.setWindowTitle("可视化最短路径演示")
        self.graph_data = {"nodes": [], "edges": []}
        self.initUI()

    def initUI(self):
        # 顶栏布局
        topWidget = QWidget()
        topLayout = QHBoxLayout()
        self.importBtn = QPushButton("Import")
        self.importBtn.clicked.connect(self.onImportFile)
        self.exportBtn = QPushButton("Export")
        self.exportBtn.clicked.connect(self.onExportFile)
        self.addNodeBtn = QPushButton("Add Node")
        self.addNodeBtn.clicked.connect(self.onAddNode)
        self.addEdgeBtn = QPushButton("Add Edge")
        self.addEdgeBtn.clicked.connect(self.onAddEdge)
        self.showNodeBtn = QPushButton("Show/Hide Node IDs")
        self.showNodeBtn.clicked.connect(self.onToggleNodeIDs)
        self.showEdgeBtn = QPushButton("Show/Hide Edge Weights")
        self.showEdgeBtn.clicked.connect(self.onToggleEdgeWeights)
        # ...existing code...
        topLayout.addWidget(self.importBtn)
        topLayout.addWidget(self.exportBtn)
        topLayout.addWidget(self.addNodeBtn)
        topLayout.addWidget(self.addEdgeBtn)
        topLayout.addWidget(self.showNodeBtn)
        topLayout.addWidget(self.showEdgeBtn)
        topWidget.setLayout(topLayout)

        # 左侧栏布局
        leftWidget = QWidget()
        leftLayout = QVBoxLayout()
        self.dfsBtn = QPushButton("DFS")
        self.dfsBtn.clicked.connect(lambda: self.onSearchAlgorithm("DFS"))
        self.bfsBtn = QPushButton("BFS")
        self.bfsBtn.clicked.connect(lambda: self.onSearchAlgorithm("BFS"))
        self.aStarBtn = QPushButton("A*")
        self.aStarBtn.clicked.connect(lambda: self.onSearchAlgorithm("A*"))
        self.dijkstraBtn = QPushButton("Dijkstra")
        self.dijkstraBtn.clicked.connect(lambda: self.onSearchAlgorithm("Dijkstra"))
        leftLayout.addWidget(self.dfsBtn)
        leftLayout.addWidget(self.bfsBtn)
        leftLayout.addWidget(self.aStarBtn)
        leftLayout.addWidget(self.dijkstraBtn)

        # 起止点输入
        self.startLabel = QLabel("起点ID:")
        self.startEdit = QLineEdit()
        self.endLabel = QLabel("终点ID:")
        self.endEdit = QLineEdit()
        leftLayout.addWidget(self.startLabel)
        leftLayout.addWidget(self.startEdit)
        leftLayout.addWidget(self.endLabel)
        leftLayout.addWidget(self.endEdit)

        # 开始搜索按钮
        self.startSearchBtn = QPushButton("开始搜索")
        self.startSearchBtn.clicked.connect(self.onStartSearch)
        leftLayout.addWidget(self.startSearchBtn)

        # 结果输出表
        self.resultTable = QTableWidget()
        self.resultTable.setColumnCount(2)
        self.resultTable.setHorizontalHeaderLabels(["Order", "Node ID"])
        leftLayout.addWidget(self.resultTable)

        # 已探索节点数、路径总权重
        self.infoLabel = QLabel("已探索节点: 0 | 路径总权重: 0")
        leftLayout.addWidget(self.infoLabel)
        leftWidget.setLayout(leftLayout)

        # 正中央画布
        self.canvas = GraphCanvas(self)
        # 全局布局
        centralWidget = QWidget()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(topWidget)
        bodylayout = QHBoxLayout()
        bodylayout.addWidget(leftWidget)
        bodylayout.addWidget(self.canvas, 1)
        mainLayout.addLayout(bodylayout)
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def onImportFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, "导入图", "", "JSON/CSV Files (*.json *.csv)")
        # ...existing code...
        if fname:
            self.graph_data = GraphIO.loadGraph(fname)
            self.canvas.loadData(self.graph_data)

    def onExportFile(self):
        fname, _ = QFileDialog.getSaveFileName(self, "导出图", "", "JSON/CSV Files (*.json *.csv)")
        if fname:
            GraphIO.saveGraph(fname, self.graph_data)

    def onAddNode(self):
        self.canvas.enableAddNodeMode(True)

    def onAddEdge(self):
        self.canvas.addEdgeDialog()

    def onToggleNodeIDs(self):
        self.canvas.toggleNodeIDs()

    def onToggleEdgeWeights(self):
        self.canvas.toggleEdgeWeights()

    def onSearchAlgorithm(self, algo):
        self.currentAlgo = algo

    def onStartSearch(self):
        start_id = self.startEdit.text()
        end_id = self.endEdit.text()
        # ...existing code...
        search_order, path_nodes, total_cost = GraphAlgorithms.runSearch(
            self.graph_data, self.currentAlgo, start_id, end_id
        )
        self.resultTable.setRowCount(0)
        for i, node in enumerate(search_order):
            self.resultTable.insertRow(i)
            self.resultTable.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.resultTable.setItem(i, 1, QTableWidgetItem(str(node)))
        self.infoLabel.setText(f"已探索节点: {len(search_order)} | 路径总权重: {total_cost}")
        self.canvas.updateSearchVisualization(search_order, path_nodes)
