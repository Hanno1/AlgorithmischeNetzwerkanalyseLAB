from src.Graph import Graph


def createGraph():
    G = Graph()
    n = 0
    m = 0
    for i in range(10):
        G.addNode(i)
        n += 1
    G.addEdge(1, 2)
    G.addEdge(1, 3)
    G.addEdge(2, 5)
    G.addEdge(9, 7)
    G.addEdge(0, 11)
    n += 1
    G.addEdge(-1, 12)
    n += 2

    G.addEdge(12, -1)
    m += 6
    return G, n, m


def readGraphEdgeList(path):
    return Graph(path, Graph.READ_MOD_EDGE_LIST)


def readGraphMetis(path):
    return Graph(path, Graph.READ_MOD_METIS)
