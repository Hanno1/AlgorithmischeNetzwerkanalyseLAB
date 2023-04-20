from Graph import Graph


# G = Graph("test.txt", Graph.READ_MOD_METIS)
G = Graph()

G.addNode(1)
G.addNode(2)
G.addNode(3)
G.addEdge(2, 3)
G.addEdge(1, 3)
G.addEdge(4, 8)

# G.saveGraphAsMetis("metisTest")

# print(G.getNodeDegree(3))

# G.printNodes()
# G.printEdges()
