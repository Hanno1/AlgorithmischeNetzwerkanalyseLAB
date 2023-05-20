import networkx as nx

import HelperClass
import src.triangleAlgorithms as tri
from src.Graph import Graph as Graph
from src.printGraph import draw_graph
import networkx


G, _, _ = HelperClass.create_graph()
G_ = nx.Graph()
G.add_edge(7, 8)
for node in G.edges:
    for node2 in G.edges[node]:
        print(node, node2)
        G_.add_edge(node, node2)

# G = Graph()
# print(tri.algorithm_trivial(G))
# print(tri.algorithm_chiba_and_nishizeki_dict(G))
# print(tri.algorithm_edge_iterator(G))
print(tri.algorithm_chiba_and_nishizeki(G))
print(nx.triangles(G_))

# G = Graph("test.txt", Graph.READ_MOD_METIS)
