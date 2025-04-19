import heapq

def dijkstra(graph, start):
    """
    使用Dijkstra算法计算从起始节点到所有其他节点的最短路径
    
    参数:
        graph: 图的邻接表表示，格式为 {node: {neighbor: distance, ...}, ...}
        start: 起始节点
        
    返回:
        distances: 从起始节点到每个节点的最短距离
        paths: 从起始节点到每个节点的最短路径
    """
    # 初始化距离字典和路径字典
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    paths = {node: [] for node in graph}
    paths[start] = [start]
    
    # 优先队列，用于选择当前最小距离的节点
    priority_queue = [(0, start)]
    
    while priority_queue:
        # 获取当前最小距离的节点
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # 如果找到的距离大于已知的距离，则跳过
        if current_distance > distances[current_node]:
            continue
        
        # 检查当前节点的所有邻居
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            # 如果找到了更短的路径
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                paths[neighbor] = paths[current_node] + [neighbor]
                heapq.heappush(priority_queue, (distance, neighbor))
                
    return distances, paths

# 示例
if __name__ == "__main__":
    # 创建图（邻接表表示）
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 5, 'C': 1}
    }
    
    # 计算从节点'A'到所有其他节点的最短路径
    distances, paths = dijkstra(graph, 'A')
    
    # 打印结果
    print("从节点'A'到各节点的最短距离:")
    for node, distance in distances.items():
        print(f"到{node}: {distance}")
    
    print("\n从节点'A'到各节点的最短路径:")
    for node, path in paths.items():
        print(f"到{node}: {' -> '.join(path)}")
