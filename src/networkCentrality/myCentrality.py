from src.Graph import Graph
from src.shortestPaths import all_pairs_shortest_path


class OwnCentrality:
    def __init__(self, G: Graph):
        self.G = G

    def node_centrality(self, v):
        """
        compute centrality of node with external id v

        :param v:
        :return:
        """
        distances = all_pairs_shortest_path(self.G)
        print(distances)
