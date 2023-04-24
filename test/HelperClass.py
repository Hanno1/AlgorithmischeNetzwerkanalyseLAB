from src.Graph import Graph


def createGraph():
    G = Graph()
    n = 0
    m = 0
    for i in range(10):
        G.addNode(i)
        n += 1
    G.addEdge(1, 2)
    G.addEdge(2, 5)
    G.addEdge(9, 7)
    G.addEdge(0, 11)
    n += 1
    G.addEdge(-1, 12)
    n += 2

    G.addEdge(-1, 12)
    m += 5
    return G, n, m
