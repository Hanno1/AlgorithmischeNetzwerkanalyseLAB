from src.Graph import Graph
from collections import deque, defaultdict
from itertools import combinations
from queue import PriorityQueue

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
    degree_queue = PriorityQueue()
    node_to_deg = {} # maps node to its degree
    degeneracy_order = []

    for node in G.internal_ids_node_ids:
        degree = len(G.edges[node])
        node_to_deg[node] = degree
        degree_queue.put((degree, node))

    degeneracy = 0
    while not degree_queue.empty():
        deg, node = degree_queue.get()

        if node not in node_to_deg:
            continue

        degeneracy_order.append(G.internal_ids_node_ids[node])

        del node_to_deg[node]

        if deg > degeneracy:
            degeneracy = deg
            
        neighbors = set(G.get_internal_neighbors(node))
        for n in neighbors:
            if n in node_to_deg.keys():
                node_to_deg[n] -= 1
                degree_queue.put((node_to_deg[n], n))

    return degeneracy, degeneracy_order

def k_core_decomposition(G:Graph):
    _, degeneracy_order = degeneracy(G)
    forward_edges = {}
    for i in range(G.n):
        n = degeneracy_order[i]
        edges = G.get_neighbors(n)
        forward_edges[n] = set(degeneracy_order[i:]) & edges
    L = defaultdict(set) 
    k = 0
    for i in range(G.n):
        n = degeneracy_order[i]
        fe = len(forward_edges[n])
        if fe > k:
            k = fe
        L[k].add(n)
    return L


def global_clustering_coefficient(G: Graph):
    triangles = 0
    triples = 0
    for node in G.internal_ids_node_ids:
        neighbors = list(G.get_internal_neighbors(node))
        k = len(neighbors)
        if k < 2:
            continue
        triples += k * (k-1) // 2
        triangles += sum(1 for u, v in combinations(neighbors, 2) if v in G.edges[u])
    if triples == 0:
        return 0.0
    return (triangles / triples)

def local_clustering_coefficient(G: Graph, node):
    internal_node = G.node_ids_internal_ids[node]
    neighbors = G.get_internal_neighbors(internal_node)
    k = len(neighbors)
    if k == 0:
        return 0
    edges_neighborhood = sum(1 for u, v in combinations(neighbors, 2) if v in G.edges[u])
    return (edges_neighborhood / ((k * (k-1))/2))