from src.Graph import Graph
from collections import deque

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
    deg_dict = {}
    node_to_deg = {}
    for i in G.internal_ids_node_ids:
        deg = len(G.edges[i])
        node_to_deg[i] = deg
        if deg in deg_dict:
            deg_dict[deg].add(i)
        else:
            deg_dict[deg] = set([i])
    removed = set()
    while deg_dict:
        x = min(deg_dict.keys())
        nodes_deg_x = deque(deg_dict[x])
        while nodes_deg_x:
            node = nodes_deg_x.pop()
            removed.add(node)
            neighbors = set(G.get_internal_neighbors(node))-removed
            # iterate over all neighbors of "removed" node, fix their degrees
            for n in neighbors:
                neighb_deg = node_to_deg[n]
                deg_dict[neighb_deg].remove(n)
                if len(deg_dict[neighb_deg]) == 0:
                    del deg_dict[neighb_deg]
                # if the degree smaller than degeneracy, add it to queue
                if neighb_deg <= x:
                    nodes_deg_x.append(n)
                else:
                    node_to_deg[n] = neighb_deg-1
                    if neighb_deg-1 in deg_dict:
                        deg_dict[neighb_deg-1].add(n)
                    else:
                        deg_dict[neighb_deg-1] = set([n])
        del deg_dict[x]
    return x

    
