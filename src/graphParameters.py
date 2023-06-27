from src.Graph import Graph
from collections import deque, defaultdict
from itertools import combinations
from queue import PriorityQueue


def density(G: Graph):
    """
    :param G: Graph
    returns: density of a Graph G: float

    """
    if G.n <= 1:
        return 0.0
    return (2*G.m)/(G.n*(G.n-1))


def max_degree(G: Graph):
    """
    :param G: Graph
    returns: maximum degree of a Graph G: int

    """
    if G.n == 0:
        return None 
    return max(len(G.edges[node]) for node in G.internal_ids_node_ids.keys())


def h_index(G: Graph):
    """
    :param G: Graph
        calculates a maximum value h such that the given Graph has at least 
        h nodes that have at least degree h
    returns: returns the h-index of a Graph G: int

    """
    degree_counts = defaultdict(int) # default value = 0
    for node in G.internal_ids_node_ids.keys():
        degree_counts[len(G.edges[node])] += 1
    h_id = 0 
    node_count = 0
    # go from maximum possible degree/h-index to lowest 
    # instead of sorting the dictionary keys
    for deg in range(G.n, -1, -1): 
        node_count += degree_counts[deg]
        if node_count >= deg:
            h_id = deg
            break
    return h_id


def degeneracy(G: Graph):
    """
    :param G: Graph
        calculates the degeneracy d(G) of a Graph G: maximum of the minimal degrees in all Subgraphs of G 
        calculates the degeneracy ordering of a Graph: Every node of rank k has max d(G) neighbors in the 
        subgraph consisting of nodes with rank r>k
    returns: 
        degeneracy: int
        degeneracy_ordering: list of G

    """
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

        if deg > degeneracy:
            degeneracy = deg

        degeneracy_order.append(G.internal_ids_node_ids[node])

        del node_to_deg[node]
            
        neighbors = set(G.get_internal_neighbors(node))
        for n in neighbors:
            if n in node_to_deg.keys():
                node_to_deg[n] -= 1
                degree_queue.put((node_to_deg[n], n))

    return degeneracy, degeneracy_order


class BucketQueue():
    def __init__(self,max_prio):
        self.buckets = defaultdict(set)
        self.pointer = max_prio
        self.max_prio = max_prio

    def update_pointer(self,start = 0):
        for i in range(start,self.max_prio):
            if self.buckets[i]:
                self.pointer = i
                self.isempty = False
                return
        self.pointer = self.max_prio

    def put(self, x):
        prio, node = x
        self.buckets[prio].add(node)
        if prio<self.pointer:
            self.pointer = prio
    
    def empty(self):
        if self.pointer == self.max_prio and not self.buckets[self.max_prio]:
            return True
        return False

    def move_down(self, x):
        prio, node = x
        self.buckets[prio+1].remove(node)
        if prio>=0:
            self.buckets[prio].add(node)
            if self.pointer > prio:
                self.pointer = prio
            return
        elif not len(self.buckets[0]):
                self.update_pointer()

    def get(self):
        e = self.buckets[self.pointer].pop()
        current_pointer = self.pointer
        if len(self.buckets[self.pointer]) == 0:
            self.update_pointer(start=self.pointer)
        return current_pointer,e
            
def degeneracy_bucket(G: Graph):
    if G.n == 0:
        return 0, []
    degree_queue = BucketQueue(max_degree(G))
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

        if deg > degeneracy:
            degeneracy = deg

        degeneracy_order.append(G.internal_ids_node_ids[node])

        del node_to_deg[node]
            
        neighbors = set(G.get_internal_neighbors(node))
        for n in neighbors:
            if n in node_to_deg.keys():
                node_to_deg[n] -= 1
                degree_queue.move_down((node_to_deg[n], n))
    return degeneracy, degeneracy_order


def k_core_decomposition(G:Graph):
    """
    :param G: Graph
        The k-core of a graph G is the maximal subgraph G' of G such that the
        minimum degree of G' is k (note: the 0-core automatically has all nodes)
    returns: 
        dictionary of sets 
            where key: k (of core)
            value: set of nodes that belong to k-core but not to any (x|x<k)-core 
                    the complete k-core is then the union of sets with keys <=k
    """
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
    """
    :param G: Graph
        compute extent, to which Graph exhibits triadic closure. (6*#triangles)/(#pfade der länge 2)
    returns: returns the global clustering coefficient of a Graph G: int [0,1]

    """
    triangles = 0
    triples = 0
    for node in G.internal_ids_node_ids:
        neighbors = list(G.get_internal_neighbors(node))
        k = len(neighbors)
        if k < 2:
            continue
        triples += k * (k-1) // 2 # possible triangles
        triangles += sum(1 for u, v in combinations(neighbors, 2) if v in G.edges[u])
    if triples == 0:
        return 0.0
    return triangles / triples


def local_clustering_coefficient(G: Graph, node):
    """
    :param G: Graph
        compute extent, to which a node neighborhood exhibits triadic closure.
    returns: returns the local clustering coefficient of a node in a Graph G: int [0,1]

    """
    internal_node = G.node_ids_internal_ids[node]
    neighbors = G.get_internal_neighbors(internal_node)
    k = len(neighbors)
    if k <= 1:
        return 0
    edges_neighborhood = sum(1 for u, v in combinations(neighbors, 2) if v in G.edges[u])
    return edges_neighborhood / ((k * (k - 1)) / 2)