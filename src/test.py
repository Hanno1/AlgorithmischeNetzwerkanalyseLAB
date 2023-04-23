from Graph import Graph
import shortestPaths as sp

# G = Graph("test.txt", Graph.READ_MOD_METIS)
G = Graph()

G.addNode(1)
G.addNode(2)
G.addNode(3)
G.addEdge(1, 3)
G.addEdge(4, 8)
G.addEdge(1, 4)
G.addEdge(2, 8)
G.addEdge(2, 3)

print(sp.bidrSearch(G,8,1))

G.removeNode(4)

print(sp.bidrSearch(G,8,1))
# G.saveGraphAsMetis("metisTest")

# print(G.getNodeDegree(3))

# G.printNodes()
# G.printEdges()
