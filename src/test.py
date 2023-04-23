from Graph import Graph
import networkx as nx
from shortestPaths import single_source_shortest_path
from shortestPaths import all_pair_shortest_path
from shortestPaths import all_pair_shortest_path_parallel
import timeit



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

# test correctness by comparing distances for a single node id
network_file = "../data/out.ucidata-zachary."
G = Graph(network_file, Graph.READ_MOD_EDGE_LIST)
nxG = nx.read_edgelist(network_file,comments="%")

id = 2 # node-ID for testing

## single source
dist = single_source_shortest_path(G,id)
dist_nx = nx.single_target_shortest_path_length(nxG, str(id))

for node in dist_nx:
    node_id, d = node
    assert(dist[int(node_id)] == d)

## all pairs
dist_all = all_pair_shortest_path_parallel(G)[id]
dist_all_nx = dict(nx.all_pairs_shortest_path_length(nxG))[str(id)]

for node in dist_all_nx:
    assert(dist_all[int(node_id)] == dist_all_nx[node_id])

# test performance 
network_file ="../data/bio-celegans.mtx"
G = Graph(network_file, Graph.READ_MOD_EDGE_LIST)
nxG = nx.read_edgelist(network_file,comments="%")
print(nxG)

num_iterations = 10
time_all_pairs = timeit.timeit(lambda: all_pair_shortest_path(G), number=num_iterations)
print("all_pair_shortest_path: ", time_all_pairs)
time_all_pairs_par = timeit.timeit(lambda: all_pair_shortest_path_parallel(G), number=num_iterations)
print("all_pair_shortest_path_parallel: ", time_all_pairs_par)
time_all_pairs_lengths = timeit.timeit(lambda: nx.all_pairs_shortest_path_length(nxG), number=num_iterations)
print("networkx - all_pair_shortest_path_length: ", time_all_pairs_lengths)