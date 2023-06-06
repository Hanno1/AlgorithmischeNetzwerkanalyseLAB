import networkx as nx
from src.Graph import Graph
import time
import matplotlib.pyplot as plt
import random


def generate_and_translate_graph(n, m, netx):
    if m is None:
        newG = nx.complete_graph(n)
    elif m == 0:
        newG = nx.empty_graph(n)
    else:
        newG = nx.dense_gnm_random_graph(n, m)
    if netx:
        return newG
    return translate_Graph(newG)


def generate_gnp_graph(n, p, netx):
    newG = nx.gnp_random_graph(n, p)
    if netx:
        return newG
    return translate_Graph(newG)


def translate_Graph(newG):
    nodes = nx.nodes(newG)
    G = Graph()
    for node in nodes:
        G.add_node(node)
    edges = nx.edges(newG)
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    return G


def test_function(n, m, function, iterations, netx, useGnp, param_k):
    start = time.time()

    if not useGnp:
        if param_k is None:
            for _ in range(iterations):
                graph = generate_and_translate_graph(n, m, netx)
                function(graph)
        else:
            for _ in range(iterations):
                graph = generate_and_translate_graph(n, m, netx)
                function(graph, k_uniform_nodes=param_k)
    else:
        if param_k is None:
            for _ in range(iterations):
                graph = generate_gnp_graph(n, m, netx)
                function(graph)
        else:
            for _ in range(iterations):
                graph = generate_gnp_graph(n, m, netx)
                function(graph, k_uniform_nodes=param_k)

    time_dif = time.time() - start
    return time_dif / iterations


def test_and_plot_function_results(n, m, functions, names, param_k, netx, useGnp, iterations):
    if netx is None:
        netx = []
    time_array = []
    i = 0
    for func in functions:
        if i in netx:
            time_array.append(test_function(n, m, func, iterations, True, useGnp, param_k))
        else:
            time_array.append(test_function(n, m, func, iterations, False, useGnp, param_k))
        i += 1
    return time_array


def test_and_plot_results(n_array, m_array, functions, names, iterations, colors=None, netx=None, useGnp=False, param_k=None):
    if colors is None or len(colors) != len(functions):
        colors = []
        for _ in range(len(functions)):
            r = random.random()
            g = random.random()
            b = random.random()
            colors.append([r, g, b])
    const_c = len(m_array[0])
    fig, axs = plt.subplots(len(n_array), const_c)
    row = 0
    for n in n_array:
        print(n)
        maxi = 0
        for c in range(const_c):
            print(c)
            m = m_array[row][c]
            time_array = test_and_plot_function_results(n, m, functions, names, param_k, netx, useGnp, iterations)
            axs[row][c].bar([i for i in range(len(time_array))], time_array, label=names, width=0.4, color=colors)
            maxi = max(time_array)
        for c in range(const_c):
            axs[row][c].set_ylim(0, maxi * 1.01)
        row += 1
    plt.legend(loc="lower center", bbox_to_anchor=(0, 0, 1, 2), ncol=2, bbox_transform=plt.gcf().transFigure)
    plt.show()


def test_and_plot_fully_connected(n_array, functions, names, iterations, colors=None, netx=None, useGnp=False, param_k=None):
    if not colors or len(colors) != len(functions):
        colors = ["black" for _ in range(len(functions))]
    fig, axs = plt.subplots(len(n_array), 1)
    counter = 0
    for n in n_array:
        m = None
        time_array = test_and_plot_function_results(n, m, functions, names, iterations, netx, useGnp, param_k)
        axs[counter].bar([i for i in range(len(time_array))], time_array, label=names, width=0.4, color=colors)
        counter += 1
    plt.legend(loc="lower center", bbox_to_anchor=(0, 0, 1, 2), ncol=2, bbox_transform=plt.gcf().transFigure)
    plt.show()
