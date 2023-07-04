import copy

from src.Graph import Graph
import math


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
            s += G.get_node_degree(n)
        s = -(s**2)
        s /= 4 * (G.m ** 2)
        s += (edge_count(G, c) / G.m)
        return s

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


def min_cut_alg(G, cluster):
    cluster_graph = G.copy_graph()
    all_nodes = G.get_nodes()
    for c in all_nodes - cluster:
        cluster_graph.remove_node(c)

    all_nodes = cluster_graph.get_nodes()

    changed_nodes = dict()
    for node in all_nodes:
        changed_nodes[node] = {node}

    edges = cluster_graph.edges
    mapping = cluster_graph.internal_ids_node_ids
    edge_weightes = dict()
    for v in edges:
        v_weightes = dict()
        for u in edges[v]:
            v_weightes[mapping[u]] = 1
        edge_weightes[mapping[v]] = v_weightes

    all_cuts = []

    while len(all_nodes) > 1:
        start_node = list(all_nodes)[0]
        current_nodes = {start_node}
        rest_nodes = all_nodes - current_nodes
        previous_node = start_node
        while len(rest_nodes) > 1:
            neighbors = dict()
            for rn in rest_nodes:
                neighbors[rn] = 0
            for node in current_nodes:
                c = edge_weightes[node]
                n_neighbors = {key for key in c}
                for n in n_neighbors - current_nodes:
                    neighbors[str(n)] += c[str(n)]
            max_value = -1
            max_node = None
            for key in neighbors:
                if neighbors[key] > max_value:
                    max_value = neighbors[key]
                    max_node = key
            # add max node to current nodes
            current_nodes |= {max_node}
            previous_node = max_node
            rest_nodes -= {max_node}
        # remove last node from all_nodes and update edge weights
        last_node = list(rest_nodes)[0]

        # add last cut
        last_weight = 0
        edge_entry = copy.deepcopy(edge_weightes[last_node])
        for key in edge_entry:
            last_weight += edge_entry[key]
        all_cuts.append([changed_nodes[last_node], last_weight])

        # union of last_node and previous_node
        all_nodes.remove(last_node)
        changed_nodes[previous_node] |= changed_nodes[last_node]
        del changed_nodes[last_node]
        # update edge weights
        try:
            del edge_weightes[previous_node][last_node]
        except:
            pass
        del edge_weightes[last_node]
        for v in edge_entry:
            if v == previous_node:
                continue
            if v in edge_weightes[previous_node]:
                edge_weightes[previous_node][v] += edge_entry[v]
            else:
                edge_weightes[previous_node][v] = edge_entry[v]
            # remove all connections to the last node
            del edge_weightes[v][last_node]
            # update weights
            try:
                edge_weightes[v][previous_node] += edge_entry[v]
            except:
                edge_weightes[v][previous_node] = edge_entry[v]
    return all_cuts


def find_minimum_cut(G: Graph, cluster=None):
    if cluster is None:
        cluster = copy.deepcopy(G.get_nodes())
    all_cuts = min_cut_alg(G, cluster)
    min_cut = None
    min_cut_value = math.inf
    for cut in all_cuts:
        if cut[1] < min_cut_value:
            min_cut_value = cut[1]
            min_cut = cut
    return min_cut


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
    # min_cut = find_minimum_cut(G, cut_cluster)[0]
    # go other all cuts:
    max_value = sum(new_evaluation_values)
    max_evaluation_values = copy.deepcopy(new_evaluation_values)
    max_clustering = copy.deepcopy(new_clustering)

    all_cuts = min_cut_alg(G, cut_cluster)
    for c in all_cuts:
        min_cut = c[0]

        c1 = cut_cluster - min_cut
        c2 = min_cut

        tmp_clustering = copy.deepcopy(new_clustering)
        tmp_clustering[m1] = c1
        tmp_clustering.append(c2)
        m2 = len(tmp_clustering) - 1
        if version == "mod":
            v1, v2 = compute_modularity(G, tmp_clustering, [m1, m2])
            new_evaluation_values[m1] = v1
            new_evaluation_values.append(v2)
            modularity = sum(new_evaluation_values)
            if modularity > max_value:
                max_value = modularity
                max_evaluation_values = copy.deepcopy(new_evaluation_values)
                max_clustering = copy.deepcopy(tmp_clustering)
        else:
            v1, v2 = compute_disagreement(G, tmp_clustering, [m1, m2])
            new_evaluation_values[m1] = v1
            new_evaluation_values.append(v2)
            disagreement = G.m - sum(new_evaluation_values)
            if disagreement < max_value:
                max_value = disagreement
                max_evaluation_values = copy.deepcopy(new_evaluation_values)
                max_clustering = copy.deepcopy(tmp_clustering)
    return max_value, max_evaluation_values, max_clustering


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
                new_sum, new_values, new_clustering = merge_cluster_value(G, clustering, i1, i2, current_values,
                                                                          version)
                if version == "mod" and new_sum > max_value:
                    max_values = new_values
                    max_value = new_sum
                    max_clustering = new_clustering
                elif version == "dis" and new_sum < max_value:
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
            elif version == "dis" and new_sum < max_value:
                max_values = new_values
                max_value = new_sum
                max_clustering = new_clustering
        if max_values:
            current_values = max_values
            current_value = max_value
            clustering = max_clustering
            better = True
    return clustering, current_value


def compute_rand_index(G, clustering_1: list, clustering_2: list):
    a = 0
    b = 0
    for elm_1 in G.get_nodes():
        for elm_2 in G.get_nodes():
            in_cluster_1 = False
            in_cluster_2 = False

            for cluster in clustering_1:
                if {elm_1, elm_2}.issubset(cluster):
                    in_cluster_1 = True

            for cluster in clustering_2:
                if {elm_1, elm_2}.issubset(cluster):
                    in_cluster_2 = True

            if in_cluster_1 and in_cluster_2:
                a += 1
            if not in_cluster_1 and not in_cluster_2:
                b += 1

    return (a + b) / math.comb(len(G.get_nodes()), 2)
