from collections import deque
from Graph import Graph
import multiprocessing

def single_source_shortest_path(G : Graph, s):
    dist = {}
    for n in G.nodes:
        dist[n] = float('inf')
    dist[s]=0
    queue = deque([s])
    visited = {s}
    while queue:
        u = queue.popleft()
        for v in G.getNeighbors(u):
            if v not in visited:
                visited.add(v)
                queue.append(v)
                dist[v] = dist[u]+1
    return dist

def all_pair_shortest_path(G : Graph):
    dist = {}
    for v in G.nodes:
        v_id = G.nodes[v].id
        dist[v_id] = single_source_shortest_path(G,v_id)
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