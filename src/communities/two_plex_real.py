import copy
from src.Graph import Graph
from src.graphParameters import degeneracy


def two_neighbors(G: Graph, node):
    current_nodes = set()
    for n in G.get_neighbors(node):
        current_nodes.add(n)
        for nn in G.get_neighbors(n):
            current_nodes.add(nn)
    return current_nodes


def get_non_neighbors(G: Graph, node):
    return (G.get_nodes() - G.get_neighbors(node)) - {node}


def test_two_plex_graph(G: Graph):
    n = G.n
    for node in G.get_nodes():
        neighbors = G.get_neighbors(node)
        if len(neighbors) < n - 2:
            return False
    return True


def test_2_plex_nodes(g: Graph, nodes):
    n = len(nodes)
    for node in nodes:
        if len(g.get_neighbors(node) & nodes) < n - 2:
            return False
    return True


def greedy_plex(G: Graph):
    deg_sorting = degeneracy(G)[1]
    deg_sorting.reverse()
    current_plex = set()
    for node in deg_sorting:
        current_plex.add(node)
        if not test_2_plex_nodes(G, current_plex):
            current_plex.remove(node)
            return current_plex
    return current_plex


def two_plex_real(G: Graph):
    gp = greedy_plex(G)
    l = len(gp)
    l = 0
    # remove all nodes with degree <= l - 2
    nodes = G.get_nodes()
    for node in nodes:
        if G.get_node_degree(node) <= l - 2:
            G.remove_node(node)
    deg_sorting = degeneracy(G)[1]
    deg_sorting.reverse()

    for node in deg_sorting:
        new_G = G.copy_graph()
        tn = two_neighbors(new_G, node)

        # remove nodes that are not in the 2-neighborhood, since a two plex has to have diameter 2
        nodes = new_G.get_nodes()
        for n in nodes:
            if n not in tn:
                new_G.remove_node(n)
        # remove nodes that have not enough neighbors
        nodes = new_G.get_nodes()
        for n in nodes:
            if new_G.get_node_degree(n) <= l - 2:
                new_G.remove_node(n)

        # start recursion algorithm for the new Graph
        search_two_plex(copy.deepcopy(new_G), set())
        G.remove_node(node)


def search_two_plex(G, F):
    if len(G.get_nodes()) <= len(max_2_plex):
        return None

    if test_two_plex_graph(G):
        return G

    if len(F) > 1:
        l_f = list(F)
        possible_pairs = [(a, b) for idx, a in enumerate(l_f) for b in l_f[idx + 1:]]
        for u, v in possible_pairs:
            if not G.test_neighbors(u, v):
                # remove all non-neighbors from u and v
                not_neighbors_u = get_non_neighbors(G, u)
                not_neighbors_v = get_non_neighbors(G, v)
                if len(not_neighbors_u & F) > 0:
                    return None
                elif len(not_neighbors_v & F) > 0:
                    return None
                else:
                    for node in (not_neighbors_u | not_neighbors_v):
                        G.remove_node(node)

    deg_sorting = degeneracy(G)[1]
    v = deg_sorting[0]

    # case 1: v is not in G
    if v not in F:
        new_G = G.copy_graph()
        new_G.remove_node(v)
        search_two_plex(new_G, copy.deepcopy(F))

    # case 2: get not neighbors
    F.add(v)
    not_neighbors = get_non_neighbors(G, v)
    if len(not_neighbors & F) < 1:
        for u in not_neighbors:
            # case 2.1: u is not inside maximum plex
            new_G = G.copy_graph()
            new_G.remove_node(u)
            search_two_plex(new_G, copy.deepcopy(F))

            # case 2.2: u is inside -> all others are not
            F.add(u)
            for nn in not_neighbors:
                if nn != u:
                    G.remove_node(nn)
            search_two_plex(G, F)
            break
    return None


# G = Graph("../../networks/out.ucidata-zachary_")
max_2_plex = set()
