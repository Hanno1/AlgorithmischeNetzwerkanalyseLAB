from src.Graph import Graph
import src.shortestPaths as Sp
import random


class OwnCentrality:
    def __init__(self, G: Graph, p=2, init=None, k_uniform_nodes=None):
        """
        :param G: Graph
        :param p: power value, the distances will be scaled with this
        :param init: initial centrality as a dictionary, if this is None, all centrality will be set to 0
        :param k_uniform_nodes: if we want to make the algorithm fast, we will use only k_uniform_nodes, instead of all

        Class to compute centrality of a given graph. The centrality for a node is computed by summing the product
        of the centrality and the distance to the power of p of all connected nodes

        There is a fast Mode, since it might be impractical to compute n BFS's there we approximate the centrality
        by using the distances to k_uniform_nodes which are uniformly chosen from the Graph G.
        """
        self.G = G
        self.p = p
        if k_uniform_nodes is None:
            self.fast = False
            self.distances = Sp.all_pairs_shortest_path_single(self.G)
        else:
            self.fast = True
            # we cant use internal id since there might be gaps in between
            all_nodes = list(G.node_ids_internal_ids.keys())
            # choose uniform k_centrality nodes
            self.distances = dict()
            for _ in range(k_uniform_nodes):
                node = random.choice(all_nodes)
                self.distances[node] = Sp.single_source_shortest_path(self.G, node)

        if init is not None:
            self.initial_centrality = init
        else:
            self.initial_centrality = dict()
            for node in self.G.node_ids_internal_ids:
                self.initial_centrality[node] = 1

    def _single_node_centrality_fast(self, v):
        """
        :param v: node for which to compute the single node centrality
        :return: node centrality of v

        compute the node centrality of v in fast mode - meaning we will only look at the distances from
        the k nodes we uniformly drew
        """
        node_centrality = 0
        for node in self.distances:
            if node != v and v in self.distances[node]:
                node_centrality += self.initial_centrality[node] * (1 / self.distances[node][v] ** self.p)
        return node_centrality

    def _single_node_centrality_slow(self, v):
        """
        :param v: node for which to compute the single node centrality
        :return: node centrality of v

        compute the node centrality of v in slow mode - here v is in self.distances and can be accessed
        """
        node_centrality = 0
        actual_distances = self.distances[v]
        for node in actual_distances:
            if node != v:
                node_centrality += self.initial_centrality[node] * (1 / actual_distances[node] ** self.p)
        return node_centrality

    def single_node_centrality(self, v):
        """
        compute centrality of node with external id v

        :param v: node v for which to compute shortest paths
        :return: centrality of node v
        """
        v = str(v)
        if self.fast:
            if v in self.distances:
                return self._single_node_centrality_slow(v)
            return self._single_node_centrality_fast(v)
        return self._single_node_centrality_slow(v)

    def all_nodes_centrality(self):
        """
        :return: dictionary containing all nodes centrality

        computes the node centrality of all nodes in G using the private functions for single node centrality
        """
        new_centrality = dict()
        if self.fast:
            for node in self.initial_centrality:
                if node in self.distances:
                    new_centrality[node] = self._single_node_centrality_slow(node)
                else:
                    new_centrality[node] = self._single_node_centrality_fast(node)
            return new_centrality
        for node in self.initial_centrality:
            new_centrality[node] = self._single_node_centrality_slow(node)
        return new_centrality

    def most_central_node(self):
        """
        :return: the most central node and the corresponding centrality - it will return all nodes with the maximal
        centrality
        """
        result = self.all_nodes_centrality()

        max_centrality = 0
        most_central_nodes = []
        for node in result:
            current_centr = round(result[node], 4)
            if current_centr > max_centrality:
                max_centrality = current_centr
                most_central_nodes = [node]
            elif current_centr == max_centrality:
                most_central_nodes.append(node)
        return most_central_nodes, max_centrality

    def k_central_nodes(self, k):
        """
        :param k: number of nodes to return
        :return: number and centralities of the k most central nodes
        """
        k_central_nodes = []
        centralities = []
        result = self.all_nodes_centrality()

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
