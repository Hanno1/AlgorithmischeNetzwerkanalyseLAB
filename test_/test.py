import math
import time
import timeit
from src.Graph import Graph
from src.printGraph import draw_graph
import src.shortestPaths as sp
from matplotlib import pyplot as plt
from tqdm import tqdm
import numpy as np
import networkx as nx

G = Graph("D:/GitHub/AlgorithmischeNetzwerkanalyseLAB/networks/bio-celegans.mtx",Graph.READ_MOD_EDGE_LIST)

def Average(lst):
    return sum(lst) / len(lst)

def generate_and_translate_graph(n, m, netx=False):
    if m is None:
        newG = nx.complete_graph(n)
    elif m == 0:
        newG = nx.empty_graph(n)
    else:
        newG = nx.dense_gnm_random_graph(n, m)
    if netx:
        return newG
    nodes = nx.nodes(newG)
    G = Graph()
    for node in nodes:
        G.add_node(node)
    edges = nx.edges(newG)
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    return G

G = Graph()
# Number 0
G.read_graph_metis("D:/GitHub/AlgorithmischeNetzwerkanalyseLAB/networks/case1.txt")
draw_graph(G,label_on=True,internal_ids=True)
for i in range(1000):
    print(sp.diameter_opt(G, 2))


num_repeat = 2
num_iterations = 2

node_degrees = []
for node in G.get_nodes():
    node_degrees.append(G.get_node_degree(node))

max_degree = max(node_degrees)
Average_degree = Average(node_degrees)
print("max-degree: ", max_degree)
print("Average_degree: ", Average_degree)


SpeedUP_List = []
t = 4
for i in tqdm(range(1,100)):
    G = generate_and_translate_graph(100,100)
    try:
        time_diameter = timeit.repeat(lambda: sp.diameter(G), time.process_time, repeat=num_repeat,
                                      number=num_iterations)
        time_diameter_opt = timeit.repeat(lambda: sp.diameter_opt(G, t), time.process_time, repeat=num_repeat,
                                          number=num_iterations)
        SpeedUP = [time_diameter[i] / time_diameter_opt[i] for i in range(len(time_diameter_opt))]
        SpeedUP_List.append(Average(SpeedUP) - 1)
    except Exception as ex:
        G.save_graph_metis("D:/GitHub/AlgorithmischeNetzwerkanalyseLAB/networks/case1")
        print(sp.diameter(G))
        print(ex)
        print("Fehler")


    #print("time_diameter_opt: ", Average(time_diameter_opt))
    #print("time_diameter: ", Average(time_diameter))
    #print("SpeedUp: ", Average(SpeedUP))

#x = np.arange(1,100, 1)
#y = np.array(SpeedUP_List)
#plt.scatter(x,y)
#plt.show()
