from collections import deque
from Graph import Graph

def single_source_shortest_path(G : Graph, s):
    dist = {}
    for n in G.nodes:
        dist[G.nodes[n].id] = float('inf')
    dist[s]=0
    queue = deque([s])
    visited = {s}
    c = 0
    while queue:
        u = queue.popleft()
        for v in G.getNeighbors(u):
            if v not in visited:
                c+=1
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