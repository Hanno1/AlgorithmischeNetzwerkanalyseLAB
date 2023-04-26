import copy
from collections import deque
from src.Graph import Graph
import multiprocessing
import src.CustomExceptions as Exc
import math


def single_source_shortest_path(G: Graph, s):
    if s not in G.nodes:
        raise Exc.NodeDoesNotExistException(s)
    dist = {}
    for n in G.nodes:
        dist[n] = math.inf
    dist[s] = 0
    queue = deque([s])
    visited = {s}
    while queue:
        u = queue.popleft()
        for v in G.get_neighbors(u):
            if v not in visited:
                visited.add(v)
                queue.append(v)
                dist[v] = dist[u] + 1
    return dist


def single_source_shortest_path_vector(G: Graph, node_idx, mapping):
    if node_idx not in G.nodes:
        raise Exc.NodeDoesNotExistException(node_idx)
    dist = [math.inf for _ in range(len(mapping))]
    dist[mapping[node_idx]] = 0

    queue = deque([node_idx])
    visited = {node_idx}
    while queue:
        u = queue.popleft()
        current_dist = dist[mapping[u]] + 1
        for v in G.get_neighbors(u):
            if v not in visited:
                visited.add(v)
                queue.append(v)
                dist[mapping[v]] = current_dist
    return dist, mapping


def all_pair_shortest_path(G: Graph):
    dist = {}
    for v in G.nodes:
        v_id = G.nodes[v].id
        dist[v_id] = single_source_shortest_path(G, v_id)
    return dist


def all_pair_shortest_path_matrix(G: Graph):
    G_prime = copy.deepcopy(G)

    matrix = [[math.inf for _ in range(G.n)] for _ in range(G.n)]
    mapping = G.get_internal_mapping()

    counter = 0
    for key in G.nodes:
        vec, _ = single_source_shortest_path_vector(G_prime, key, mapping)
        for col in range(counter, len(mapping)):
            matrix[counter][col] = vec[col]
            matrix[col][counter] = vec[col]
        G_prime.remove_node(key)
        counter += 1
    return matrix, mapping


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
    node_ids = list(G.nodes.keys())
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
