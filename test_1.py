import unittest
import math
from algorithms import GraphAlgorithms


class TestAStarAlgorithm(unittest.TestCase):
    def test_simple_path(self):
        """测试在简单图中寻找路径"""
        graph_data = {
            "nodes": [
                {"id": "A", "x": 0, "y": 0},
                {"id": "B", "x": 1, "y": 0},
                {"id": "C", "x": 2, "y": 0}
            ],
            "edges": [
                {"start": "A", "end": "B", "weight": 1, "directed": False},
                {"start": "B", "end": "C", "weight": 1, "directed": False}
            ]
        }

        visited, path, cost = GraphAlgorithms.a_star(graph_data, "A", "C")
        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 2)
        self.assertTrue(all(node in visited for node in ["A", "B", "C"]))

    def test_unreachable_end(self):
        """测试终点不可达的情况"""
        graph_data = {
            "nodes": [
                {"id": "A", "x": 0, "y": 0},
                {"id": "B", "x": 1, "y": 0},
                {"id": "C", "x": 2, "y": 0}
            ],
            "edges": [
                {"start": "A", "end": "B", "weight": 1, "directed": False}
            ]
        }

        visited, path, cost = GraphAlgorithms.a_star(graph_data, "A", "C")
        self.assertEqual(path, [])
        self.assertEqual(cost, 0)
        self.assertNotIn("C", visited)

    def test_start_is_end(self):
        """测试起点即为终点的情况"""
        graph_data = {
            "nodes": [
                {"id": "A", "x": 0, "y": 0},
                {"id": "B", "x": 1, "y": 0}
            ],
            "edges": [
                {"start": "A", "end": "B", "weight": 1, "directed": False}
            ]
        }

        visited, path, cost = GraphAlgorithms.a_star(graph_data, "A", "A")
        self.assertEqual(path, ["A"])
        self.assertEqual(cost, 0)

    def test_multiple_paths(self):
        """测试有多条路径时是否找到最短路径"""
        graph_data = {
            "nodes": [
                {"id": "A", "x": 0, "y": 0},
                {"id": "B", "x": 1, "y": 0},
                {"id": "C", "x": 2, "y": 0},
                {"id": "D", "x": 1, "y": 1}
            ],
            "edges": [
                {"start": "A", "end": "B", "weight": 1, "directed": False},
                {"start": "B", "end": "C", "weight": 1, "directed": False},
                {"start": "A", "end": "D", "weight": 1, "directed": False},
                {"start": "D", "end": "C", "weight": 3, "directed": False}
            ]
        }

        visited, path, cost = GraphAlgorithms.a_star(graph_data, "A", "C")
        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 2)

    def test_directed_graph(self):
        """测试在有向图中的路径搜索"""
        graph_data = {
            "nodes": [
                {"id": "A", "x": 0, "y": 0},
                {"id": "B", "x": 1, "y": 0},
                {"id": "C", "x": 2, "y": 0}
            ],
            "edges": [
                {"start": "A", "end": "B", "weight": 1, "directed": True},
                {"start": "B", "end": "C", "weight": 1, "directed": True},
                {"start": "C", "end": "A", "weight": 1, "directed": True}
            ]
        }

        # A到C的路径应该是通过B
        visited, path, cost = GraphAlgorithms.a_star(graph_data, "A", "C")
        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 2)

        # C到B不应该有路径（���非绕一圈）
        visited, path, cost = GraphAlgorithms.a_star(graph_data, "C", "B")
        self.assertEqual(path, ["C", "A", "B"])
        self.assertEqual(cost, 2)


if __name__ == '__main__':
    unittest.main()