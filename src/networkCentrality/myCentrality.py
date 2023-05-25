import numpy as np
from src.Graph import Graph
import src.shortestPaths as Sp


class OwnCentrality:
    def __init__(self, G: Graph):
        self.G = G

    def single_node_centrality(self, v):
        """
        compute centrality of node with external id v

        :param v:
        :return:
        """
        v = str(v)
        distances = Sp.single_source_shortest_path(self.G, v)
        node_degrees = dict()
        for node in self.G.node_ids_internal_ids:
            node_degrees[node] = self.G.get_node_degree(node)

        node_centrality = 0
        for w in distances:
            if w != v:
                node_centrality += node_degrees[w] * (1/distances[w]**2)
        return node_centrality

    def _init_nodes_centrality(self):
        node_degrees = dict()
        for node in self.G.node_ids_internal_ids:
            node_degrees[node] = self.G.get_node_degree(node)
        return node_degrees

    def all_nodes_centrality(self, i=1):
        distances = Sp.all_pairs_shortest_path_single(self.G)
        initial_centralities = self._init_nodes_centrality()

        for _ in range(i):
            new_centralities = dict()
            for node in initial_centralities:
                new_centralities[node] = 0
                distances_current = distances[node]
                for v in distances_current:
                    if v != node:
                        new_centralities[node] += initial_centralities[v] * (1 / distances_current[v]**2)
            initial_centralities = new_centralities
        return initial_centralities

    def most_central_node(self, i=1):
        result = self.all_nodes_centrality(i)
        max_centrality = 0
        most_central_nodes = []
        eps = np.finfo(float).eps
        for node in result:
            if result[node] > max_centrality:
                max_centrality = result[node]
                most_central_nodes = [node]
            elif max_centrality - eps < result[node] < max_centrality + eps:
                most_central_nodes.append(node)
        return most_central_nodes

    def k_central_nodes(self, k, i=1):
        k_central_nodes = []
        centralities = []
        result = self.all_nodes_centrality(i)

        for node in result:
            centrality = result[node]
            if len(k_central_nodes) < k:
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
        return k_central_nodes, centralities

