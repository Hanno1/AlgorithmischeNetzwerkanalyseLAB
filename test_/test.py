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
import sys
sys.setrecursionlimit(3000)
from networkx.algorithms.distance_measures import diameter

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
    return G ,newG

G = Graph()
"""
for i in range(0,40):
    G.add_node(i)

G.add_edge(38,16)
G.add_edge(16,43)
G.add_edge(43,23)
G.add_edge(23,15)
G.add_edge(45,15)
G.add_edge(15,29)
G.add_edge(29,5)
G.add_edge(29,31)
G.add_edge(29,35)
G.add_edge(5,49)
G.add_edge(31,17)
G.add_edge(31,36)
G.add_edge(35,34)
G.add_edge(35,12)
G.add_edge(34,36)
G.add_edge(34,41)
G.add_edge(49,22)
G.add_edge(49,6)
G.add_edge(49,21)
G.add_edge(49,1)
G.add_edge(17,25)
G.add_edge(12,21)
G.add_edge(12,8)
G.add_edge(12,2)
G.add_edge(41,13)
G.add_edge(41,19)
G.add_edge(12,39)
G.add_edge(21,39)
G.add_edge(21,24)
G.add_edge(24,44)
G.add_edge(22,39)
G.add_edge(22,30)
G.add_edge(39,42)
G.add_edge(6,42)
G.add_edge(42,25)
G.add_edge(25,13)
G.add_edge(1,8)
G.add_edge(8,19)
G.add_edge(19,2)
G.add_edge(2,26)
G.add_edge(19,3)
G.add_edge(8,20)
G.add_edge(20,33)
G.add_edge(33,10)
G.add_edge(33,37)
G.add_edge(37,14)
G.add_edge(14,32)
G.add_edge(14,47)
G.add_edge(47,28)
G.add_edge(30,40)
G.add_edge(40,27)

G.remove_node(9)
G.remove_node(0)
G.remove_node(7)
G.remove_node(4)
G.remove_node(18)
G.remove_node(11)

G_nx = nx.Graph()
G_nx.add_edge(38,16)
G_nx.add_edge(16,43)
G_nx.add_edge(43,23)
G_nx.add_edge(23,15)
G_nx.add_edge(45,15)
G_nx.add_edge(15,29)
G_nx.add_edge(29,5)
G_nx.add_edge(29,31)
G_nx.add_edge(29,35)
G_nx.add_edge(5,49)
G_nx.add_edge(31,17)
G_nx.add_edge(31,36)
G_nx.add_edge(35,34)
G_nx.add_edge(35,12)
G_nx.add_edge(34,36)
G_nx.add_edge(34,41)
G_nx.add_edge(49,22)
G_nx.add_edge(49,6)
G_nx.add_edge(49,21)
G_nx.add_edge(49,1)
G_nx.add_edge(17,25)
G_nx.add_edge(12,21)
G_nx.add_edge(12,8)
G_nx.add_edge(12,2)
G_nx.add_edge(41,13)
G_nx.add_edge(41,19)
G_nx.add_edge(12,39)
G_nx.add_edge(21,39)
G_nx.add_edge(21,24)
G_nx.add_edge(24,44)
G_nx.add_edge(22,39)
G_nx.add_edge(22,30)
G_nx.add_edge(39,42)
G_nx.add_edge(6,42)
G_nx.add_edge(42,25)
G_nx.add_edge(25,13)
G_nx.add_edge(1,8)
G_nx.add_edge(8,19)
G_nx.add_edge(19,2)
G_nx.add_edge(2,26)
G_nx.add_edge(19,3)
G_nx.add_edge(8,20)
G_nx.add_edge(20,33)
G_nx.add_edge(33,10)
G_nx.add_edge(33,37)
G_nx.add_edge(37,14)
G_nx.add_edge(14,32)
G_nx.add_edge(14,47)
G_nx.add_edge(47,28)
G_nx.add_edge(30,40)
G_nx.add_edge(40,27)

print("dia_nx: ",nx.diameter(G_nx))
# Number 0
#G.read_graph_metis("E:/GitHub/AlgorithmischeNetzwerkanalyseLAB/networks/case1.txt")
#G, newG = generate_and_translate_graph(10,10)
#G.save_graph_metis("E:/GitHub/AlgorithmischeNetzwerkanalyseLAB/networks/case1")
draw_graph(G,label_on=True,internal_ids=True)
for i in tqdm(range(1000)):
    dia_opt = sp.diameter_opt(G, 2)
    dia = sp.diameter(G)
    #print("dia_opt: ", dia_opt)
    #print("dia: ", dia)
    if dia-dia_opt != 0:
        print("dia_opt: ",dia_opt)
        print("dia: ",dia)
        break

"""

num_repeat = 2
num_iterations = 2

SpeedUP_List_global = []
t = 2
for j in range(1,5000,200):
    SpeedUP_List = []
    for i in tqdm(range(1,10)):
        G, G_nx = generate_and_translate_graph(10*j, 10*j)
        GNX = G_nx.subgraph(max(nx.connected_components(G_nx), key=len)).copy()

        try:
            dia = sp.diameter(G)
            dia_opt = sp.diameter_opt(G, t)
            dia_nx = nx.diameter(GNX)

            time_diameter_nx = timeit.repeat(lambda: nx.diameter(GNX), time.process_time, repeat=num_repeat,
                                          number=num_iterations)
            time_diameter = timeit.repeat(lambda: sp.diameter(G), time.process_time, repeat=num_repeat,
                                          number=num_iterations)
            time_diameter_opt = timeit.repeat(lambda: sp.diameter_opt(G, t), time.process_time, repeat=num_repeat,
                                              number=num_iterations)
            SpeedUP = [time_diameter_nx[i] / time_diameter_opt[i] for i in range(len(time_diameter_opt))]


            if dia_nx-dia_opt != 0:
                print("dia: ",dia_nx)
                print("dia_opt: ", dia_opt)
                print("dia_opt falsch")
                #draw_graph(G,label_on=True,internal_ids=True)
                #G.save_graph_metis("E:/GitHub/AlgorithmischeNetzwerkanalyseLAB/networks/case1")
                break
            else:
                SpeedUP_List.append(Average(SpeedUP) - 1)
        except Exception as ex:
            draw_graph(G, label_on=True, internal_ids=True)
            G.save_graph_metis("E:/GitHub/AlgorithmischeNetzwerkanalyseLAB/networks/case1")
            print(ex)
            print("Fehler")
    SpeedUP_List_global.append(Average(SpeedUP_List))

x = np.arange(1,50000, 2000)
y = np.array(SpeedUP_List_global)
print(x.shape)
print(y.shape)
plt.scatter(x,y)
plt.show()

"""
    #print("time_diameter_opt: ", Average(time_diameter_opt))
    #print("time_diameter: ", Average(time_diameter))
    #print("SpeedUp: ", Average(SpeedUP))

#x = np.arange(1,100, 1)
#y = np.array(SpeedUP_List)
#plt.scatter(x,y)
#plt.show()
"""