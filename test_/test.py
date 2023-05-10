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
G.add_edge(6,7)
G.add_edge(8,6)


#G.add_edge(0,1)
#G.add_edge(1,2)
#G.add_edge(0,2)
#G.add_edge(2,3)
#G.add_edge(3,4)

no_start_nodes = sp.find_cut_nodes(G)
same_distance = sp.not_to_visit_neighbors_subset_nodes(G)[1]
node_not_to_visit = sp.not_to_visit_neighbors_subset_nodes(G)[0].difference(no_start_nodes)
print(no_start_nodes)
print(same_distance)
print(node_not_to_visit)
print(sp.single_source_shortest_path(G,0))
print(sp.single_source_shortest_path_opt(G,0,node_not_to_visit,same_distance))
#draw_graph(G,label_on=True)
#sp.find_cut_nodes(G)
sp.all_pairs_shortest_path_opt(G,node_not_to_visit,same_distance,no_start_nodes)
