import time

from src.Graph import Graph
from src.printGraph import draw_graph
import src.shortestPaths as sp


G = Graph()

G.add_edge(0,2)
G.add_edge(1,3)
G.add_edge(0,1)
G.add_edge(2,3)
G.add_edge(3,4)
G.add_edge(3,5)
G.add_edge(4,6)
G.add_edge(5,6)

#G.add_edge(0,1)
#G.add_edge(1,2)
#G.add_edge(0,2)
#G.add_edge(2,3)
#G.add_edge(3,4)

draw_graph(G)
sp.find_cut_nodes(G,0,0)
