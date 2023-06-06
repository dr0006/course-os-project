from collections import defaultdict


class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.vertices = vertices

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def is_cyclic_util(self, v, visited, rec_stack):
        visited[v] = True
        rec_stack[v] = True

        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                if self.is_cyclic_util(neighbor, visited, rec_stack):
                    return True
            elif rec_stack[neighbor]:
                return True

        rec_stack[v] = False
        return False

    def is_cyclic(self):
        visited = [False] * self.vertices
        rec_stack = [False] * self.vertices

        for node in range(self.vertices):
            if not visited[node]:
                if self.is_cyclic_util(node, visited, rec_stack):
                    return True

        return False


def detect_deadlock(needs, allocated):
    n = len(needs)
    m = len(needs[0])

    # 统计每种资源的剩余数量
    avail = [0] * m
    for i in range(n):
        for j in range(m):
            avail[j] += allocated[i][j]

    # 将矩阵转化为图
    graph = Graph(n + m + 2)
    source = n + m
    sink = n + m + 1

    for j in range(m):
        for i in range(n):
            if needs[i][j] > 0 and allocated[i][j] == 0:
                graph.add_edge(source, n+j)
                graph.add_edge(n+j, i)
                graph.add_edge(i, n+j)

    for i in range(n):
        graph.add_edge(i, sink)

    return graph.is_cyclic()


# 测试代码
if __name__ == '__main__':
    # Test Case 1
    needs = [[2, 1, 0], [1, 0, 3], [1, 0, 2]]
    allocated = [[0, 0, 1], [3, 2, 0], [2, 1, 0]]
    if detect_deadlock(needs, allocated):
        print("有死锁")
    else:
        print("无死锁")

    # Test Case 2
    needs = [[1, 2, 1], [1, 1, 1], [2, 1, 2]]
    allocated = [[1, 0, 0], [1, 0, 1], [1, 0, 1]]
    if detect_deadlock(needs, allocated):
        print("有死锁")
    else:
        print("无死锁")

    # Test Case 3
    needs = [[2, 1, 0], [1, 0, 3], [1, 0, 2]]
    allocated = [[1, 1, 0], [3, 2, 0], [2, 1, 1]]
    if detect_deadlock(needs, allocated):
        print("有死锁")
    else:
        print("无死锁")