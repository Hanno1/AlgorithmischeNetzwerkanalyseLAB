from src.Graph import Graph
import src.shortestPaths as Sp
import random


def ownCentrality(G: Graph, p=2, init=None, k_uniform_nodes=None, node=None, k=None):
    """
    computes my own Centrality for the given parameters
    There is a fast Mode, since it might be impractical to compute n BFS's there we approximate the centrality
    by using the distances to k_uniform_nodes which are uniformly chosen from the Graph G.

    :param G: Graph Object
    :param p: power of centrality scaling
    :param init: initial centrality as a dictionary, if this is None, all centrality will be set to 0
    :param k_uniform_nodes: if we want to make the algorithm fast, we will use only k_uniform_nodes, instead of all
    :param node: if this is not None, the algorithm will return the centrality of the given node
    :param k: if this is not None, the algorithm will return the nodes
    :return: - if node is provided: Centrality of the given node
    - if k is provided: top k central nodes with the centrality
    - neither k nor node -> Dictionary with all centrality
    """
    if node and k:
        raise Exception("Invalid combination of Arguments: Either get top k nodes or centrality for one specific node.")

    # given initial value?
    if init is not None:
        initial_centrality = init
    else:
        initial_centrality = dict()
        for v in G.node_ids_internal_ids:
            initial_centrality[v] = 1

    distances = dict()
    # fast or slow mode
    if k_uniform_nodes:
        fast = True
        all_nodes = list(G.node_ids_internal_ids.keys())
        # choose uniform k_centrality nodes
        for _ in range(k_uniform_nodes):
            v = random.choice(all_nodes)
            distances[v] = Sp.single_source_shortest_path(G, v)
    else:
        fast = False
        distances = Sp.all_pairs_shortest_path_single(G)

    if node and not k:
        return _single_node_centrality(fast, node, distances, initial_centrality, p)
    elif k and not node:
        return _k_central_nodes(k, fast, distances, initial_centrality, p)
    return _all_nodes_centrality(fast, distances, initial_centrality, p)


def _single_node_centrality_fast(v, distances, initial_centrality, p):
    """
    :param v: node for which to compute the single node centrality
    :return: node centrality of v

    compute the node centrality of v in fast mode - meaning we will only look at the distances from
    the k nodes we uniformly drew
    """
    node_centrality = 0
    for node in distances:
        if node != v and v in distances[node]:
            node_centrality += initial_centrality[node] * (1 / distances[node][v] ** p)
    return node_centrality


def _single_node_centrality_slow(v, distances, initial_centrality, p):
    """
    :param v: node for which to compute the single node centrality
    :return: node centrality of v

    compute the node centrality of v in slow mode - here v is in self.distances and can be accessed
    """
    node_centrality = 0
    actual_distances = distances[v]
    for node in actual_distances:
        if node != v:
            node_centrality += initial_centrality[node] * (1 / actual_distances[node] ** p)
    return node_centrality


def _single_node_centrality(fast, v, distances, initial_centrality, p):
    """
    compute centrality of node with external id v

    :param v: node v for which to compute shortest paths
    :return: centrality of node v
    """
    v = str(v)
    if fast:
        if v in distances:
            return _single_node_centrality_slow(v, distances, initial_centrality, p)
        return _single_node_centrality_fast(v, distances, initial_centrality, p)
    return _single_node_centrality_slow(v, distances, initial_centrality, p)


def _all_nodes_centrality(fast, distances, initial_centrality, p):
    """
    :return: dictionary containing all nodes centrality

    computes the node centrality of all nodes in G using the private functions for single node centrality
    """
    new_centrality = dict()
    if fast:
        for node in initial_centrality:
            if node in distances:
                new_centrality[node] = _single_node_centrality_slow(node, distances, initial_centrality, p)
            else:
                new_centrality[node] = _single_node_centrality_fast(node, distances, initial_centrality, p)
        return new_centrality
    for node in initial_centrality:
        new_centrality[node] = _single_node_centrality_slow(node, distances, initial_centrality, p)
    return new_centrality


def _k_central_nodes(k, fast, distances, initial_centrality, p):
    """
    :param k: number of nodes to return
    :return: number and centralities of the k most central nodes
    """
    k_central_nodes = []
    centralities = []
    result = _all_nodes_centrality(fast, distances, initial_centrality, p)

    additional_nodes = []
    additional_centrality = 0

    for node in result:
        centrality = result[node]
        if len(k_central_nodes) < k:
            # insert new node, but at the right place, so that the list is still sorted
            inserted = False
            for index in range(len(k_central_nodes)):
                if centrality < centralities[index]:
                    k_central_nodes.insert(index, node)
                    centralities.insert(index, centrality)
                    inserted = True
                    break
            if not inserted:
                k_central_nodes.append(centrality)
                centralities.append(centrality)
        else:
            if centrality > centralities[0]:
                k_central_nodes.pop(0)
                centralities.pop(0)

                inserted = False
                for index in range(len(k_central_nodes)):
                    if centrality < centralities[index]:
                        k_central_nodes.insert(index, node)
                        centralities.insert(index, centrality)
                        inserted = True
                        break
                if not inserted:
                    k_central_nodes.append(node)
                    centralities.append(centrality)

                if centralities[0] > additional_centrality:
                    additional_nodes = []
            if centrality == centralities[0]:
                additional_centrality = centrality
                additional_nodes.append(node)
    # if we want a exact result, it may contain more than k nodes
    """return additional_nodes + k_central_nodes, \
           [additional_centrality for _ in range(len(additional_nodes))] + centralities"""
    return k_central_nodes, centralities
