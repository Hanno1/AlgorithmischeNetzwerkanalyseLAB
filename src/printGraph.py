import networkx as nx
import matplotlib.pyplot as plt
from src.Graph import Graph


def draw_graph(G: Graph):
    networkxG = nx.Graph()

    nodes = G.get_nodes()
    mapping = G.node_ids_internal_ids
    for node in nodes:
        networkxG.add_node(mapping[node])

    edges = G.edges
    for key in edges:
        value = edges[key]
        for val in value:
            networkxG.add_edge(key, val)

    nx.draw(networkxG)
    plt.show()
