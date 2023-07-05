import copy
import math
from src.Graph import Graph
import heapq


def edge_count(G: Graph, cluster: list):
    edge_count = 0
    for el in cluster:
        neighbors = G.get_neighbors(el) & cluster
        edge_count += len(neighbors)
    return edge_count // 2


def outer_edge_count(G: Graph, cluster: list):
    edge_count = 0
    for el in cluster:
        other_neighbors = G.get_neighbors(el) - cluster
        edge_count += len(other_neighbors)
    return edge_count // 2


def compute_modularity(G: Graph, C: list, index: list = None):
    def compute_mod_single_cluster(c):
        s = 0
        for n in c:
            s += G.get_node_degree(n)
        s = -(s ** 2)
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
        return ((cluster_length * (cluster_length - 1)) / 2) - edge_count(G, c) + outer_edge_count(G, c)

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
        return sum(new_evaluation_values), new_evaluation_values, new_clustering


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
            disagreement = sum(new_evaluation_values)
            if disagreement < max_value:
                max_value = disagreement
                max_evaluation_values = copy.deepcopy(new_evaluation_values)
                max_clustering = copy.deepcopy(tmp_clustering)
    return max_value, max_evaluation_values, max_clustering


def merge_clustering(G: Graph, version="mod"):
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


def cut_clustering(G: Graph, version="mod"):
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
            if elm_1 == elm_2:
                continue
            in_cluster_1 = False
            in_cluster_2 = False

            for cluster in clustering_1:
                if {elm_1, elm_2} <= (cluster):
                    in_cluster_1 = True

            for cluster in clustering_2:
                if {elm_1, elm_2} <= (cluster):
                    in_cluster_2 = True

            if in_cluster_1 and in_cluster_2:
                a += 1
            if not in_cluster_1 and not in_cluster_2:
                b += 1
    return (a / 2 + b / 2) / math.comb(G.n, 2)


def merge_modularity_opt(G: Graph, verbose=False):
    def compute_update_deltas(deltas, a, merge_i, merge_j):
        # computes delta indices that need to be deleted from heap
        # computes new delta values that need to be added to heap
        # -> we delete and insert instead of updating because of the heap datastructure
        sub_deltas = {}  # get all deltas that are relevant for current merge choices (tuples containing i or j)
        for idx, (delta, (u, v)) in enumerate(deltas):
            if {u, v} == {merge_i, merge_j}:
                continue
            if u in [merge_i, merge_j] or v in [merge_i, merge_j]:
                sub_deltas[(u, v)] = (
                delta, idx)  # also save index of where we found it in »deltas« so we can delete it later if necessary

        i_neighbors = set([n for N in G.edges for n in G.edges[N] if N in clusters[merge_i]])
        j_neighbors = set([n for N in G.edges for n in G.edges[N] if N in clusters[merge_j]])
        q_idx_to_delete = []
        q_updates = []

        # now we need to update the deltas
        for c_idx in sub_deltas:  # iterate over all deltas that might change
            u, v = c_idx  # cluster indices
            delta, q_idx = sub_deltas[
                c_idx]  # get the delta for cluster-change (u,v) and the associated queue-index q_idx for »deltas»
            if merge_j in [u,
                           v]:  # if the "merged-in" cluster is part of the delta-variable it is not changed (its deleted later)
                q_idx_to_delete.append(q_idx)  # for deletion of with merge_j associated variables later
                continue
            l = v if u == merge_i else u  # assign l to the other cluster-index, thats not part of the merge
            cl_nodes = set()
            for n in clusters[l]:
                try:
                    cl_nodes |= G.edges[n]
                except:
                    pass

            if merge_j > l:  # get change for cluster-merge (merge_j, l)
                delta_j, _ = sub_deltas[(l, merge_j)]
            else:
                delta_j, _ = sub_deltas[(merge_j, l)]

            # update deltas depending on cluster l nodes' connections with the merged clusters
            # update = -(update) from lectures because we have a min heap
            updated_delta = None
            if cl_nodes & j_neighbors and cl_nodes & i_neighbors:
                updated_delta = (delta + delta_j, (u, v))
            elif cl_nodes & i_neighbors:
                updated_delta = (delta + 2 * a[merge_i] * a[l], (u, v))
            elif cl_nodes & j_neighbors:
                updated_delta = (delta + 2 * a[merge_j] * a[l], (u, v))
            if updated_delta is not None:
                q_idx_to_delete.append(q_idx)
                q_updates.append(updated_delta)
        return q_idx_to_delete, q_updates

    nodes = sorted(list(G.get_internal_nodes()))
    clusters = {i: {n} for i, n in enumerate(nodes)}  # save clusters with their "ID"
    degrees = {n: len(G.edges[n]) for n in G.edges}
    a = {i: degrees[n] / (2 * G.m) for i, n in enumerate(nodes)}
    deltas = []

    # init deltas
    for i in range(G.n):
        n_i = nodes[i]
        for j in range(i + 1, G.n):
            n_j = nodes[j]
            if n_j in G.edges[n_i]:
                change = 1 / G.m - (2 * degrees[n_i] * degrees[n_j]) / (4 * G.m ** 2)
            else:
                change = - (2 * degrees[n_i] * degrees[n_j]) / (4 * G.m ** 2)
            values = (-change, (i, j))  # init delta = -(init delta) because we have a min heap
            deltas.append(values)
    heapq.heapify(deltas)

    while len(clusters) > 1:
        _, (merge_i, merge_j) = heapq.heappop(deltas)
        if verbose:
            print("merge", (merge_i, merge_j))
        clusters[merge_i] = clusters[merge_i] | clusters[merge_j]
        a[merge_i] += a[merge_j]

        q_idx_to_delete, q_updates = compute_update_deltas(deltas, a, merge_i, merge_j)

        # delete all variables associated with j and update deltas by deletion and re-insertion
        del clusters[merge_j]
        del a[merge_j]
        q_idx_to_delete.reverse()  # index array is ordered (ascending). reverse because otherwise indices would not match after deletion
        for idx in q_idx_to_delete:
            del deltas[idx]
        for update in q_updates:
            heapq.heappush(deltas, update)

        done = True
        for (d,
             _) in deltas:  # check if done: if all values in queue are > 0 (because we have a min-heap and we reversed the deltas)
            if d < 0:
                done = False
                break
        if done:
            break

    # translate internal ids
    new_clusters = []
    for c in clusters:
        new_c = set()
        for i in clusters[c]:
            new_c.add(G.internal_ids_node_ids[i])
        new_clusters.append(new_c)

    return new_clusters


def clustering(G, mode = "cut", optimize="modularity"):
    if mode == "cut":
        if optimize == "modularity":
            cl, _ = cut_clustering(G)
        else:
            cl, _ = cut_clustering(G, version ="dis")
    else:
        if optimize == "modularity":
            cl = merge_modularity_opt(G)
        else:
            cl, _ = merge_clustering(G)
    return cl
