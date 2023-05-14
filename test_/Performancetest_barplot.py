import networkx as nx
from src.Graph import Graph
import time
import src.triangleAlgorithms as Ta
import matplotlib.pyplot as plt


def generate_and_translate_graph(n, m):
    if m is None:
        newG = nx.complete_graph(n)
    elif m == 0:
        newG = nx.empty_graph(n)
    else:
        newG = nx.dense_gnm_random_graph(n, m)
    nodes = nx.nodes(newG)
    G = Graph()
    for node in nodes:
        G.add_node(node)
    edges = nx.edges(newG)
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    return G


def test_function(n, m, function, name, iterations):
    start = time.time()

    for _ in range(iterations):
        graph = generate_and_translate_graph(n, m)
        function(graph)

    time_dif = time.time() - start
    return time_dif / iterations


def test_and_plot_function_results(n, m, functions, names, iterations=100):
    time_array = []
    i = 0
    for func in functions:
        time_array.append(test_function(n, m, func, names[i], iterations))
        i += 1
    return time_array


def test_and_plot_results(n_array, m_array, functions, names, iterations, colors=None):
    if not colors or len(colors) != len(functions):
        colors = ["black" for _ in range(len(functions))]
    const_c = len(m_array[0])
    fig, axs = plt.subplots(len(n_array), const_c)
    row = 0
    for n in n_array:
        maxi = 0
        for c in range(const_c):
            m = m_array[row][c]
            time_array = test_and_plot_function_results(n, m, functions, names, iterations)
            axs[row][c].bar([i for i in range(len(time_array))], time_array, label=names, width=0.4, color=colors)
            maxi = max(time_array)
        for c in range(const_c):
            axs[row][c].set_ylim(0, maxi * 1.01)
        row += 1
    plt.legend(loc="lower center", bbox_to_anchor=(0, 0, 1, 2), ncol=2, bbox_transform=plt.gcf().transFigure)
    plt.show()


def test_and_plot_fully_connected(n_array, functions, names, iterations, colors=None):
    if not colors or len(colors) != len(functions):
        colors = ["black" for _ in range(len(functions))]
    fig, axs = plt.subplots(len(n_array), 1)
    counter = 0
    for n in n_array:
        m = None
        time_array = test_and_plot_function_results(n, m, functions, names, iterations)
        axs[counter].bar([i for i in range(len(time_array))], time_array, label=names, width=0.4, color=colors)
        counter += 1
    plt.legend(loc="lower center", bbox_to_anchor=(0, 0, 1, 2), ncol=2, bbox_transform=plt.gcf().transFigure)
    plt.show()


n_array = [50, 100, 200]
functions = [Ta.algorithm_node_iterator, Ta.algorithm_node_iterator_without_sorting,
             Ta.algorithm_edge_iterator, Ta.algorithm_triangle_counter_ayz]
names = ["node iterator", "node iterator, no sorting", "edge iterator", "ayz"]
colors = ["blue", "green", "orange", "red"]
"""m_array = [[0, entry * 2, entry * 5] for entry in n_array]
test_and_plot_results(n_array, m_array,
                      [Ta.algorithm_node_iterator,
                       Ta.algorithm_node_iterator_without_sorting,
                       Ta.algorithm_edge_iterator,
                       Ta.algorithm_triangle_counter_ayz],
                      ["node iterator", "node iterator, no sorting", "edge iterator",
                       "ayz"], 100, colors=["blue", "green", "orange", "red"])
"""

test_and_plot_fully_connected(n_array, functions, names, 1, colors)

"""test_and_plot_results([10, 50, 100], [[0, None] for _ in [10, 50, 100]],
                      [Ta.algorithm_node_iterator, Ta.algorithm_edge_iterator,
                       Ta.algorithm_triangle_counter_ayz],
                      ["node iterator", "edge iterator",
                       "ayz"], 100, colors=["blue", "green", "orange"])"""
