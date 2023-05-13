import time

from src.Graph import Graph
#from src.printGraph import draw_graph
import src.shortestPaths as sp


G = Graph()

G.add_edge(0,1)
G.add_edge(1,2)
G.add_edge(0,3)
G.add_edge(3,4)

#G.add_edge(0,2)
#G.add_edge(1,3)
#G.add_edge(0,1)
#G.add_edge(2,3)
#G.add_edge(3,4)
#G.add_edge(3,5)
#G.add_edge(4,6)
#G.add_edge(5,6)
#G.add_edge(6,7)
#G.add_edge(8,6)

#G.add_edge(1,4)
#G.add_edge(4,2)
#G.add_edge(4,5)
#G.add_edge(4,6)
#G.add_edge(4,3)
#G.add_edge(4,7)
#G.add_edge(2,5)
#G.add_edge(5,15)
#G.add_edge(5,6)
#G.add_edge(6,7)
#G.add_edge(6,3)
#G.add_edge(6,13)
#G.add_edge(6,14)
#G.add_edge(3,11)
#G.add_edge(3,8)
#G.add_edge(15,16)
#G.add_edge(14,10)
#G.add_edge(14,12)
#G.add_edge(12,11)
#G.add_edge(12,10)
#G.add_edge(12,9)
#G.add_edge(9,8)
#G.add_edge(13,8)






#G.add_edge(0,1)
#G.add_edge(1,2)
#G.add_edge(0,2)
#G.add_edge(2,3)
#G.add_edge(3,4)

print(sp.all_pairs_shortest_path_opt(G,1))
#print(sp.all_pairs_shortest_path(G))

#for i in sp.find_cut_nodes(G):
#    print(G.internal_ids_node_ids[i])
#print("--")
#same_distance = sp.not_to_visit_neighbors_subset_nodes(G)[1]
#node_not_to_visit = sp.not_to_visit_neighbors_subset_nodes(G)[0]
#for i in sp.not_to_visit_neighbors_subset_nodes_2(G)[0]:
#    print(G.internal_ids_node_ids[i])

#print(no_start_nodes)
#print(same_distance)
#print(node_not_to_visit)
#print(sp.single_source_shortest_path(G,0))
#print(sp.single_source_shortest_path_opt(G,0,node_not_to_visit,same_distance))
#draw_graph(G,label_on=True)
#sp.find_cut_nodes(G)
#sp.all_pairs_shortest_path_opt(G,node_not_to_visit,same_distance,no_start_nodes)
