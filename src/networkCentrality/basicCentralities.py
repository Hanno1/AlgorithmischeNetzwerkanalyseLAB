from src.Graph import Graph
from src.shortestPaths import all_pairs_shortest_path, single_source_shortest_path, connected_components
import random
import numpy as np

def closeness_centrality_approx(G: Graph, k_approx = None, k = None):
    """
    Approximates the closeness centrality for nodes in a graph using random sampling.
    In case the graph has multiple components, the harmonic centrality is calculated.

    Parameters:
        G (Graph): The graph object for which closeness centrality is to be approximated.
        k_approx (int, optional): The number of nodes to sample for approximation. if not provided, the function
            uses the square root of the number of nodes in the graph.
            in case k_approx is larger then the number of nodes in the Graph, the regular closeness_centrality is used.
        k (int, optional): The number of top nodes to return. Default is None, which returns centrality values for all nodes.

    Returns:
        dict or None: A dictionary containing closeness centrality values for nodes in the graph.
            If k is provided, returns a dictionary with the top-k nodes and their centrality values.
            If k is not provided, returns a dictionary with centrality values for all nodes.

    Note:
        This function uses random sampling to approximate closeness centrality.
        The approximation is based on the shortest paths from the sampled nodes to all other nodes in the graph.
        If k is provided, the function returns the top-k nodes with the highest centrality values.

    """
    node_ids = list(G.node_ids_internal_ids.keys())
    if not k_approx:
        k_approx = max(int(np.sqrt(G.n)), 10) # choosing a "moderate amount" of nodes. just an estimation

    if k_approx>=G.n:
        return closeness_centrality(G, k = k)

    k_choices =  random.choices(node_ids, k=k_approx)

    all_shortest_paths = {}
    for n in k_choices:
        all_shortest_paths[n] = single_source_shortest_path(G,n)

    node_centralities={}
    cc = connected_components(G)
    avg = np.zeros(G.n)
    if len(cc)>1:
        for n in k_choices:
            shortest_paths = all_shortest_paths[n]
            node_centralities[n]=sum([1/d if d >0 else 0 for d in shortest_paths.values()])/(G.n-1)
            for node_d in node_ids:
                if node_d in shortest_paths and node_d != n:
                    avg[node_ids.index(node_d)] += 1/shortest_paths[node_d]
        avg = avg/k_approx

    else:
        for n in k_choices:
            shortest_paths = single_source_shortest_path(G,n)
            node_centralities[n]=(G.n-1)/sum(shortest_paths.values())
            avg += np.array([shortest_paths[node] for node in node_ids])
        avg = k_approx/avg

    for n in set(G.node_ids_internal_ids)-node_centralities.keys(): # not-chosen nodes
        idx = node_ids.index(n)
        node_centralities[n] = avg[idx]
    
    if k:
        top_k_nodes = sorted(node_centralities, key=node_centralities.get, reverse=True)[:k]
        top_k_centralities = {node: node_centralities[node] for node in top_k_nodes}
        return top_k_centralities

    return node_centralities


def closeness_centrality(G: Graph, node = None, k = None):
    """
    Calculate closeness centrality for nodes in a graph.
    In case the graph has multiple components, the harmonic centrality is calculated.

    Parameters:
    - G (Graph): The graph object.
    - node (int, optional): The node ID for which to calculate the closeness centrality. If provided, the function returns the closeness centrality for the specified node.
    - k (int, optional): The number of top central nodes to calculate closeness centrality for. If provided, the function returns a dictionary containing the top-k nodes and their corresponding closeness centralities.

    Returns:
    - If node is provided: The closeness centrality for the specified node.
    - If k is provided: A dictionary containing the top-k central nodes and their corresponding closeness centralities.
    - If neither node nor k is provided: A dictionary containing the closeness centrality for all nodes in the graph.
    """
    if k and node:
        raise Exception("invalid combination of arguments: You can either get top-k central nodes or centrality for one specific node")
    if node:
        shortest_paths = single_source_shortest_path(G,node)
        if len(shortest_paths)<G.n:
            return sum([1/d if d >0 else 0 for d in shortest_paths.values()])/(G.n-1)
        else:
            return (G.n-1)/sum(shortest_paths.values())
    all_shortest_paths = all_pairs_shortest_path(G)
    node_centralities = {}
    if len(next(iter(all_shortest_paths.values())))< G.n: #harmonic centrality for multi-component graphs
        for n in all_shortest_paths:
            shortest_paths= all_shortest_paths[n]
            node_centralities[n]=sum([1/d if d >0 else 0 for d in shortest_paths.values()])/(G.n-1)
    else:
        for n in all_shortest_paths:
            shortest_paths= all_shortest_paths[n]
            node_centralities[n]=(G.n-1)/sum(shortest_paths.values())
    if k:
        top_k_nodes = sorted(node_centralities, key=node_centralities.get, reverse=True)[:k]
        top_k_centralities = {node: node_centralities[node] for node in top_k_nodes}
        return top_k_centralities
    return node_centralities

def degree_centrality(G: Graph, node = None, k = None):
    """
    Calculate degree centrality for nodes in a graph.

    Parameters:
    - G (Graph): The graph object.
    - node (int, optional): The node ID for which to calculate the degree centrality. If provided, the function returns the degree centrality for the specified node.
    - k (int, optional): The number of top central nodes to calculate degree centrality for. If provided, the function returns a dictionary containing the top-k nodes and their corresponding degree centralities.

    Returns:
    - If node is provided: The degree centrality for the specified node.
    - If k is provided: A dictionary containing the top-k central nodes and their corresponding degree centralities.
    - If neither node nor k is provided: A dictionary containing the degree centrality for all nodes in the graph.
    """
    if k and node:
        raise Exception("invalid combination of arguments: You can either get top-k central nodes or centrality for one specific node")
    if node:
        return len(G.get_internal_neighbors(G.node_ids_internal_ids[node]))

    node_centralities = {}
    for n in G.node_ids_internal_ids:
        n_internal = G.node_ids_internal_ids[n]
        c = len(G.get_internal_neighbors(n_internal))
        node_centralities[n] = c/(G.n-1)
    if k:
        top_k_nodes = sorted(node_centralities, key=node_centralities.get, reverse=True)[:k]
        top_k_centralities = {node: node_centralities[node] for node in top_k_nodes}
        return top_k_centralities
    return node_centralities
