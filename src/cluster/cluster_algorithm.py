import copy
from src.Graph import Graph


def edge_count(G: Graph, cluster: list):
    edge_count = 0
    for el in cluster:
        neighbors = G.get_neighbors(el) & cluster
        edge_count += len(neighbors)
    return edge_count // 2


def compute_modularity(G: Graph, C: list, index: list = None):
    def compute_mod_single_cluster(c):
        s = 0
        for n in c:
            s -= G.get_node_degree(n) ** 2
        s /= 4 * m ** 2
        s += (edge_count(G, c) / m)
        return s

    m = G.m
    if index:
        if len(index) == 1:
            return compute_mod_single_cluster(C[index[0]])
        return [compute_mod_single_cluster(C[index[0]]), compute_mod_single_cluster(C[index[1]])]
    mod = []
    for cluster in C:
        mod.append(compute_mod_single_cluster(cluster))
    return mod


def compute_disagreement(G: Graph, C: list, index: list = None):
    def compute_dis_single_cluster(c):
        cluster_length = len(c)
        return ((cluster_length * (cluster_length - 1)) / 2) - 2 * edge_count(G, c)
    if index:
        if len(index) == 1:
            return compute_dis_single_cluster(C[index[0]])
        return [compute_dis_single_cluster(C[index[0]]), compute_dis_single_cluster(C[index[1]])]
    mod = []
    for cluster in C:
        mod.append(compute_dis_single_cluster(cluster))
    return mod


def find_minimum_cut(G: Graph, cluster: set):
    cluster_graph = G.copy_graph()
    all_nodes = G.get_nodes()
    for c in all_nodes - cluster:
        cluster_graph.remove_node(c)

    changed_nodes = dict()
    for node in all_nodes:
        changed_nodes[node] = {node}

    edges = cluster_graph.edges
    edge_weightes = dict()
    for v in edges:
        v_weightes = dict()
        for u in edges[v]:
            v_weightes[u] = 1
        edge_weightes[v] = v_weightes

    all_cuts = set()

    while len(all_nodes) > 1:
        start_node = list(all_nodes)[0]
        current_nodes = {start_node}
        rest_nodes = all_nodes - current_nodes
        previous_node = None
        previous_weight = 0
        while len(rest_nodes) > 1:
            neighbors = dict()
            for rn in rest_nodes:
                neighbors[rn] = 0
            for node in current_nodes:
                n_neighbors = [key for key in edge_weightes[node]]
                for n in n_neighbors:
                    neighbors[n] += edge_weightes[node][n]
            max_value = 0
            max_node = None
            for key in neighbors:
                if neighbors[key] > max_value:
                    max_value = neighbors[key]
                    max_node = key
            # add max node to current nodes
            current_nodes |= max_node
            previous_node = max_node
            previous_weight = max_value
            rest_nodes -= max_node
        # remove last node from all_nodes and update edge weights
        last_node = rest_nodes[0]

        # add last cut
        all_cuts.add([last_node, previous_weight])

        # union of last_node and previous_node
        all_nodes.remove(last_node)
        del changed_nodes[last_node]
        changed_nodes[previous_node] |= last_node
        # update edge weights
        edge_entry = edge_weightes[last_node]
        for v in edge_entry:
            if v in edge_weightes[previous_node]:
                edge_weightes[previous_node][v] += edge_entry[v]
            else:
                edge_weightes[previous_node][v] = edge_entry[v]
        break
    return all_cuts


def merge_cluster_value(G: Graph, C: list, m1: int, m2: int, evaluation_values, version="mod"):
    if len(C) < 1:
        return
    new_evaluation_values = copy.deepcopy(evaluation_values)
    new_clustering = copy.deepcopy(C)
    new_cluster = C[m1] | C[m2]
    new_clustering[m1] = new_cluster
    new_clustering.pop(m2)
    if version == "mod":
        v1 = compute_modularity(G, new_clustering, [m1])
        new_evaluation_values[m1] = v1
        new_evaluation_values.pop(m2)
        return sum(new_evaluation_values), new_evaluation_values, new_clustering
    else:
        v1 = compute_disagreement(G, new_clustering, [m1])
        new_evaluation_values[m1] = v1
        new_evaluation_values.pop(m2)
        return G.m - sum(new_evaluation_values), new_evaluation_values, new_clustering


def cut_cluster_value(G: Graph, C: list, m1: int, evaluation_values, version="mod", rule="min_degree"):
    if len(C) < 1:
        return
    new_evaluation_values = copy.deepcopy(evaluation_values)
    new_clustering = copy.deepcopy(C)

    # TODO - more rules. this is min_degree
    cut_cluster = C[m1]
    min_degree_nodes = set()
    min_degree = G.n
    for node in cut_cluster:
        deg = G.get_node_degree(node)
        if deg < min_degree:
            min_degree_nodes = {node}
            min_degree = deg
        elif deg == min_degree:
            min_degree_nodes.add(node)

    c1 = cut_cluster - min_degree_nodes
    c2 = min_degree_nodes
    new_clustering[m1] = c1
    new_clustering.append(c2)
    m2 = len(new_clustering) - 1
    if version == "mod":
        v1, v2 = compute_modularity(G, new_clustering, [m1, m2])
        new_evaluation_values[m1] = v1
        new_evaluation_values[m2] = v2
        return sum(new_evaluation_values), new_evaluation_values, new_clustering
    else:
        v1, v2 = compute_disagreement(G, new_clustering, [m1, m2])
        new_evaluation_values[m1] = v1
        new_evaluation_values[m2] = v2
        return G.m - sum(new_evaluation_values), new_evaluation_values, new_clustering


def first_heuristic(G: Graph, version="mod"):
    clustering = []
    for node in G.get_nodes():
        clustering.append({node})
    better = True
    current_values = compute_modularity(G, clustering) if version == "mod" else compute_disagreement(G, clustering)
    current_value = sum(current_values) if version == "mod" else G.m - sum(current_values)
    while better:
        if len(clustering) == 1:
            break
        better = False
        max_value = current_value
        max_values = None
        max_clustering = None
        for i1 in range(len(clustering) - 1):
            for i2 in range(i1 + 1, len(clustering)):
                # try merging
                new_sum, new_values, new_clustering = merge_cluster_value(G, clustering, i1, i2, current_values, version)
                if version == "mod" and new_sum > max_value:
                    max_values = new_values
                    max_value = new_sum
                    max_clustering = new_clustering
                elif version == "dis" and new_sum <= max_value:
                    max_values = new_values
                    max_value = new_sum
                    max_clustering = new_clustering
        if max_values:
            current_values = max_values
            current_value = max_value
            clustering = max_clustering
            better = True
    return clustering, current_value


def second_heuristic(G: Graph, version="mod"):
    clustering = [G.get_nodes()]
    better = True
    current_values = compute_modularity(G, clustering) if version == "mod" else compute_disagreement(G, clustering)
    current_value = sum(current_values) if version == "mod" else G.m - sum(current_values)
    while better:
        if len(clustering) == 1:
            break
        better = False
        max_value = current_value
        max_values = None
        max_clustering = None
        for i in range(len(clustering)):
            new_sum, new_values, new_clustering = cut_cluster_value(G, clustering, i, current_values, version)
            if version == "mod" and new_sum > max_value:
                max_values = new_values
                max_value = new_sum
                max_clustering = new_clustering
            elif version == "dis" and new_sum <= max_value:
                max_values = new_values
                max_value = new_sum
                max_clustering = new_clustering
        if max_values:
            current_values = max_values
            current_value = max_value
            clustering = max_clustering
            better = True
    return clustering, current_value


G = Graph("../../networks/out.ucidata-zachary_")
# print(first_heuristic(G, version="dis"))
# print(second_heuristic(G, version="dis"))
find_minimum_cut(G, G.get_nodes())
