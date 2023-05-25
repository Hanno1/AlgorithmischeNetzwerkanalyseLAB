import networkx as nx

import HelperClass
import src.networkCentrality.myCentrality as Nc


G, _, _ = HelperClass.create_graph()
G_ = nx.Graph()

cent = Nc.OwnCentrality(G)
print(cent.single_node_centrality(4))
print(cent.all_nodes_centrality(10))
print(cent.most_central_node())
print(cent.k_central_nodes(3))
