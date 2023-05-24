import src.triangleAlgorithms as tri
import time
import os
from src.Graph import Graph
import matplotlib.pyplot as plt
import random
import networkx as nx


class TestTriangleImplementationPowerNetworks:
    def __init__(self, functions, names, netx=None):
        self.functions = functions
        self.netx = netx
        self.times = None
        self.names = names

    def run(self):
        self.times = []
        path = "../../networks/power_networks/"
        files = [path + entry for entry in list(os.listdir(path))]

        counter = 0
        iterations = 1
        for function in self.functions:
            if counter in self.netx:
                start = time.time()
                for file in files:
                    with open(file, "r") as f:
                        G = nx.Graph()
                        for line in f:
                            G.add_edge(line[0], line[1])
                        for _ in range(iterations):
                            function(G)
            else:
                start = time.time()

                for file in files:
                    G = Graph(file)
                    for _ in range(iterations):
                        function(G)
            counter += 1
            time_dif = time.time() - start
            self.times.append(time_dif / iterations)

    def plot_and_run(self, colors=None):
        self.run()

        if colors is None or len(colors) != len(self.times):
            colors = []
            for _ in range(len(self.times)):
                r = random.random()
                g = random.random()
                b = random.random()
                colors.append([r, g, b])

        plt.bar([i for i in range(len(self.times))], self.times, label=self.names, width=0.4, color=colors)
        plt.legend(loc="lower center", bbox_to_anchor=(0, 0, 1, 2), ncol=2, bbox_transform=plt.gcf().transFigure)
        plt.show()


test = TestTriangleImplementationPowerNetworks([tri.algorithm_node_iterator,
                                                tri.algorithm_with_combinations,
                                                tri.algorithm_node_iterator_degeneracy_sorting,
                                                nx.triangles],
                                               ["Node Iterator", "using combinations",
                                                "Node Iterator, degeneracy", "networkX"], [3])
test.plot_and_run()
