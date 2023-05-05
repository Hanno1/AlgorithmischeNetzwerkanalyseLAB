import copy

from src.Graph import Graph


def sort_nodes(G: Graph):
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


def algorithm_trivial(G: Graph):
    tmpG = copy.deepcopy(G)
    vertices_dict = sort_nodes(tmpG)

    number_triangles = 0
    mapping = tmpG.internal_ids_node_ids
    sorted_keys = sorted(vertices_dict.keys())

    for key in sorted_keys:
        if key > 1:
            for entry in vertices_dict[key]:
                neighbors = list(tmpG.get_internal_neighbors(entry))
                for i in range(0, len(neighbors)-1):
                    for j in range(i+1, len(neighbors)):
                        n_i = neighbors[i]
                        n_j = neighbors[j]

                        if tmpG.test_internal_neighbors(n_i, n_j):
                            print(f"Triangle found {entry}, {n_i}, {n_j}")
                            number_triangles += 1
                tmpG.remove_node(mapping[entry])
    return number_triangles


def algorithm_chiba_and_nishizeki_dict(G: Graph):
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
    sorted_keys = sorted(vertices_dict.keys())
    for key in sorted_keys:
        if key > 1:
            for entry in vertices_dict[key]:
                marked = list(tmpG.get_internal_neighbors(entry))
                while marked:
                    node = marked[0]
                    neighbors = list(tmpG.get_internal_neighbors(node))
                    for neighbor in neighbors:
                        if neighbor in marked:
                            print(f"Triangle found {mapping[entry]}, {mapping[node]}, {mapping[neighbor]}")
                            number_triangles += 1
                    marked.pop(0)
                tmpG.remove_node(mapping[entry])
    return number_triangles

