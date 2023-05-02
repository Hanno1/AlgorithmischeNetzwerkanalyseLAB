from collections import deque
from src.Graph import Graph
import multiprocessing
import src.CustomExceptions as Exc
import math

__all__ = [
    "single_source_shortest_path",
    "all_pairs_shortest_path",
    "shortest_s_t_path",
    "connected_components"
]

#@lru_cache(maxsize=None)
def single_source_shortest_path(G: Graph, s):
    """
    :param Graph: Graph object to analyse 
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
    dist[s]=0

    internal_s = G.node_ids_internal_ids[s]
    visited = {internal_s}
    next_level = [internal_s]
    distance = 0

    # traverse each "distance level" seperately, making stack pop operations unnecessary
    while next_level:
        distance +=1
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
    dist={}
    for v in G.node_ids_internal_ids:
        dist[v]= single_source_shortest_path(G,v)
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
    :param Graph: Graph object to analyse 

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
    num_processes = multiprocessing.cpu_count()
    if num_processes < 4:
        return _all_pairs_shortest_path_single(G)
    else:
        return _all_pairs_shortest_path_parallel(G,num_processes)


def breadth_first_search(G: Graph, node_IDs: list, visited: list, parent: list, queue: list):
    current_node = queue.pop(0)
    for node_id in G.get_neighbors(node_IDs[current_node]):
        node = node_IDs.index(node_id)
        if not visited[node]:
            visited[node] = True
            parent[node] = current_node
            queue.append(node)


def check_collision(number_of_nodes, s_visited: list, t_visited: list):
    for i in range(number_of_nodes):
        if s_visited[i] and t_visited[i]:
            return i
    return -1


def shortest_s_t_path(G: Graph, s_id, t_id):
    s_id = str(s_id)
    t_id = str(t_id)
    node_ids = list(G.node_ids_internal_ids.keys())
    s = node_ids.index(s_id)
    t = node_ids.index(t_id)
    shortest_path = []

    s_visited = [False] * G.n
    t_visited = [False] * G.n

    s_queue = []
    t_queue = []

    s_parent = [-1] * G.n
    t_parent = [-1] * G.n

    s_visited[s] = True
    s_queue.append(s)
    t_visited[t] = True
    t_queue.append(t)

    while s_queue and t_queue:
        breadth_first_search(G, node_ids, s_visited, s_parent, s_queue)
        breadth_first_search(G, node_ids, t_visited, t_parent, t_queue)
        intersection = check_collision(G.n, s_visited, t_visited)
        if intersection != -1:
            i = intersection
            shortest_path.append(node_ids[i])
            while i != s:
                shortest_path.append(node_ids[s_parent[i]])
                i = s_parent[i]
            shortest_path.reverse()
            i = intersection
            while i != t:
                shortest_path.append(node_ids[t_parent[i]])
                i = t_parent[i]
            return shortest_path, len(shortest_path) - 1
    return [], math.inf

def connected_components(G: Graph):
    """
    :param Graph: Graph object to analyse 

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
            if distances[node_id]< math.inf:
                component.add(node_id)
                visited.add(node_id)
        components.append(component)
    return components
