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
            actual_nodes |= not_neighbors
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
            permanent.remove(v)
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
                #permanent.add(u)
                actual_nodes.add(u)
                res = _search_2_plex_rec_first(orig_graph, actual_nodes, permanent, max_2_plex)
                if res:
                    max_2_plex = res
                actual_nodes.remove(u)
                #permanent.remove(u)
            actual_nodes |= not_neighbors
            permanent.remove(v)
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
            permanent.remove(v)
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
            actual_nodes |= not_neighbors
            permanent.remove(v)
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
            permanent.remove(v)
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
            actual_nodes |= not_neighbors
            permanent.remove(v)
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
            permanent.remove(v)
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
            actual_nodes |= not_neighbors
            permanent.remove(v)
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
    actual_nodes = (working_set | permanent) - remove
    current_n = len(actual_nodes)
    for u in actual_nodes - permanent:
        neighbors_v = orig_graph.get_neighbors(u) & actual_nodes
        if len(neighbors_v) >= current_n - 2:
            permanent.add(u)
            res = _search_2_plex_rec_test(orig_graph, all_distances, actual_nodes, permanent, max_2_plex)
            if res:
                max_2_plex = res
            permanent.remove(u)
        else:
            # case 1 - v is not in the 2-plex
            actual_nodes.remove(u)
            res = _search_2_plex_rec_test(orig_graph, all_distances, actual_nodes, permanent, max_2_plex)
            if res:
                max_2_plex = res
            actual_nodes.add(u)

            # case 2 - v is in 2-plex and therefore permanent
            permanent.add(u)

            not_neighbors = actual_nodes - (neighbors_v | {u})
            counter = 0
            for n in not_neighbors:
                if n not in permanent:
                    if counter <= 1:
                        # n is not inside
                        actual_nodes.remove(n)
                        res = _search_2_plex_rec_test(orig_graph, all_distances, actual_nodes, permanent, max_2_plex)
                        if res:
                            max_2_plex = res
                        actual_nodes.add(n)
                    elif counter == 2:
                        break
                    counter += 1

            permanent.remove(u)
        break
    return max_2_plex


def _search_2_plex_rec_test2(orig_graph: Graph, all_distances, possible_nodes, permanent, max_2_plex):
    all_nodes = possible_nodes | permanent
    if test_2_plex(orig_graph, all_nodes):
        print(all_nodes)
        return
    # choose node from possible nodes
    current_n = len(all_nodes)
    for v in possible_nodes:
        neighbors = orig_graph.get_neighbors(v) & (permanent | possible_nodes)
        not_neighbors = possible_nodes - (neighbors | {v})

        if len(neighbors) >= current_n-2:
            permanent.add(v)
            possible_nodes.remove(v)

            _search_2_plex_rec_test2(orig_graph, all_distances, possible_nodes, permanent, max_2_plex)

            permanent.remove(v)
            possible_nodes.add(v)
            break

        # case 1: v is not inside
        possible_nodes.remove(v)
        _search_2_plex_rec_test2(orig_graph, all_distances, possible_nodes, permanent, max_2_plex)

        # case 2: v is inside, meaning one of the not neighbors is not
        permanent.add(v)

        counter = 0
        for u in not_neighbors:
            if counter == 2:
                break
            if u not in permanent:
                possible_nodes.remove(u)
                _search_2_plex_rec_test2(orig_graph, all_distances, possible_nodes, permanent, max_2_plex)
                possible_nodes.add(u)
                counter += 1

        possible_nodes.add(v)
        permanent.remove(v)

        break
