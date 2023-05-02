import time
import random
from src.Graph import Graph
import matplotlib.pyplot as plt
import networkx as nx
import src.shortestPaths as sp
from tqdm import tqdm


class GraphPerformanceTester:
    def __init__(self, sizes=[100, 500, 1000], iters=3, graph_density=0.5):
        self.iters = iters
        self.graph_sizes = sizes  # list of graph sizes to test
        self.rand_edge_density = graph_density
        self.num_iterations = iters  # number of times to repeat each test
        self.graphs = {}  # dictionary to hold generated graphs
        self.graph_types = ["no_edges", f"rand_density_{self.rand_edge_density}", "fully_connected"]
        self.generate_graphs()

    def generate_graphs(self, verbose=True):
        print("generating graphs")
        for size in self.graph_sizes:
            FCGraph = Graph()
            EmptyGraph = Graph()
            RandGraph = Graph()

            FCGraph_nx = nx.Graph()
            EmptyGraph_nx = nx.Graph()
            RandGraph_nx = nx.Graph()

            # create edges for each type of graph
            for i in tqdm(range(size), disable=not verbose):
                EmptyGraph.add_node(i)
                EmptyGraph_nx.add_node(str(i))
                for j in range(i + 1, size):
                    i, j = str(i), str(j)
                    FCGraph.add_edge(i, j)
                    FCGraph_nx.add_edge(i, j)
                    if random.random() < self.rand_edge_density:
                        RandGraph.add_edge(i, j)
                        RandGraph_nx.add_edge(i, j)

            self.graphs[size] = {self.graph_types[0]: (EmptyGraph, EmptyGraph_nx),
                                 self.graph_types[1]: (RandGraph, RandGraph_nx),
                                 self.graph_types[2]: (FCGraph, FCGraph_nx)}

    def run_tests(self, func, nx_func, func_args, generators=[False, False], verbose=True):
        print("running tests")
        performance = {}
        for size in self.graph_sizes:
            performance[size] = {}
            for k in self.graph_types:
                performance[size][k] = []

        for size in self.graph_sizes:
            for k in self.graph_types:
                G, nxG = self.graphs[size][k]
                times_nx = []
                times = []
                for i in tqdm(range(self.iters), disable=not verbose):

                    # time the custom function
                    start = time.time()
                    if generators[0]:
                        [i for i in func(G, *func_args)]
                    else:
                        func(G, *func_args)
                    end = time.time()
                    times.append(round(end - start, 10))
                    if verbose:
                        print(f"time for size{size}, graph type {k}: {end - start}s")

                    # time the NetworkX function
                    start = time.time()
                    if generators[1]:
                        [i for i in nx_func(nxG, *func_args)]
                    else:
                        nx_func(nxG, *func_args)
                    end = time.time()
                    times_nx.append(round(end - start, 10))
                    if verbose:
                        print(f"nx time for size{size}, graph type {k}: {end - start}s")

                performance[size][k].append((times, times_nx))

        return performance

    def plot_results(self, results, plot_method=["our function", "NetworkX"]):
        fig, axs = plt.subplots(1, len(results[next(iter(results))]), figsize=(16, 5))
        x_labels = list(results.keys())

        for i, graph_type in enumerate(results[x_labels[0]]):
            ax = axs[i]
            x_val = 2
            width = 0.35
            for size in results:
                m_time, nx_time = results[size][graph_type][0]
                if "our function" in plot_method:
                    ax.scatter([x_val - width / 2] * len(m_time), m_time, label='our function', color="orange",
                               alpha=0.5, s=100)
                if "NetworkX" in plot_method:
                    ax.scatter([x_val + width / 2] * len(nx_time), nx_time, label='NetworkX', color="blue", alpha=0.5,
                               s=100)
                x_val += 2

            xtick_locs = range(2, 2 * len(self.graph_sizes) + 1, 2)
            ax.set_xticks(xtick_locs)
            ax.set_xticklabels(x_labels)
            ax.legend(labels=plot_method)
            ax.set_title(graph_type)

        plt.show()


if __name__ == "__main__":
    GPT = GraphPerformanceTester(sizes=[50, 100, 500], iters=3)
    performance = GPT.run_tests(sp.single_source_shortest_path, nx.single_source_shortest_path_length, ("3",))
    print(performance)
    GPT.plot_results(performance)