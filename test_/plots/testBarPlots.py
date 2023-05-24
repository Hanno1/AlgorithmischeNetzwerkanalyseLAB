from test_.plots.Performancetest_barplot import test_and_plot_results
import math
import src.triangleAlgorithms as Ta
import networkx as nx
import TestsOnPowerNetworks as Tp


"""n_array = [50, 100, 200]
functions = [Ta.algorithm_chiba_and_nishizeki, Ta.algorithm_node_iterator_without_sorting,
             Ta.algorithm_node_iterator_degeneracy_sorting, nx.triangles]
names = ["chiba", "node iterator, no sorting", "ayz", "network x"]
colors = ["blue", "green", "orange", "red"]
m_array = [[0, entry * 2, entry * round(math.log(entry))] for entry in n_array]
p_array = [[0.01, 0.1, 0.5] for entry in n_array]
test_and_plot_results(n_array, p_array,
                      functions,
                      names, 50, colors=colors, netx=[3], useGnp=True)"""

# test_and_plot_fully_connected(n_array, functions, names, 1, colors, netx=[4])

"""test_and_plot_results([10, 50, 100], [[0, None] for _ in [10, 50, 100]],
                      [Ta.algorithm_node_iterator, Ta.algorithm_edge_iterator,
                       Ta.algorithm_triangle_counter_ayz],
                      ["node iterator", "edge iterator",
                       "ayz"], 100, colors=["blue", "green", "orange"])"""

"""test = Tp.TestTriangleImplementationPowerNetworks([tri.algorithm_node_iterator,
                                                tri.algorithm_with_combinations,
                                                tri.algorithm_node_iterator_degeneracy_sorting,
                                                nx.triangles],
                                               ["Node Iterator", "using combinations",
                                                "Node Iterator, degeneracy", "networkX"], [3])"""
test = Tp.TestAYZImplementationOnPowerNetworks([1, 2, 3, 4, 5])
test.plot_and_run()
