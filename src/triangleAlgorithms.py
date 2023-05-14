import copy
from numpy.linalg import matrix_power
from src.Graph import Graph


def sort_nodes(G: Graph):
    """
    sort vertices by degree in a dictionary (degree -> list of nodes that have this degree)

    :param G: Graph
    :return: dictionary
    """
    # sort vertices by degree and use dictionary for it
    nodes = G.get_internal_nodes()
    vertices_dict = dict()

    for node in nodes:
        degree = len(G.get_internal_neighbors(node))
        if degree not in vertices_dict:
            vertices_dict[degree] = [node]
        else:
            vertices_dict[degree].append(node)
    return vertices_dict


def algorithm_node_iterator_without_sorting(G: Graph):
    """
    trivial Algorithm for getting all triangles in the Graph G
    just look at all pairwise neighbors of all nodes and check if they are connected

    :param G: Graph
    :return: number of triangles
    """
    tmpG = copy.deepcopy(G)

    number_triangles = 0
    mapping = G.internal_ids_node_ids

    triangles = []
    for internal_id in mapping:
        neighbors = list(tmpG.get_internal_neighbors(internal_id))
        for i in range(0, len(neighbors)-1):
            for j in range(i+1, len(neighbors)):
                n_i = neighbors[i]
                n_j = neighbors[j]

                if tmpG.test_internal_neighbors(n_i, n_j):
                    triangles.append([mapping[internal_id], mapping[n_i], mapping[n_j]])
                    number_triangles += 1
        tmpG.remove_node(mapping[internal_id])
    return number_triangles, triangles


def algorithm_node_iterator(G: Graph):
    """
    trivial Algorithm for getting all triangles in the Graph G
    just look at all pairwise neighbors of all nodes and check if they are connected

    :param G: Graph
    :return: number of triangles
    """
    tmpG = copy.deepcopy(G)
    vertices_dict = sort_nodes(tmpG)

    number_triangles = 0
    mapping = tmpG.internal_ids_node_ids
    sorted_keys = sorted(vertices_dict.keys(), reverse=True)

    if sorted_keys.__contains__(0):
        sorted_keys.remove(0)
    if sorted_keys.__contains__(1):
        sorted_keys.remove(1)

    triangles = []

    for key in sorted_keys:
        for entry in vertices_dict[key]:
            neighbors = list(tmpG.get_internal_neighbors(entry))
            for i in range(0, len(neighbors)-1):
                for j in range(i+1, len(neighbors)):
                    n_i = neighbors[i]
                    n_j = neighbors[j]

                    if tmpG.test_internal_neighbors(n_i, n_j):
                        triangles.append([mapping[entry], mapping[n_i], mapping[n_j]])
                        number_triangles += 1
            tmpG.remove_node(mapping[entry])
    return number_triangles, triangles


def algorithm_chiba_and_nishizeki(G: Graph):
    """
    This algorithm is from the paper "Triangle Listing Algorithms: Back from the Diversion"
    by Mark Ortmann and Ulrik Brandes

    :param G: Graph
    :return: number of triangles in G
    """
    tmpG = copy.deepcopy(G)
    vertices_dict = sort_nodes(tmpG)

    number_triangles = 0
    mapping = tmpG.internal_ids_node_ids
    sorted_keys = sorted(vertices_dict.keys(), reverse=True)

    if sorted_keys.__contains__(0):
        sorted_keys.remove(0)
    if sorted_keys.__contains__(1):
        sorted_keys.remove(1)

    triangles = []

    for key in sorted_keys:
        for entry in vertices_dict[key]:
            marked = list(tmpG.get_internal_neighbors(entry))
            while marked:
                node = marked[0]
                neighbors = list(tmpG.get_internal_neighbors(node))
                for neighbor in neighbors:
                    if neighbor in marked:
                        triangles.append([mapping[entry], mapping[node], mapping[neighbor]])
                        number_triangles += 1
                marked.pop(0)
            tmpG.remove_node(mapping[entry])
    return number_triangles, triangles


def first_neighbor_index(i, adj_matrix):
    row = adj_matrix[i]
    for el_counter in range(len(row)):
        el = row[el_counter]
        if el == 1:
            return el_counter
    return len(row)


def next_neighbor_index(i, adj_matrix, j):
    row = adj_matrix[i]
    for el_counter in range(len(row)):
        el = row[el_counter]
        if el == 1 and el_counter > j:
            return el_counter
    return len(row)


def algorithm_edge_iterator(G: Graph):
    """
    implementation of the compact forward Algorithm described in Algorithmic Aspects of Triangle-Based Network Analysis
    by Thomas Schank

    :param G: Graph
    :return: number of triangles in G
    """
    adj, node_id_mapping, adj_index_mapping = G.get_adjacency_matrix()
    triangle_counter = 0
    triangles = []
    for i in range(G.n):
        neighbors = G.get_neighbors(adj_index_mapping[i])
        for neighbor in neighbors:
            l = node_id_mapping[neighbor]

            if l >= i:
                continue

            j = first_neighbor_index(i, adj)
            k = first_neighbor_index(l, adj)

            while j < l and k < l:
                if j < k:
                    j = next_neighbor_index(i, adj, j)
                elif k < j:
                    k = next_neighbor_index(l, adj, k)
                else:
                    # k == j
                    triangles.append([adj_index_mapping[k], adj_index_mapping[i], adj_index_mapping[l]])
                    triangle_counter += 1

                    j = next_neighbor_index(i, adj, j)
                    k = next_neighbor_index(l, adj, k)
        i += 1
    return triangle_counter, triangles


def algorithm_triangle_counter_ayz(G: Graph, gamma):
    V_low = []
    V_high = []

    beta = G.m**((gamma - 1) / (gamma + 1))
    tri_counter = dict()
    sum_of_triangles = 0

    for v in G.node_ids_internal_ids:
        tri_counter[v] = 0
        node_degree = G.get_node_degree(v)
        if node_degree <= beta:
            V_low.append(v)
        else:
            V_high.append(v)
    for v in V_low:
        neighbors = list(G.get_neighbors(v))
        for i in range(len(neighbors)-1):
            for j in range(i+1, len(neighbors)):
                node_i = neighbors[i]
                node_j = neighbors[j]
                if G.test_neighbors(node_i, node_j):
                    if node_i in V_low and node_j in V_low:
                        tri_counter[v] += 1/3
                        tri_counter[node_i] += 1/3
                        tri_counter[node_j] += 1/3
                        sum_of_triangles += 1 / 3
                    elif node_i in V_high and node_j in V_high:
                        tri_counter[v] += 1
                        tri_counter[node_i] += 1
                        tri_counter[node_j] += 1
                        sum_of_triangles += 1
                    else:
                        tri_counter[v] += 1 / 2
                        tri_counter[node_i] += 1 / 2
                        tri_counter[node_j] += 1 / 2
                        sum_of_triangles += 1 / 2
    A = Graph()
    for v in V_high:
        A.add_node(v)
        neighbors = G.get_neighbors(v)
        for neighbor in neighbors:
            if neighbor in V_high:
                A.add_edge(v, neighbor)

    mat, m1, m2 = A.get_adjacency_matrix()
    A_3 = matrix_power(mat, 3)

    for v in V_high:
        tri_counter[v] += A_3[m1[v]][m1[v]] / 2
        sum_of_triangles += A_3[m1[v]][m1[v]] / 6

    return round(sum_of_triangles), tri_counter


def algorithm_triangle_counter_ayz_internal_ids(G: Graph, gamma):
    V_low = []
    V_high = []

    beta = G.m**((gamma - 1) / (gamma + 1))
    tri_counter = dict()
    sum_of_triangles = 0

    for v in G.internal_ids_node_ids:
        tri_counter[v] = 0
        node_degree = len(G.get_internal_neighbors(v))
        if node_degree <= beta:
            V_low.append(v)
        else:
            V_high.append(v)
    for v in V_low:
        neighbors = list(G.get_internal_neighbors(v))
        for i in range(len(neighbors)-1):
            for j in range(i+1, len(neighbors)):
                node_i = neighbors[i]
                node_j = neighbors[j]
                if G.test_internal_neighbors(node_i, node_j):
                    if node_i in V_low and node_j in V_low:
                        tri_counter[v] += 1/3
                        tri_counter[node_i] += 1/3
                        tri_counter[node_j] += 1/3
                        sum_of_triangles += 1 / 3
                    elif node_i in V_high and node_j in V_high:
                        tri_counter[v] += 1
                        tri_counter[node_i] += 1
                        tri_counter[node_j] += 1
                        sum_of_triangles += 1
                    else:
                        tri_counter[v] += 1 / 2
                        tri_counter[node_i] += 1 / 2
                        tri_counter[node_j] += 1 / 2
                        sum_of_triangles += 1 / 2
    A = Graph()
    for v in V_high:
        A.add_node(v)
        neighbors = G.get_internal_neighbors(v)
        for neighbor in neighbors:
            if neighbor in V_high:
                A.add_edge(v, neighbor)

    mat, m1, m2 = A.get_adjacency_matrix()
    A_3 = matrix_power(mat, 3)

    for v in V_high:
        tri_counter[v] += A_3[m1[str(v)]][m1[str(v)]] / 2
        sum_of_triangles += A_3[m1[str(v)]][m1[str(v)]] / 6
    return round(sum_of_triangles), tri_counter
