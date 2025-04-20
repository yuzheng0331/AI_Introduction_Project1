from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange, QTableWidgetSelectionRange, \
    QFrame
# ...existing code...
from PyQt5.QtCore import Qt, QTimer
from canvas import GraphCanvas
from readwrite import GraphIO
from algorithms import GraphAlgorithms

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.node_add_mode_active = False
        self.edge_add_mode_active = False
        self.edge_add_directed = False
        self.node_ids_visible = True
        self.edge_weights_visible = True
        self.active_btn_style = "background-color: #4CAF50; color: white;"
        self.inactive_btn_style = ""
        self.visualization_timer = None
        self.search_cost = None
        self.total_steps = None
        self.current_step_index = None
        self.full_path_nodes = None
        self.full_search_order = None
        self.setWindowTitle("可视化最短路径演示")
        self.resize(1920, 1080)
        self.graph_data = {"nodes": [], "edges": []}
        self.initUI()
        self.canvas.graphDataChanged.connect(self.onGraphDataChanged)

    def onGraphDataChanged(self, updated_data):
        self.graph_data = updated_data

    def initUI(self):
        # 顶栏布局
        topWidget = QWidget()
        topLayout = QHBoxLayout()
        self.importBtn = QPushButton("导入文件")
        self.importBtn.clicked.connect(self.onImportFile)
        self.exportBtn = QPushButton("导出文件")
        self.exportBtn.clicked.connect(self.onExportFile)
        self.addNodeBtn = QPushButton("添加节点")
        self.addNodeBtn.clicked.connect(self.onAddNode)
        self.addUndirectedEdgeBtn = QPushButton("添加无向边")
        self.addUndirectedEdgeBtn.clicked.connect(lambda: self.onAddEdge(directed=False))
        self.addDirectedEdgeBtn = QPushButton("添加有向边")
        self.addDirectedEdgeBtn.clicked.connect(lambda: self.onAddEdge(directed=True))
        self.showNodeBtn = QPushButton("展示/隐藏节点ID")
        self.showNodeBtn.clicked.connect(self.onToggleNodeIDs)
        self.showEdgeBtn = QPushButton("展示/隐藏边权重值")
        self.showEdgeBtn.clicked.connect(self.onToggleEdgeWeights)
        # ...existing code...
        topLayout.addWidget(self.importBtn)
        topLayout.addWidget(self.exportBtn)
        topLayout.addWidget(self.addNodeBtn)
        topLayout.addWidget(self.addUndirectedEdgeBtn)
        topLayout.addWidget(self.addDirectedEdgeBtn)
        topLayout.addWidget(self.showNodeBtn)
        topLayout.addWidget(self.showEdgeBtn)

        # 设置初始状态下显示/隐藏按钮的样式
        self.showNodeBtn.setStyleSheet(self.active_btn_style)
        self.showEdgeBtn.setStyleSheet(self.active_btn_style)
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
        self.resultTable.setHorizontalHeaderLabels(["Order", "节点ID"])
        leftLayout.addWidget(self.resultTable)

        # 已探索节点数、路径总权重
        self.infoLabel = QLabel("已探索节点: 0 | 路径总权重: 0")
        # 已探索节点数、路径总权重和执行时间
        self.infoLabel = QLabel("已探索节点: 0 | 路径总权重: 0")
        leftLayout.addWidget(self.infoLabel)
        self.timeLabel = QLabel("执行耗时: 0 ms")
        leftLayout.addWidget(self.timeLabel)
        leftWidget.setLayout(leftLayout)

        # 正中央画布
        self.canvas = GraphCanvas(self)
        # 正中央画布
        self.canvas = GraphCanvas(self)
        # 全局布局
        centralWidget = QWidget()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(topWidget)

        # 添加顶栏与内容之间的水平分割线
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setFrameShadow(QFrame.Sunken)
        mainLayout.addWidget(hLine)

        bodylayout = QHBoxLayout()
        bodylayout.addWidget(leftWidget)

        # 添加左侧栏与画布之间的垂直分割线
        vLine = QFrame()
        vLine.setFrameShape(QFrame.VLine)
        vLine.setFrameShadow(QFrame.Sunken)
        bodylayout.addWidget(vLine)

        bodylayout.addWidget(self.canvas, 5)
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
        self.node_add_mode_active = not self.node_add_mode_active
        self.canvas.enableAddNodeMode(self.node_add_mode_active)

        # 更新按钮样式
        if self.node_add_mode_active:
            self.addNodeBtn.setStyleSheet(self.active_btn_style)
            # 关闭其他模式
            self.edge_add_mode_active = False
            self.addUndirectedEdgeBtn.setStyleSheet(self.inactive_btn_style)
            self.addDirectedEdgeBtn.setStyleSheet(self.inactive_btn_style)
        else:
            self.addNodeBtn.setStyleSheet(self.inactive_btn_style)

    def onAddEdge(self, directed=False):
        # 如果点击的是当前已激活的按钮，则关闭模式
        if self.edge_add_mode_active and self.edge_add_directed == directed:
            self.edge_add_mode_active = False
            if directed:
                self.addDirectedEdgeBtn.setStyleSheet(self.inactive_btn_style)
            else:
                self.addUndirectedEdgeBtn.setStyleSheet(self.inactive_btn_style)
        else:
            # 否则激活该模式
            self.edge_add_mode_active = True
            self.edge_add_directed = directed

            # 更新按钮样式
            if directed:
                self.addDirectedEdgeBtn.setStyleSheet(self.active_btn_style)
                self.addUndirectedEdgeBtn.setStyleSheet(self.inactive_btn_style)
            else:
                self.addUndirectedEdgeBtn.setStyleSheet(self.active_btn_style)
                self.addDirectedEdgeBtn.setStyleSheet(self.inactive_btn_style)

            # 关闭其他模式
            self.node_add_mode_active = False
            self.addNodeBtn.setStyleSheet(self.inactive_btn_style)

        self.canvas.addEdge(directed)

    def onToggleNodeIDs(self):
        self.node_ids_visible = not self.node_ids_visible
        self.canvas.toggleNodeIDs()

        # 更新按钮样式
        if self.node_ids_visible:
            self.showNodeBtn.setStyleSheet(self.active_btn_style)
        else:
            self.showNodeBtn.setStyleSheet(self.inactive_btn_style)

    def onToggleEdgeWeights(self):
        self.edge_weights_visible = not self.edge_weights_visible
        self.canvas.toggleEdgeWeights()

        # 更新按钮样式
        if self.edge_weights_visible:
            self.showEdgeBtn.setStyleSheet(self.active_btn_style)
        else:
            self.showEdgeBtn.setStyleSheet(self.inactive_btn_style)

    def onSearchAlgorithm(self, algo):
        self.currentAlgo = algo

        # 更新所有算法按钮的样式
        self.dfsBtn.setStyleSheet(self.inactive_btn_style)
        self.bfsBtn.setStyleSheet(self.inactive_btn_style)
        self.aStarBtn.setStyleSheet(self.inactive_btn_style)
        self.dijkstraBtn.setStyleSheet(self.inactive_btn_style)

        # 设置当前选中的算法按钮样式
        if algo == "DFS":
            self.dfsBtn.setStyleSheet(self.active_btn_style)
        elif algo == "BFS":
            self.bfsBtn.setStyleSheet(self.active_btn_style)
        elif algo == "A*":
            self.aStarBtn.setStyleSheet(self.active_btn_style)
        elif algo == "Dijkstra":
            self.dijkstraBtn.setStyleSheet(self.active_btn_style)

    def onStartSearch(self):
        start_id = self.startEdit.text()
        end_id = self.endEdit.text()
        # ...existing code...
        import time
        start_time = time.time()
        search_order, path_nodes, total_cost = GraphAlgorithms.runSearch(
            self.graph_data, self.currentAlgo, start_id, end_id
        )
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # 转换为毫秒

        self.resultTable.setRowCount(0)
        # 存储搜索结果和当前索引
        self.full_search_order = search_order
        self.full_path_nodes = path_nodes
        self.current_step_index = 0
        self.total_steps = len(search_order)
        self.search_cost = total_cost

        # 创建定时器用于逐步显示
        self.visualization_timer = QTimer(self)
        self.visualization_timer.timeout.connect(self.showNextSearchStep)

        # 显示基本信息
        self.timeLabel.setText(f"算法: {self.currentAlgo} | 执行耗时: {execution_time:.2f} ms")
        self.infoLabel.setText(f"已探索节点: 0/{self.total_steps} | 路径总权重: {total_cost}")

        # 清空画布上的之前的可视化
        self.canvas.updateSearchVisualization([], [], None)

        # 开始逐步显示
        self.visualization_timer.start(400)

    def showNextSearchStep(self):
        if self.current_step_index < self.total_steps:
            # 添加一行到表格
            i = self.current_step_index
            node = self.full_search_order[i]
            end_id = self.endEdit.text()
            order_item = QTableWidgetItem(str(i + 1))
            node_item = QTableWidgetItem(str(node))
            self.resultTable.insertRow(i)
            if node in self.full_path_nodes:
                order_item.setBackground(Qt.yellow)  # 使用黄色背景高亮
                node_item.setBackground(Qt.yellow)
            self.resultTable.setItem(i, 0, order_item)
            self.resultTable.setItem(i, 1, node_item)

            # 滚动到当前行
            self.resultTable.scrollToItem(self.resultTable.item(i, 0))

            # 更新画布显示到当前步骤
            current_order = self.full_search_order[:i + 1]
            current_path = [n for n in self.full_path_nodes if n in current_order]
            self.canvas.updateSearchVisualization(current_order, current_path, end_id)

            # 更新信息标签
            self.infoLabel.setText(f"已探索节点: {i + 1}/{self.total_steps} | 路径总权重: {self.search_cost}")

            # 递增索引
            self.current_step_index += 1
        else:
            # 全部显示完成，停止定时器
            self.visualization_timer.stop()
