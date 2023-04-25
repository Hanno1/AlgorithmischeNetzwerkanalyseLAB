from collections import deque
from src.Graph import Graph
import multiprocessing
import src.exception as exc
import math


def single_source_shortest_path(G: Graph, s):
    if s not in G.nodes:
        raise exc.NodeDoesNotExist(s)
    dist = {}
    for n in G.nodes:
        dist[n] = math.inf
    dist[s] = 0
    queue = deque([s])
    visited = {s}
    while queue:
        u = queue.popleft()
        for v in G.getNeighbors(u):
            if v not in visited:
                visited.add(v)
                queue.append(v)
                dist[v] = dist[u] + 1
    return dist


def all_pair_shortest_path(G: Graph):
    dist = {}
    for v in G.nodes:
        v_id = G.nodes[v].id
        dist[v_id] = single_source_shortest_path(G, v_id)
    return dist


def _calc_shortest_paths(node_chunk, G):
    dist_chunk = {}
    for v in node_chunk:
        v_id = G.nodes[v].id
        dist_chunk[v_id] = single_source_shortest_path(G, v_id)
    return dist_chunk


def all_pair_shortest_path_parallel(G):
    dist = {}
    num_processes = multiprocessing.cpu_count()
    nodes = list(G.nodes)
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


def breadthFirstSearch(G: Graph, node_IDs: list, visited: list, parent: list, queue: list):
    current_node = queue.pop(0)
    for node_id in G.getNeighbors(node_IDs[current_node]):
        node = node_IDs.index(node_id)
        if not visited[node]:
            visited[node] = True
            parent[node] = current_node
            queue.append(node)


def checkCollision(number_of_nodes, s_visited: list, t_visited: list):
    for i in range(number_of_nodes):
        if s_visited[i] == t_visited[i]:
            return i
    return -1


def biDirSearch(G: Graph, s_id, t_id):
    node_IDs = list(G.nodes.keys())
    s = node_IDs.index(s_id)
    t = node_IDs.index(t_id)
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

    while s_queue or t_queue:
        breadthFirstSearch(G, node_IDs, s_visited, s_parent, s_queue)
        breadthFirstSearch(G, node_IDs, t_visited, t_parent, t_queue)
        intersection = checkCollision(G.n, s_visited, t_visited)
        if intersection != -1:
            i = intersection
            shortest_path.append(node_IDs[i])
            while i != s:
                shortest_path.append(node_IDs[s_parent[i]])
                i = s_parent[i]
            shortest_path.reverse()
            i = intersection
            while i != t:
                shortest_path.append(node_IDs[t_parent[i]])
                i = t_parent[i]
            return shortest_path, len(shortest_path)


def connected_components(G: Graph):
    components = []
    visited = []

    for i in G.nodes.keys():
        if i in visited:
            continue

        component = set()
        d = single_source_shortest_path(G, i)
        for key in d:
            value = d[key]
            if value < math.inf:
                component.add(key)
                visited.append(key)
        components.append(component)
    return components
