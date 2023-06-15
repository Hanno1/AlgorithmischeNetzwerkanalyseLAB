from src.Graph import Graph
from src.graphParameters import degeneracy, degeneracy_bucket, density
import time

def bron_kerbosch(G, timeout):
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

def find_pivot_bf(G: Graph, C, F): # brute-force maximize C & u_neighbors
    max_eliminated = 0
    C_internal = set([G.node_ids_internal_ids[el] for el in C ])
    F_internal = set([G.node_ids_internal_ids[el] for el in F ])
    pool = C_internal | F_internal
    for u in pool:
        eliminated = len(G.edges[u] & C_internal)
        if eliminated >= max_eliminated:
            max_eliminated=eliminated
            current_u = u
    return set([G.internal_ids_node_ids[s] for s in G.edges[current_u]])

def find_pivot_deg(G: Graph, C, F): # brute-force maximize C & u_neighbors
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
    _, order = degeneracy_bucket(G)
    for i in range(0,G.n):
        neighbors = G.get_neighbors(order[i])
        C = set(order[i+1:]) & neighbors
        F = set(order[:i]) & neighbors
        yield from bron_kerbosch_pivot(G, {order[i]}, C, F, pivot_strategy)

def find_cliques(G: Graph, mode = "regular", pivot_strategy=None, timeout = 60):
    if mode == "regular":
        yield from bron_kerbosch(G, timeout = timeout)
    if mode == "pivot":
        if pivot_strategy is None:
            raise Exception("need to specify a pivot strategy")
        nodes = set(G.node_ids_internal_ids.keys())
        yield from bron_kerbosch_pivot(G, set(), nodes, set(), pivot_strategy)
    if mode == "degeneracy":
        if pivot_strategy is None:
            raise Exception("need to specify a pivot strategy")
        yield from bron_kerbosch_pivot_degen(G, pivot_strategy)

if __name__ == "__main__":
    from time import time
    import os
    import pandas as pd
    directory = "../../networks/"

    for params in [("regular",None), ("pivot", find_pivot_bf), ("pivot", find_pivot_deg), ("degeneracy",find_pivot_bf),("degeneracy", find_pivot_deg)]:
        mode = params[0]
        pivot_strategy = params[1]
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
            for i, clique in enumerate(find_cliques(G, mode = mode, pivot_strategy=pivot_strategy, timeout = 60)):
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
            print(stats)
            df.loc[len(df)] = stats
        print(mode, pivot_strategy)
        print(df)