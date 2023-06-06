import numpy as np
from src.Graph import Graph

def von_mises_iteration(matrix: np.array,num_iterations: int):
    """
    :param matrix: A symetric numpy array
    :param num_iterations: number of iterations to find the eigenvector if the matrix
    :return: eigenvetor of the matrix with the larges eigenvalue
    """
    eigenvector = np.random.rand(matrix.shape[0])

    #Eigenvector
    for _ in range(num_iterations):

        matrix_x = matrix.dot(eigenvector)
        eigenvector = matrix_x/np.linalg.norm(matrix_x)

    #Eigenvalue : Rayleigh quotient
    #Eigenvalue = np.dot(np.transpose(Eigenvector),matrix_x)/np.dot(np.transpose(Eigenvector),Eigenvector)
    return eigenvector

def eigenvector_of_adjacence(G: Graph):
    """
    :param G: The graph object.
    :return: The eigenvector of the Adjacence-Matrix of G as dict with the node and eigenvator-values Pairs
    """
    eigenvector = dict()
    adjacency_matrix, new_mapping, new_mapping_back = G.get_adjacency_matrix()

    for idx, elm in enumerate(von_mises_iteration(adjacency_matrix, 20)):
        eigenvector[new_mapping_back[idx]] = elm

    return eigenvector

def eigenvector_centrality(G: Graph, node = None, k = None):
    """
        Calculates the eigenvector centrality for nodes in a graph using the eigenvector with the max eigenvalue of the Adjacency-matrix of G.

        Parameters:
            - G (Graph): The graph object.
            - node (int, optional): The node ID for which to calculate the eigenvector centrality. If provided, the function returns the eigenvector centrality for the specified node.
            - k (int, optional): The number of top central nodes to calculate eigenvector centrality for. If provided, the function returns a dictionary containing the top-k nodes and their corresponding eigenvector centralities.

        Returns:
            - If node is provided: The eigenvector centrality for the specified node.
            - If k is provided: A dictionary containing the top-k central nodes and their corresponding eigenvector centralities.
            - If neither node nor k is provided: A dictionary containing the eigenvector centrality for all nodes in the graph.
        """

    if k and node:
        raise Exception("invalid combination of arguments: You can either get top-k central nodes or centrality for one specific node")
    if k != None and k > G.n:
        raise Exception("invalid argument k: The Number of Nodes in G is less than k")
    if node != None and str(node) not in G.get_nodes():
        raise Exception("invalid argument node: Node is not in G")

    if node:
        eigenvector = eigenvector_of_adjacence(G)
        return eigenvector[str(node)]

    if k:
        eigenvector = eigenvector_of_adjacence(G)
        centrality = dict(sorted(eigenvector.items(), key=lambda item: item[1])[-k:])
        return centrality
    return eigenvector_of_adjacence(G)

