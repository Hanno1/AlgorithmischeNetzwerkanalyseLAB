import copy

from src.Graph import Graph
import src.shortestPaths as Sp


def test_2_plex(g: Graph, nodes):
    n = len(nodes)
    for node in nodes:
        if len(g.get_neighbors(node) & nodes) < n-2:
            return False
    return True


def search_2_plex_rec_orig(orig_graph: Graph, actual_nodes, max_2_plex):
    current_n = len(actual_nodes)
    if test_2_plex(orig_graph, actual_nodes):
        if len(actual_nodes) > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None
    for v in actual_nodes:
        neighbors_v = orig_graph.get_neighbors(v) & actual_nodes
        if len(neighbors_v) < current_n - 2:
            actual_nodes.remove(v)

            res = search_2_plex_rec_orig(orig_graph, actual_nodes, max_2_plex)
            if res:
                max_2_plex = res

            actual_nodes.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            not_neighbors = actual_nodes - (neighbors_v | {v})
            actual_nodes = neighbors_v | {v}
            # none of the not neighbors
            res = search_2_plex_rec_orig(orig_graph, actual_nodes, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                actual_nodes.add(u)
                res = search_2_plex_rec_orig(orig_graph, actual_nodes, max_2_plex)
                if res:
                    max_2_plex = res
                actual_nodes.remove(u)
            break
    return max_2_plex


def search_2_plex_rec_first(orig_graph: Graph, actual_nodes, permanent, max_2_plex):
    current_n = len(actual_nodes)
    if test_2_plex(orig_graph, actual_nodes):
        if current_n > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None
    for v in actual_nodes - set(permanent):
        neighbors_v = orig_graph.get_neighbors(v) & actual_nodes
        if len(neighbors_v) == current_n - 1:
            permanent.append(v)
            search_2_plex_rec_first(orig_graph, actual_nodes, permanent, max_2_plex)
            permanent.remove(v)
        elif len(neighbors_v) < current_n - 2:
            actual_nodes.remove(v)
            res = search_2_plex_rec_first(orig_graph, actual_nodes, permanent, max_2_plex)
            if res:
                max_2_plex = res
            actual_nodes.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            permanent.append(v)

            not_neighbors = actual_nodes - (neighbors_v | {v})
            actual_nodes = neighbors_v | {v}
            # none of the not neighbors
            res = search_2_plex_rec_first(orig_graph, actual_nodes, permanent, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                actual_nodes.add(u)
                res = search_2_plex_rec_first(orig_graph, actual_nodes, permanent, max_2_plex)
                if res:
                    max_2_plex = res
                actual_nodes.remove(u)

            # in the top the path can be still possible
            permanent.remove(v)
            break
    return max_2_plex


def search_2_plex_rec_second(orig_graph: Graph, all_distances, actual_nodes, permanent, max_2_plex):
    current_n = len(actual_nodes)
    if test_2_plex(orig_graph, actual_nodes):
        if current_n > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None

    # second improvement -> remove nodes with distance of at least 3 from any permanent node
    working_set = actual_nodes - set(permanent)
    remove = set()
    for node in working_set:
        for permanent_node in permanent:
            if all_distances[node][permanent_node] >= 3:
                remove.add(node)
    working_set = (working_set | set(permanent)) - remove
    current_n = len(working_set)
    for v in working_set - set(permanent):
        neighbors_v = orig_graph.get_neighbors(v) & working_set
        if len(neighbors_v) == current_n - 1:
            permanent.append(v)
            search_2_plex_rec_second(orig_graph, all_distances, working_set, permanent, max_2_plex)
            permanent.remove(v)
        elif len(neighbors_v) < current_n - 2:
            working_set.remove(v)
            res = search_2_plex_rec_second(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
            working_set.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            permanent.append(v)

            not_neighbors = working_set - (neighbors_v | {v})
            working_set = neighbors_v | {v}
            # none of the not neighbors
            res = search_2_plex_rec_second(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                working_set.add(u)
                res = search_2_plex_rec_second(orig_graph, all_distances, working_set, permanent, max_2_plex)
                if res:
                    max_2_plex = res
                working_set.remove(u)

            # in the top the path can be still possible
            permanent.remove(v)
            break
    return max_2_plex


def search_2_plex_rec_third(orig_graph: Graph, all_distances, actual_nodes, permanent, max_2_plex):
    current_n = len(actual_nodes)

    # third improvement
    if len(actual_nodes) <= len(max_2_plex):
        return None

    if test_2_plex(orig_graph, actual_nodes):
        if current_n > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None

    # second improvement -> remove nodes with distance of at least 3 from any permanent node
    working_set = actual_nodes - set(permanent)
    remove = set()
    for node in working_set:
        for permanent_node in permanent:
            if all_distances[node][permanent_node] >= 3:
                remove.add(node)
    working_set = (working_set | set(permanent)) - remove
    current_n = len(working_set)
    for v in working_set - set(permanent):
        neighbors_v = orig_graph.get_neighbors(v) & working_set
        if len(neighbors_v) == current_n - 1:
            permanent.append(v)
            search_2_plex_rec_third(orig_graph, all_distances, working_set, permanent, max_2_plex)
            permanent.remove(v)
        elif len(neighbors_v) < current_n - 2:
            working_set.remove(v)
            res = search_2_plex_rec_third(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
            working_set.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            permanent.append(v)

            not_neighbors = working_set - (neighbors_v | {v})
            working_set = neighbors_v | {v}
            # none of the not neighbors
            res = search_2_plex_rec_third(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                working_set.add(u)
                res = search_2_plex_rec_third(orig_graph, all_distances, working_set, permanent, max_2_plex)
                if res:
                    max_2_plex = res
                working_set.remove(u)

            # in the top the path can be still possible
            permanent.remove(v)
            break
    return max_2_plex


def search_2_plex_rec_fourth(orig_graph: Graph, all_distances, actual_nodes, permanent, max_2_plex):
    current_n = len(actual_nodes)

    # third improvement
    if len(actual_nodes) <= len(max_2_plex):
        return None

    if test_2_plex(orig_graph, actual_nodes):
        if current_n > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None

    # second improvement -> remove nodes with distance of at least 3 from any permanent node
    working_set = actual_nodes - set(permanent)
    remove = set()
    for node in working_set:
        for permanent_node in permanent:
            if all_distances[node][permanent_node] >= 3:
                remove.add(node)
        # last improvement - remove nodes with at most len(max_2_plex) - 2 neighbors
        neighbors = orig_graph.get_neighbors(node) & working_set
        if len(neighbors) <= len(max_2_plex) - 2:
            remove.add(node)
    working_set = (working_set | set(permanent)) - remove
    current_n = len(working_set)
    for v in working_set - set(permanent):
        neighbors_v = orig_graph.get_neighbors(v) & working_set
        if len(neighbors_v) == current_n - 1:
            permanent.append(v)
            search_2_plex_rec_third(orig_graph, all_distances, working_set, permanent, max_2_plex)
            permanent.remove(v)
        elif len(neighbors_v) < current_n - 2:
            working_set.remove(v)
            res = search_2_plex_rec_third(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
            working_set.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            permanent.append(v)

            not_neighbors = working_set - (neighbors_v | {v})
            working_set = neighbors_v | {v}
            # none of the not neighbors
            res = search_2_plex_rec_third(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                working_set.add(u)
                res = search_2_plex_rec_third(orig_graph, all_distances, working_set, permanent, max_2_plex)
                if res:
                    max_2_plex = res
                working_set.remove(u)

            # in the top the path can be still possible
            permanent.remove(v)
            break
    return max_2_plex


G = Graph("../../networks/out.ucidata-zachary_")

all_pairs_shortest_paths = Sp.all_pairs_shortest_path_single(G)

print(search_2_plex_rec_orig(G, G.get_nodes(), []))
print(search_2_plex_rec_first(G, G.get_nodes(), [], []))
print(search_2_plex_rec_second(G, all_pairs_shortest_paths, G.get_nodes(), [], []))
print(search_2_plex_rec_third(G, all_pairs_shortest_paths, G.get_nodes(), [], []))
print(search_2_plex_rec_fourth(G, all_pairs_shortest_paths, G.get_nodes(), [], []))
