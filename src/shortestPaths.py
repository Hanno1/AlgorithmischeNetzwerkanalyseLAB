import random
from collections import deque
from src.Graph import Graph
import multiprocessing
import src.CustomExceptions as Exc
import math
import random
import numpy as np

__all__ = [
    "single_source_shortest_path",
    "all_pairs_shortest_path",
    "shortest_s_t_path",
    "connected_components"
]


# @lru_cache(maxsize=None)
def single_source_shortest_path(G: Graph, s):
    """
    :param G:
    :param s: name of the Graph node for which shortest paths are computed

    calculates the length of the shortest path from node s to each node in the Graph.

    returns: 
    dictionary where keys are names of all nodes in the Graph and values
    are corresponding distances (int). Non-reachable nodes have distance infinite

    """
    s = str(s)
    if s not in G.node_ids_internal_ids:
        raise Exc.NodeDoesNotExistException(s)
    dist = {}
    for n in G.node_ids_internal_ids:
        dist[n] = math.inf
    dist[s] = 0

    internal_s = G.node_ids_internal_ids[s]
    visited = {internal_s}
    next_level = [internal_s]
    distance = 0

    # traverse each "distance level" seperately, making stack pop operations unnecessary
    while next_level:
        distance += 1
        child_level = []
        for u in next_level:
            for v in G.get_internal_neighbors(u):
                if v not in visited:
                    visited.add(v)
                    child_level.append(v)
                    external_v = G.internal_ids_node_ids[v]
                    dist[external_v] = distance
                    if len(visited) == G.n:
                        return dist
        next_level = child_level
    return dist


def _all_pairs_shortest_path_single(G: Graph):
    dist = {}
    for v in G.node_ids_internal_ids:
        dist[v] = single_source_shortest_path(G, v)
    return dist


def _calc_shortest_paths(node_chunk, G: Graph):
    dist_chunk = {}
    for v in node_chunk:
        dist_chunk[v] = single_source_shortest_path(G, v)
    return dist_chunk


def _all_pairs_shortest_path_parallel(G: Graph, num_processes: int):
    dist = {}
    nodes = list(G.node_ids_internal_ids.keys())
    node_chunks = [nodes[i::num_processes] for i in range(num_processes)]

    # create a process pool and map the node chunks to worker processes
    with multiprocessing.Pool(num_processes) as pool:
        results = []
        for node_chunk in node_chunks:
            result = pool.apply_async(_calc_shortest_paths, args=(node_chunk, G))
            results.append(result)

        # get the results from all processes and combine them into a single dictionary
        for result in results:
            dist_chunk = result.get()
            dist.update(dist_chunk)

    return dist


def all_pairs_shortest_path(G: Graph):
    """
    :param G: Graph
    Calculates the length of the shortest path for each pair of nodes in the Graph.
    Parallelization depending on available cpu cores.

    returns: 
    dictionary of dictionaries where keys are names of all nodes in the Graph and values
    are corresponding distances (int). Non-reachable nodes have distance infinite
    {node_id1: {node_id1: 0, node_id2: dist12, ..., node_idN: dist1N},
    node_id1: {node_id1: dist21, node_id2: 0, ..., node_idN: dist2N},
    ...
    node_idN: {node_id1: distN1, node_id2: distN2, ..., node_idN: 0}}
    """
    num_processes = 3
    #num_processes = multiprocessing.cpu_count()
    if num_processes < 4:
        return _all_pairs_shortest_path_single(G)
    else:
        return _all_pairs_shortest_path_parallel(G, num_processes)


def breadth_first_search(G: Graph, parent: dict, b_parent: dict, queue: deque):
    """
    Breadth-First-Search
    Input:  Graph, Dictionary of the parents of discovered Nodes, Dictionary of discovered Nodes from the other search direction, Queue of Nodes from where to search

    Looking from one active Node, all neighbors of that Node.
    If the Neighbor was never visited, the parent node of that Node is the active node
    New discovered Nodes will be taken in the queue.
    If the active Node was already discovered by the other search direction, the Search has an Interception and will return the active Node as Intersection Node

    Return the node where two directions of search meet. If there is no Interception, it will return -1
    """

    current_node = queue.popleft()
    for node in G.get_internal_neighbors(current_node):
        if node not in parent:
            parent[node] = current_node
            queue.append(node)
        if node in b_parent:
            return node
    return -1


def shortest_s_t_path(G: Graph, s_id, t_id):
    """
    Bidirectional shortest path in G from source s_id to target t_id (bidirectional)
    Input: Graph, Start node, End node

    For both Start- and End node, a queue Nodes that need to be visited will be created
    The short of both Queues will be the active Search Queue

    If both Search-Directions find the same Node, there will be an Intersection
    After that, the Search will stop and the Parent dictionary of both directions will be merged as the Final shortest Path

    If Start node = End node, it will return a length of 0
    If Start node and End node are not connected, it will return a length of inf

    Returns: Paths as List and length of the shortest path
    """

    if str(s_id) not in G.node_ids_internal_ids:
        raise Exc.NodeDoesNotExistException(s_id)
    if str(t_id) not in G.node_ids_internal_ids:
        raise Exc.NodeDoesNotExistException(t_id)

    if s_id == t_id:
        return [str(s_id)], 0

    node_ids = list(G.node_ids_internal_ids.keys())

    s = node_ids.index(str(s_id))
    t = node_ids.index(str(t_id))

    shortest_path = []

    s_queue = deque([s])
    t_queue = deque([t])

    s_parent = dict()
    t_parent = dict()
    s_parent[s] = -1
    t_parent[t] = -1

    while s_queue and t_queue:
        if len(s_queue) <= len(t_queue):
            intersection = breadth_first_search(G, s_parent, t_parent, s_queue)
        else:
            intersection = breadth_first_search(G, t_parent, s_parent, t_queue)
        if intersection != -1:
            i = intersection
            shortest_path.append(G.internal_ids_node_ids[i])
            while i != s:
                shortest_path.append(G.internal_ids_node_ids[s_parent[i]])
                i = s_parent[i]
            shortest_path.reverse()
            i = intersection
            while i != t:
                shortest_path.append(G.internal_ids_node_ids[t_parent[i]])
                i = t_parent[i]
            return shortest_path, len(shortest_path) - 1
    return [], math.inf


def connected_components(G: Graph):
    """
    determines the components the graph is composed of.

    returns: 
    a list of sets, each of which contains the nodes of a disjoint component.

    """
    components = []
    visited = set()

    for i in G.node_ids_internal_ids.keys():
        if i in visited:
            continue

        component = set()
        distances = single_source_shortest_path(G, i)
        for node_id in distances:
            if distances[node_id] < math.inf:
                component.add(node_id)
                visited.add(node_id)
        components.append(component)
    return components

def diameter(G: Graph):
    diameter = -math.inf
    apsp = all_pairs_shortest_path(G)
    for node1 in apsp:
        for node2 in apsp[node1]:
            if apsp[node1][node2] != math.inf and apsp[node1][node2] > diameter:
                diameter = apsp[node1][node2]
    return diameter


def breadth_first_search_tree(G: Graph,s,disc,low,time,parent,cut_nodes):
    """
    :param G:

    Finds the Nodes that when they get deleted will create two new connected components.
    It's using the Tarjan’s Algorithm and therefore will create an BFS-Tree

    :return: set of Cut-Nodes
    """

    low[s] = time;disc[s] = time
    time = time+1
    children = 0

    for node in G.get_internal_neighbors(s):
        if node not in disc:
            children = children+1
            parent[node] = s
            breadth_first_search_tree(G,node,disc,low,time,parent,cut_nodes)
            low[s] = min(low[s],low[node])

            if s not in parent and children >1:
                cut_nodes.add(s)
            if s in parent and parent[s] != None and low[node]>=disc[s]:
                cut_nodes.add(s)
        elif(node != parent[s]):
            low[s] = min(low[s],disc[node])

def find_cut_nodes(G: Graph):
    """
    :param G:

    Preparing the Creation of a Breadth_first_search_tree to get the Cut-Nodes

    :return: set of Cut-Nodes
    """
    s = random.sample(G.internal_ids_node_ids.keys(), 1)[0]
    time = 0
    disc = {}; low = {}; parent = {s:None}; cut_nodes = set()
    breadth_first_search_tree(G,s,disc,low,time,parent,cut_nodes)
    return cut_nodes

def not_to_visit_neighbors_subset_nodes(G: Graph):
    """
    :param G:

    Finding all Nodes that dont need to be visited in the all pair shortest path for the calculation of the diameter of graph

    :return: set of node_not_to_visit, dict of nodes with the same distance
    """
    node_not_to_visit = set()
    same_distance = dict()

    hash_map = dict()
    for v in G.internal_ids_node_ids:
        v_neighbors = G.get_internal_neighbors(v)
        v_degree = len(v_neighbors)
        v_neighbors_hash = hash(sum([hash(str(i)) for i in v_neighbors]))
        if v_neighbors_hash not in hash_map:
            hash_map[v_neighbors_hash] = v
        else:
            same_distance[v] = hash_map[v_neighbors_hash]
        if v_degree != 1:
            for u in G.get_internal_grand_neighbors(v):       #Der aufwand nochmal alle neigbors zu holen könnte zu groß sein
                u_neighbors = G.get_internal_neighbors(u)
                if len(u_neighbors) != 1 and u_neighbors <= v_neighbors: #Der Teilmengenverlgeich brauch lange
                    if v not in same_distance.keys():
                        node_not_to_visit.add(v)
        #Wenn der Knotengrad 1 ist aber der des einzigen nachtbarn nicht dann muss man diesen nachtbarn nicht besuchen
        elif G.get_node_degree(G.internal_ids_node_ids[list(v_neighbors)[0]]) > 1: #Nicht sehr effektiv das erst in eine Liste umzuwandeln
            node_not_to_visit.add(list(v_neighbors)[0])
            if v in same_distance:
                node_not_to_visit.add(v)

    return node_not_to_visit,same_distance

def single_source_shortest_path_opt(G: Graph, s, same_distance_copy,d_max):
    """
    :param G:
    :param s: name of the Graph node for which shortest paths are computed

    calculates the length of the shortest path from node s to each node in the Graph.

    returns:
    dictionary where keys are names of all nodes in the Graph and values
    are corresponding distances (int). Non-reachable nodes have distance infinite

    """
    same_distance = same_distance_copy.copy()
    dist = {}
    dist[s] = 0
    if s in same_distance.keys():
        same_distance.pop(s)
    elif s in same_distance.values():
        same_distance.pop(list(same_distance.keys())[list(same_distance.values()).index(s)])
    visited = {s}
    visited.update(set(same_distance.values()))
    next_level = [s]
    distance = 0

    # traverse each "distance level" seperately, making stack pop operations unnecessary
    while next_level:
        distance += 1
        child_level = []
        for u in next_level:
            for v in G.get_internal_neighbors(u):
                if v not in visited:
                    visited.add(v)
                    child_level.append(v)
                    external_v = v
                    dist[external_v] = distance
            if len(visited) == G.n:
                break
                #return dist
        next_level = child_level
    for node in same_distance.keys():
        if node in dist.keys():
            dist[same_distance[node]] = dist[node]
        elif same_distance[node] in dist.keys():
            dist[node] = dist[same_distance[node]]
    if distance-1 == d_max:
        return dist , True
    return dist , False

def min_condition(dist,neighbors):
    dist_v = dist[next(iter(neighbors))].copy()
    #print("dist_v: ",dist_v, "\n", "neighbors: ", neighbors)
    for u in dist_v:
        min = math.inf
        for w in neighbors:
            #print(w,u)
            #print("neighbors: ",dist[w])
            if dist[w][u] < min:                                    #Fehler
                min = dist[w][u]
        dist_v[u] = min + 1
    return  dist_v

def all_pair_shortest_path_minimum_condition(G: Graph,dist,v,max_node_degree,same_distance,d_max):
    """
    :param G: Graph
    :param dist: Distance-Dictionary
    :param v: Node form witch it will be search from
    :param max_node_degree: Integer for the max_node_degree for witch the breath first search will be run
    :param same_distance: Nodes that have the same distance dictionary dont need to be visited both.
    :param d_max:
    :return: The Distance-Dictionary of v
    """
    dist_v = {}
    all_distance_known = True
    neighbors = G.get_internal_neighbors(v)

    for w in neighbors:
        if w not in dist:
            all_distance_known = False


    if all_distance_known and neighbors != set():
        dist_v = min_condition(dist,neighbors)
    elif G.get_node_degree(G.internal_ids_node_ids[v]) <= max_node_degree and neighbors != set():
        dist[v], found_diameter = single_source_shortest_path_opt(G, v, same_distance, d_max)
        if found_diameter:
            return d_max
        return
    else:
        for w in neighbors:
            if w not in dist:
                dist[w], found_diameter = single_source_shortest_path_opt(G, w,same_distance,d_max)
                if found_diameter:
                    return d_max
        dist_v = min_condition(dist,neighbors)


    dist[v] = dist_v
    for w in G.get_neighbors(G.internal_ids_node_ids[v]):
        dist[v][w] = 1
    dist[v][G.internal_ids_node_ids[v]] = 0

def all_pairs_shortest_path_opt(G: Graph,max_node_degree,node_not_to_visit,same_distance):
    """
    :param G: Graph
    :param max_node_degree: Integer for the max_node_degree for witch the breath first search will be run
    :param node_not_to_visit: Nodes that dont need to be visited for the calculation of the Diameter.
    :param same_distance: Nodes that have the same distance dictionary dont need to be visited both.

    Made an Appraisal for the larges possible Diameter. Than will calculate the all_pair_shortest_path for every node.

    :return: The Distance-Dictornaray of ever node that not in node_not_to_visit and in G OR It will return the diameter if the Algo finds a diameter that will be equal to the larges possible Diameter.
    """
    dist = {}
    all_nodes = set(G.node_ids_internal_ids.values()).difference(node_not_to_visit)

    d_max = math.inf
    if len(node_not_to_visit) != 0:
        v = node_not_to_visit.copy().pop()                                                                                  #nicht sehr speichereffizent
        dist[v] = single_source_shortest_path_opt(G, v, same_distance,math.inf)[0]
        d_max = 2*max(dist[v].values())                                                                                     #gut für eine erste Abschätzung


    for v in all_nodes:
        if v not in dist:
            diameter = all_pair_shortest_path_minimum_condition(G,dist,v,max_node_degree,node_not_to_visit,same_distance,d_max)
            if diameter != None:
                return diameter
    return dist

def diameter_opt(G: Graph,max_node_degree):
    """
    :param G: The complet Graph. Dont need to be connected
    :param max_node_degree: Integer for the max_node_degree for witch the breath first search will be run

    Calculation all Pair-Shortest-Path for each node expect for nodes_not_to_visit or cut-nodes. Thes node can not be the start or end Node of an shortest path that define the diameter of G.

    :return: The Diameter of the Graph G as Integer
    """
    diameter = -math.inf

    sub_graph = max(connected_components(G), key=len)
    for node in G.get_nodes():
        if node not in sub_graph:
            G.remove_node(node)

    node_not_to_visit, same_dist = not_to_visit_neighbors_subset_nodes(G)
    node_not_to_visit.update(find_cut_nodes(G))

    apsp = all_pairs_shortest_path_opt(G,max_node_degree,node_not_to_visit,same_dist)

    if type(apsp) != int:
        for node in apsp:
            d = max(apsp[node].values())
            if d > diameter:
                diameter = d
        return diameter
    else:
        return apsp