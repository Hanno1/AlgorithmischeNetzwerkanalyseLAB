import copy

from src.Graph import Graph
import src.shortestPaths as Sp


def test_2_plex(g: Graph, nodes):
    n = len(nodes)
    for node in nodes:
        if len(g.get_neighbors(node) & nodes) < n-2:
            return False
    return True


def search_2_plex(orig_graph: Graph, version=0):
    actual_nodes = orig_graph.get_nodes()
    if version == 0:
        res = _search_2_plex_rec_orig(orig_graph, actual_nodes, [])
    elif version == 1:
        res = _search_2_plex_rec_first(orig_graph, actual_nodes, set(), [])
    elif version == 2:
        all_distances = Sp.all_pairs_shortest_path_single(orig_graph)
        res = _search_2_plex_rec_second(orig_graph, all_distances, actual_nodes, set(), [])
    elif version == 3:
        all_distances = Sp.all_pairs_shortest_path_single(orig_graph)
        res = _search_2_plex_rec_third(orig_graph, all_distances, actual_nodes, set(), [])
    elif version == 4:
        all_distances = Sp.all_pairs_shortest_path_single(orig_graph)
        res = _search_2_plex_rec_fourth(orig_graph, all_distances, actual_nodes, set(), [])
    elif version == 5:
        all_distances = Sp.all_pairs_shortest_path_single(orig_graph)
        res = _search_2_plex_rec_test(orig_graph, all_distances, actual_nodes, set(), [])
    else:
        all_distances = Sp.all_pairs_shortest_path_single(orig_graph)
        res = _search_2_plex_rec_test2(orig_graph, all_distances, actual_nodes, set(), [])
    return res


def _search_2_plex_rec_orig(orig_graph: Graph, actual_nodes, max_2_plex):
    current_n = len(actual_nodes)
    if test_2_plex(orig_graph, actual_nodes):
        if len(actual_nodes) > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None
    for v in actual_nodes:
        neighbors_v = orig_graph.get_neighbors(v) & actual_nodes
        if len(neighbors_v) < current_n - 2:
            actual_nodes.remove(v)

            res = _search_2_plex_rec_orig(orig_graph, actual_nodes, max_2_plex)
            if res:
                max_2_plex = res

            actual_nodes.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            not_neighbors = actual_nodes - (neighbors_v | {v})
            actual_nodes = neighbors_v | {v}
            # none of the not neighbors
            res = _search_2_plex_rec_orig(orig_graph, actual_nodes, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                actual_nodes.add(u)
                res = _search_2_plex_rec_orig(orig_graph, actual_nodes, max_2_plex)
                if res:
                    max_2_plex = res
                actual_nodes.remove(u)
            break
    return max_2_plex


def _search_2_plex_rec_first(orig_graph: Graph, actual_nodes, permanent, max_2_plex):
    current_n = len(actual_nodes)
    if test_2_plex(orig_graph, actual_nodes):
        if current_n > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None
    for v in actual_nodes - permanent:
        neighbors_v = orig_graph.get_neighbors(v) & actual_nodes
        if len(neighbors_v) >= current_n - 2:
            permanent.add(v)
            res = _search_2_plex_rec_first(orig_graph, actual_nodes, permanent, max_2_plex)
            if res:
                max_2_plex = res
        else:
            actual_nodes.remove(v)
            res = _search_2_plex_rec_first(orig_graph, actual_nodes, permanent, max_2_plex)
            if res:
                max_2_plex = res
            actual_nodes.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            permanent.add(v)

            not_neighbors = actual_nodes - (neighbors_v | {v})
            actual_nodes = neighbors_v | {v}
            # none of the not neighbors
            res = _search_2_plex_rec_first(orig_graph, actual_nodes, permanent, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                actual_nodes.add(u)
                res = _search_2_plex_rec_first(orig_graph, actual_nodes, permanent, max_2_plex)
                if res:
                    max_2_plex = res
                actual_nodes.remove(u)
        break
    return max_2_plex


def _search_2_plex_rec_second(orig_graph: Graph, all_distances, actual_nodes, permanent, max_2_plex):
    current_n = len(actual_nodes)
    if test_2_plex(orig_graph, actual_nodes):
        if current_n > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None

    # second improvement -> remove nodes with distance of at least 3 from any permanent node
    working_set = actual_nodes - permanent
    remove = set()
    for node in working_set:
        for permanent_node in permanent:
            if permanent_node in all_distances[node]:
                if all_distances[node][permanent_node] >= 3:
                    remove.add(node)
            else:
                remove.add(node)
    working_set = (working_set | permanent) - remove
    current_n = len(working_set)
    for v in working_set - permanent:
        neighbors_v = orig_graph.get_neighbors(v) & working_set
        if len(neighbors_v) >= current_n - 2:
            permanent.add(v)
            res = _search_2_plex_rec_second(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
        else:
            working_set.remove(v)
            res = _search_2_plex_rec_second(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
            working_set.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            permanent.add(v)

            not_neighbors = working_set - (neighbors_v | {v})
            working_set = neighbors_v | {v}
            # none of the not neighbors
            res = _search_2_plex_rec_second(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                working_set.add(u)
                res = _search_2_plex_rec_second(orig_graph, all_distances, working_set, permanent, max_2_plex)
                if res:
                    max_2_plex = res
                working_set.remove(u)
        break
    return max_2_plex


def _search_2_plex_rec_third(orig_graph: Graph, all_distances, actual_nodes, permanent, max_2_plex):
    current_n = len(actual_nodes)

    # third improvement
    if len(actual_nodes) <= len(max_2_plex):
        return None

    if test_2_plex(orig_graph, actual_nodes):
        if current_n > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None

    # second improvement -> remove nodes with distance of at least 3 from any permanent node
    working_set = actual_nodes - permanent
    remove = set()
    for node in working_set:
        for permanent_node in permanent:
            if permanent_node in all_distances[node]:
                if all_distances[node][permanent_node] >= 3:
                    remove.add(node)
            else:
                remove.add(node)
    working_set = (working_set | permanent) - remove
    current_n = len(working_set)
    for v in working_set - permanent:
        neighbors_v = orig_graph.get_neighbors(v) & working_set
        if len(neighbors_v) >= current_n - 2:
            permanent.add(v)
            res = _search_2_plex_rec_third(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
        else:
            working_set.remove(v)
            res = _search_2_plex_rec_third(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
            working_set.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            permanent.add(v)

            not_neighbors = working_set - (neighbors_v | {v})
            working_set = neighbors_v | {v}
            # none of the not neighbors
            res = _search_2_plex_rec_third(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                working_set.add(u)
                res = _search_2_plex_rec_third(orig_graph, all_distances, working_set, permanent, max_2_plex)
                if res:
                    max_2_plex = res
                working_set.remove(u)
        break
    return max_2_plex


def _search_2_plex_rec_fourth(orig_graph: Graph, all_distances, actual_nodes, permanent, max_2_plex):
    current_n = len(actual_nodes)

    # third improvement
    if len(actual_nodes) <= len(max_2_plex):
        return None

    if test_2_plex(orig_graph, actual_nodes):
        if current_n > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None

    # second improvement -> remove nodes with distance of at least 3 from any permanent node
    working_set = actual_nodes - permanent
    remove = set()
    for node in working_set:
        for permanent_node in permanent:
            if permanent_node in all_distances[node]:
                if all_distances[node][permanent_node] >= 3:
                    remove.add(node)
            else:
                remove.add(node)
        # last improvement - remove nodes with at most len(max_2_plex) - 2 neighbors
        neighbors = orig_graph.get_neighbors(node) & working_set
        if len(neighbors) <= len(max_2_plex) - 2:
            remove.add(node)
    working_set = (working_set | permanent) - remove
    current_n = len(working_set)
    for v in working_set - permanent:
        neighbors_v = orig_graph.get_neighbors(v) & working_set
        if len(neighbors_v) >= current_n - 2:
            permanent.add(v)
            res = _search_2_plex_rec_fourth(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
        else:
            working_set.remove(v)
            res = _search_2_plex_rec_fourth(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
            working_set.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            permanent.add(v)

            not_neighbors = working_set - (neighbors_v | {v})
            working_set = neighbors_v | {v}
            # none of the not neighbors
            res = _search_2_plex_rec_fourth(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                working_set.add(u)
                res = _search_2_plex_rec_fourth(orig_graph, all_distances, working_set, permanent, max_2_plex)
                if res:
                    max_2_plex = res
                working_set.remove(u)
        break
    return max_2_plex


def _search_2_plex_rec_test(orig_graph: Graph, all_distances, actual_nodes, permanent, max_2_plex):
    current_n = len(actual_nodes)

    # third improvement
    if len(actual_nodes) <= len(max_2_plex):
        return None

    if test_2_plex(orig_graph, actual_nodes):
        if current_n > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None

    # second improvement -> remove nodes with distance of at least 3 from any permanent node
    working_set = actual_nodes - permanent
    remove = set()
    for node in working_set:
        for permanent_node in permanent:
            if permanent_node in all_distances[node]:
                if all_distances[node][permanent_node] >= 3:
                    remove.add(node)
            else:
                remove.add(node)
        # last improvement - remove nodes with at most len(max_2_plex) - 2 neighbors
        neighbors = orig_graph.get_neighbors(node) & working_set
        if len(neighbors) <= len(max_2_plex) - 2:
            remove.add(node)
    working_set = (working_set | permanent) - remove
    current_n = len(working_set)
    for v in working_set - permanent:
        neighbors_v = orig_graph.get_neighbors(v) & working_set
        if len(neighbors_v) >= current_n - 2:
            working_set.remove(v)
            permanent.add(v)
            res = _search_2_plex_rec_test(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
        else:
            working_set.remove(v)
            res = _search_2_plex_rec_test(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
            working_set.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            permanent.add(v)

            not_neighbors = working_set - (neighbors_v | {v})
            working_set = neighbors_v | {v}
            # none of the not neighbors
            res = _search_2_plex_rec_test(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                working_set.add(u)
                res = _search_2_plex_rec_test(orig_graph, all_distances, working_set, permanent, max_2_plex)
                if res:
                    max_2_plex = res
                working_set.remove(u)
        break
    return max_2_plex


def _search_2_plex_rec_test2(orig_graph: Graph, all_distances, actual_nodes, permanent, max_2_plex):
    current_n = len(actual_nodes)

    # third improvement
    if len(actual_nodes) <= len(max_2_plex):
        return None

    if test_2_plex(orig_graph, actual_nodes):
        if current_n > len(max_2_plex):
            return copy.deepcopy(actual_nodes)
        return None

    # second improvement -> remove nodes with distance of at least 3 from any permanent node
    working_set = actual_nodes - permanent
    remove = set()
    for node in working_set:
        for permanent_node in permanent:
            if permanent_node in all_distances[node]:
                if all_distances[node][permanent_node] >= 3:
                    remove.add(node)
            else:
                remove.add(node)
        # last improvement - remove nodes with at most len(max_2_plex) - 2 neighbors
        neighbors = orig_graph.get_neighbors(node) & working_set
        if len(neighbors) <= len(max_2_plex) - 2:
            remove.add(node)
    working_set = (working_set | permanent) - remove
    current_n = len(working_set)
    for v in working_set - permanent:
        neighbors_v = orig_graph.get_neighbors(v) & working_set
        if len(neighbors_v) >= current_n - 2:
            working_set.remove(v)
            permanent.add(v)
            res = _search_2_plex_rec_test2(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
        else:
            working_set.remove(v)
            res = _search_2_plex_rec_test2(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res
            working_set.add(v)

            # case 2 - v is in 2-plex and therefore permanent
            permanent.add(v)

            not_neighbors = working_set - (neighbors_v | {v})
            working_set = neighbors_v | {v}
            # none of the not neighbors
            res = _search_2_plex_rec_test2(orig_graph, all_distances, working_set, permanent, max_2_plex)
            if res:
                max_2_plex = res

            # at most one of the not neighbors
            for u in not_neighbors:
                permanent.add(u)
                working_set.add(u)
                res = _search_2_plex_rec_test2(orig_graph, all_distances, working_set, permanent, max_2_plex)
                if res:
                    max_2_plex = res
                working_set.remove(u)
                permanent.remove(u)
        break
    return max_2_plex
