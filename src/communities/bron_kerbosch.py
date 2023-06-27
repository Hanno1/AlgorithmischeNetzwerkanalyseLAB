from src.Graph import Graph
from src.graphParameters import degeneracy_bucket, density
from time import time

def bron_kerbosch(G, timeout= 60):
    start_time = time()
    def internal(K, C, F):
        if not C and not F:
            yield K
            return
        for node in list(C):
            node_neighbors = G.get_neighbors(node)
            if time()-start_time > timeout:
                yield Exception("timeout")
                return
            yield from internal(K | {node}, C & node_neighbors, F & node_neighbors)
            C.remove(node)
            F.add(node)
    nodes = set(G.node_ids_internal_ids.keys())
    yield from internal(set(), nodes, set())

def _find_pivot_bf(G: Graph, C, F, threshold = None): # brute-force maximize C & u_neighbors
    threshold = threshold if threshold else len(C)-1
    max_eliminated = 0
    C_internal = set([G.node_ids_internal_ids[el] for el in C ])
    F_internal = set([G.node_ids_internal_ids[el] for el in F ])
    pool = C_internal | F_internal
    for u in pool:
        eliminated = len(G.edges[u] & C_internal)
        if eliminated >= max_eliminated:
            max_eliminated=eliminated
            current_u = u
            if max_eliminated>=threshold:
                break
    return set([G.internal_ids_node_ids[s] for s in G.edges[current_u]])


def _find_pivot_deg(G: Graph, C, F): # heuristic: maximize u degree
    max_eliminated = 0
    C_internal = set([G.node_ids_internal_ids[el] for el in C ])
    F_internal = set([G.node_ids_internal_ids[el] for el in F ])
    pool = C_internal | F_internal
    for u in pool:
        eliminated = len(G.edges[u])
        if eliminated >= max_eliminated:
            max_eliminated=eliminated
            current_u = u
    return set([G.internal_ids_node_ids[s] for s in G.edges[current_u]])

def bron_kerbosch_pivot(G, K, C, F, pivot_strategy):
    if not C and not F:
        yield K
        return
    u_neighbors = pivot_strategy(G,C,F) 
    for node in list(C - u_neighbors):
        node_neighbors = G.get_neighbors(node)
        yield from bron_kerbosch_pivot(G, K | {node}, C & node_neighbors, F & node_neighbors, pivot_strategy)
        C.remove(node)
        F.add(node)

def bron_kerbosch_pivot_degen(G: Graph, pivot_strategy):
    _, order = degeneracy(G)
    for i in range(0,G.n):
        neighbors = G.get_neighbors(order[i])
        C = set(order[i+1:]) & neighbors
        F = set(order[:i]) & neighbors
        yield from bron_kerbosch_pivot(G, {order[i]}, C, F, pivot_strategy)

def find_cliques(G: Graph, mode = "regular", pivot_strategy=None, timeout_regular = 60):
    pivot_func = None
    if pivot_strategy == "brute force":
        pivot_func = _find_pivot_bf
    if pivot_strategy == "degree":
        pivot_func = _find_pivot_deg
    if mode == "regular":
        yield from bron_kerbosch(G, timeout = timeout_regular)
        return
    if mode == "pivot":
        if pivot_strategy is None:
            raise Exception("need to specify a pivot strategy")
        nodes = set(G.node_ids_internal_ids.keys())
        yield from bron_kerbosch_pivot(G, set(), nodes, set(), pivot_func)
        return
    if mode == "degeneracy":
        if pivot_strategy is None:
            raise Exception("need to specify a pivot strategy")
        yield from bron_kerbosch_pivot_degen(G, pivot_func)
        return

if __name__ == "__main__":
    from time import time
    import os
    import pandas as pd
    directory = "../../networks/"

    versions = [("regular",None), ("pivot", "brute force"), ("pivot", "degree"), ("degeneracy", "brute force"),("degeneracy", "degree")]

    for params in versions:
        mode, pivot_strategy = params
        df =pd.DataFrame(columns=["filename","nodes","edges","density", "degen","num_cliques", "time","finished"])
        timeout = 60
        for filename in os.listdir(directory):
            if os.path.isdir(directory+filename):
                continue
            try:
                G = Graph(directory+filename)
            except:
                G = Graph(directory+filename,mode="metis")

            cliques = []

            tik = time()
            finished = True
            for i, clique in enumerate(find_cliques(G, mode = mode, pivot_strategy=pivot_strategy, timeout_regular = 60)):
                if isinstance(clique, Exception):
                    finished = False
                if i % 1000 == 0:
                    t = time()-tik
                    if t>60:
                        finished = False
                        break
                cliques.append(clique)
            t = time()-tik
            dens_G = round(density(G),3)
            degen_G,_ = degeneracy_bucket(G)
            stats = [filename,G.n,G.m,dens_G, degen_G, len(cliques),round(t,3),finished]
            df.loc[len(df)] = stats
        print(mode, pivot_strategy)
        print(df)