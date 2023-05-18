import HelperClass
import src.triangleAlgorithms as tri
from src.Graph import Graph as Graph
from src.printGraph import draw_graph
import networkx


G, _, _ = HelperClass.create_graph()

G.add_edge(7, 8)
# G = Graph()
# print(tri.algorithm_trivial(G))
# print(tri.algorithm_chiba_and_nishizeki_dict(G))
# print(tri.algorithm_edge_iterator(G))
print(tri.algorithm_node_iterator_degeneracy_sorting(G))

# G = Graph("test.txt", Graph.READ_MOD_METIS)
