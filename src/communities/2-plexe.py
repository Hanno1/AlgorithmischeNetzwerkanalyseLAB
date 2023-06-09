import copy

from src.Graph import Graph
import test_.HelperClass as Hc


def test_2_plex(g: Graph, nodes):
    n = len(nodes)
    for node in nodes:
        if len(g.get_neighbors(node) & nodes) < n-2:
            return False
    return True


def filter_2_plex(list_):
    maximal_length = 0
    for g in list_:
        if len(g) > maximal_length:
            maximal_length = len(g)
    for g in list_:
        if len(g) == maximal_length:
            return g


def search_2_plex_rec(orig_graph: Graph, actual_nodes, permanent, max_2_plex):
    current_n = len(actual_nodes)
    if current_n <= len(max_2_plex):
        return None
    if test_2_plex(orig_graph, actual_nodes):
        if current_n > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None
    for v in actual_nodes:
        neighbors_v = orig_graph.get_neighbors(v) & actual_nodes
        if v not in permanent and len(neighbors_v) < current_n - 2:
            actual_nodes.remove(v)
            res = search_2_plex_rec(orig_graph, actual_nodes, permanent, max_2_plex)
            if res:
                max_2_plex = res
            actual_nodes.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            permanent.append(v)

            not_neighbors = actual_nodes - (neighbors_v | {v})
            actual_nodes = neighbors_v | {v}
            # none of the not neighbors
            res = search_2_plex_rec(orig_graph, actual_nodes, permanent, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                actual_nodes.add(u)
                res = search_2_plex_rec(orig_graph, actual_nodes, permanent, max_2_plex)
                if res:
                    max_2_plex = res
                actual_nodes.remove(u)

            # in the top the path can be still possible
            permanent.remove(v)
            break
    return max_2_plex


G = Graph("../../networks/out.ucidata-zachary_")

print(search_2_plex_rec(G, G.get_nodes(), [], []))
