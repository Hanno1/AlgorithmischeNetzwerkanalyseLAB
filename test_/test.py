import HelperClass
import src.triangleAlgorithms as tri
from src.printGraph import draw_graph


G, _, _ = HelperClass.create_graph()

G.add_edge(7, 8)
print(tri.algorithm_trivial(G))
