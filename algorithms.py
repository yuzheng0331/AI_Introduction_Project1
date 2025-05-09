from collections import deque
import heapq
import math

class GraphAlgorithms:
    @staticmethod
    def runSearch(graph_data, algo, start_id, end_id):
        if algo == "DFS":
            return GraphAlgorithms.dfs(graph_data, start_id, end_id)
        elif algo == "BFS":
            return GraphAlgorithms.bfs(graph_data, start_id, end_id)
        elif algo == "A*":
            return GraphAlgorithms.a_star(graph_data, start_id, end_id)
        elif algo == "Dijkstra":
            return GraphAlgorithms.dijkstra(graph_data, start_id, end_id)
        return [], [], 0

    @staticmethod
    def dfs(graph_data, start_id, end_id):
        visited = []  # 记录所有访问过的节点
        min_cost = float('infinity')  # 最小权重
        shortest_path = []  # 最短路径

        stack = [(start_id, [start_id], 0, {start_id})]  # (当前节点, 路径, 权重, 当前路径中的节点集合)

        while stack:
            current, route, cost, path_visited = stack.pop()

            # 记录当前节点为已访问
            if current not in visited:
                visited.append(current)

            # 如果到达目标节点，更新最短路径
            if current == end_id:
                if cost < min_cost:
                    min_cost = cost
                    shortest_path = route
            else:
                # 探索邻居节点
                for nx, w in GraphAlgorithms.getNeighbors(graph_data, current):
                    if nx not in path_visited:  # 避免当前路径中的环路
                        new_path_visited = path_visited.copy()
                        new_path_visited.add(nx)
                        stack.append((nx, route + [nx], cost + w, new_path_visited))

        # 返回访问过的节点列表、最短路径和最小权重
        if shortest_path:
            return visited, shortest_path, min_cost
        return visited, [], 0

    @staticmethod
    def bfs(graph_data, start_id, end_id):
        visited = []  # 记录所有访问过的节点
        min_cost = float('infinity')  # 最小权重
        shortest_path = []  # 最短路径

        queue = deque([(start_id, [start_id], 0)])
        while queue:
            current, route, cost = queue.popleft()

            if current not in visited:
                visited.append(current)

                # 如果到达目标节点，更新最短路径
                if current == end_id:
                    if cost < min_cost:
                        min_cost = cost
                        shortest_path = route
                # 继续探索即使已经找到目标节点
                for nx, w in GraphAlgorithms.getNeighbors(graph_data, current):
                    if nx not in visited:
                        queue.append((nx, route + [nx], cost + w))

        # 返回访问过的节点列表、最短路径和最小权重
        if shortest_path:
            return visited, shortest_path, min_cost
        return visited, [], 0

    @staticmethod
    def dijkstra(graph_data, start_id, end_id):
        visited = []
        dist = {n["id"]: math.inf for n in graph_data["nodes"]}
        dist[start_id] = 0
        prev = {}
        pq = [(0, start_id)]
        while pq:
            current_dist, current = heapq.heappop(pq)
            if current not in visited:
                visited.append(current)
                if current == end_id:
                    route = GraphAlgorithms.reconstructPath(prev, start_id, end_id)
                    return visited, route, current_dist
                for nx, w in GraphAlgorithms.getNeighbors(graph_data, current):
                    new_dist = current_dist + w
                    if new_dist < dist[nx]:
                        dist[nx] = new_dist
                        prev[nx] = current
                        heapq.heappush(pq, (new_dist, nx))
        return visited, [], 0

    @staticmethod
    def a_star(graph_data, start_id, end_id):
        visited = []
        dist = {n["id"]: math.inf for n in graph_data["nodes"]}
        dist[start_id] = 0
        prev = {}
        def heuristic(a, b):
            nodeA = GraphAlgorithms.getNode(graph_data, a)
            nodeB = GraphAlgorithms.getNode(graph_data, b)
            if nodeA and nodeB:
                return math.hypot(nodeA["x"] - nodeB["x"], nodeA["y"] - nodeB["y"])
            return 0
        open_set = [(0, start_id)]
        while open_set:
            _, current = heapq.heappop(open_set)
            if current not in visited:
                visited.append(current)
                if current == end_id:
                    route = GraphAlgorithms.reconstructPath(prev, start_id, end_id)
                    return visited, route, dist[end_id]
                for nx, w in GraphAlgorithms.getNeighbors(graph_data, current):
                    g_cost = dist[current] + w
                    if g_cost < dist[nx]:
                        dist[nx] = g_cost
                        f_cost = g_cost + heuristic(nx, end_id)
                        prev[nx] = current
                        heapq.heappush(open_set, (f_cost, nx))
        return visited, [], 0

    @staticmethod
    def getNeighbors(graph_data, node_id):
        neighbors = []
        for e in graph_data["edges"]:
            if e["start"] == node_id:
                neighbors.append((e["end"], e["weight"]))
            if not e["directed"] and e["end"] == node_id:
                neighbors.append((e["start"], e["weight"]))
        return neighbors

    @staticmethod
    def getNode(graph_data, node_id):
        for n in graph_data["nodes"]:
            if n["id"] == node_id:
                return n
        return None

    @staticmethod
    def reconstructPath(prev, start, end):
        path = []
        current = end
        while current in prev:
            path.append(current)
            current = prev[current]
        if current == start:
            path.append(start)
            path.reverse()
            return path
        return []
