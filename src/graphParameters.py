from src.Graph import Graph
from collections import deque, defaultdict
from itertools import combinations

def density(G: Graph):
    return (2*G.m)/(G.n*(G.n-1))

def max_degree(G: Graph):
    max_deg = 0 
    for i in G.internal_ids_node_ids:
        deg = len(G.edges[i])
        if max_deg < deg:
            max_deg = deg
    return max_deg

def h_index(G: Graph):
    degrees = []
    for i in G.internal_ids_node_ids:
        degrees.append(len(G.edges[i]))
    degrees.sort(reverse=True)
    h_id = degrees[0]
    for i, deg in enumerate(degrees):
        if i>= h_id:
            return h_id
        if deg < h_id:
            h_id = deg
    return h_id

def degeneracy(G: Graph):
    degree_dict = defaultdict(set) # key: degree d, value: set of nodes that have degree d
    node_to_deg = {} # maps node to its degree
    for node in G.internal_ids_node_ids:
        degree = len(G.edges[node])
        node_to_deg[node] = degree
        degree_dict[degree].add(node)

    nodes_removed = set() # list of removed nodes
    degeneracy_order = []
    while degree_dict:
        x = min(degree_dict.keys())
        nodes_deg_x = deque(degree_dict[x])
        while nodes_deg_x:
            node = nodes_deg_x.pop()
            nodes_removed.add(node)
            degeneracy_order.append(G.internal_ids_node_ids[node])
            neighbors = set(G.get_internal_neighbors(node)) - set(nodes_removed)
            # iterate over all neighbors of "removed" node, fix their degrees
            for n in neighbors:
                if n in nodes_removed: # we want to know if n is already staged for removal
                # <-> "n in nodes_deg_x", but testing this is inefficient
                    continue
                neighb_deg = node_to_deg[n]
                degree_dict[neighb_deg].remove(n)
                if not degree_dict[neighb_deg]:
                    del degree_dict[neighb_deg]
                # if the degree is smaller than degeneracy, add neighbor to queue
                if neighb_deg <= x:
                    nodes_deg_x.append(n)
                    nodes_removed.add(n)
                else: # otherwise register neighbor as member of decremented degree
                    node_to_deg[n] -= 1
                    degree_dict[node_to_deg[n]].add(n)
        del degree_dict[x]
    return x, degeneracy_order

def global_clustering_coefficient(G: Graph):
    triangles = 0
    triples = 0
    for node in G.internal_ids_node_ids:
        neighbors = G.get_internal_neighbors(node)
        k = len(neighbors)
        if k < 2:
            continue
        triples += k * (k-1) / 2
        triangles += sum(1 for u, v in combinations(neighbors, 2) if v in G.edges[u])
    return (triangles / triples)

def local_clustering_coefficient(G: Graph, node):
    internal_node = G.node_ids_internal_ids[node]
    neighbors = G.get_internal_neighbors(internal_node)
    k = len(neighbors)
    edges_neighborhood = sum(1 for u, v in combinations(neighbors, 2) if v in G.edges[u])
    return (edges_neighborhood / ((k * (k-1))/2))