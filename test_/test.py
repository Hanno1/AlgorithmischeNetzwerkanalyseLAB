from src.Graph import Graph
import src.shortestPaths as sp
from src.printGraph import draw_graph
import timeit
import networkx as nx

import os
import sys
import subprocess


# Erstellung eines leeren Graphens
G = Graph()

# Hinzufügen von Knoten
G.add_node("Node1")
G.add_node("Node2")
G.add_node("Node3")
G.add_node(2)

# Hinzufügen von Kanten
G.add_edge("2", "Node3")
G.add_edge("2", "Node1")
G.add_edge("Node1", "Node3")

# Hinzufügen von Kanten und Knoten sind noch unbekannt -> Knoten wird automatisch erstellt
G.add_edge("Node4", "Node5")

# print edges
G.print_edges()

# draw the Graph using networkx
draw_graph(G)
