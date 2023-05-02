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
    num_processes = multiprocessing.cpu_count()
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
