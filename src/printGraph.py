import networkx as nx
import matplotlib.pyplot as plt
from src.Graph import Graph


def draw_graph(G: Graph, label_on=False, internal_ids=False):
    networkxG = nx.Graph()

    nodes = G.get_nodes()
    mapping = G.node_ids_internal_ids
    for node in nodes:
        networkxG.add_node(mapping[node], key=node)

    edges = G.edges
    for key in edges:
        value = edges[key]
        for val in value:
            networkxG.add_edge(key, val)

    if not internal_ids:
        mapping = G.internal_ids_node_ids
        networkxG = nx.relabel_nodes(networkxG, mapping)

    nx.draw(networkxG, with_labels=label_on)
    plt.show()
