from src.Graph import Graph


def createGraph():
    G = Graph()
    n = 0
    m = 0

    for i in range(-1, 14):
        G.addNode(i)
        n += 1
    G.addNode(15)
    n += 1

    # connected component 1
    G.addEdge(1, 2)
    G.addEdge(2, 3)
    G.addEdge(3, 4)
    G.addEdge(4, 5)
    G.addEdge(3, 5)
    m += 5

    # 2
    G.addEdge(6, 7)
    G.addEdge(7, 8)
    G.addEdge(6, 8)
    m += 3

    # 3
    G.addEdge(0, -1)
    m += 1

    # 4
    G.addEdge(10, 11)
    G.addEdge(11, 12)
    G.addEdge(12, 13)
    G.addEdge(10, 13)
    m += 4

    return G, n, m


def readGraphEdgeList(path):
    return Graph(path, Graph.READ_MOD_EDGE_LIST)


def readGraphMetis(path):
    return Graph(path, Graph.READ_MOD_METIS)
