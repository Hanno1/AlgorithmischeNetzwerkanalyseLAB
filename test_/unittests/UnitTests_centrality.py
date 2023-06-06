from unittest import TestCase
import test_.HelperClass as Hc
import src.Graph as Graph


def initial_centrality(G: Graph):
    initial_cent = dict()
    for node in G.node_ids_internal_ids:
        initial_cent[node] = G.get_node_degree(node)
    return initial_cent


class TestOwnCentrality(TestCase):

    def test_fast_mode_centrality(self):
        G, _, _ = Hc.create_graph()
        G.add_edge(11, 13)
        Hc.create_own_centrality_fast(G, 10)
        Hc.create_own_centrality_fast(G, 10, node="3")
        Hc.create_own_centrality_fast(G, 10, node="15")
        Hc.create_own_centrality_fast(G, 10, k=1)
        Hc.create_own_centrality_fast(G, 10, k=2)
        Hc.create_own_centrality_fast(G, 10, k=3)

    def test_single_node_centrality(self):
        G, _, _ = Hc.create_graph()
        G.add_edge(11, 13)

        decimal_place = 2
        self.assertAlmostEqual(Hc.create_own_centrality(G, node="-1"), 1, decimal_place)
        self.assertAlmostEqual(Hc.create_own_centrality(G, node="3"), 3.25, decimal_place)
        self.assertAlmostEqual(Hc.create_own_centrality(G, node="5"), 2.36, decimal_place)
        self.assertAlmostEqual(Hc.create_own_centrality(G, node="15"), 0, decimal_place)

        initial_centr = initial_centrality(G)
        self.assertAlmostEqual(Hc.create_own_centrality_init(G, initial_centr, node="-1", ), 1, decimal_place)
        self.assertAlmostEqual(Hc.create_own_centrality_init(G, initial_centr, node="4"), 5.61, decimal_place)
        self.assertAlmostEqual(Hc.create_own_centrality_init(G, initial_centr, node="3"), 6.25, decimal_place)
        self.assertAlmostEqual(Hc.create_own_centrality_init(G, initial_centr, node="12"), 6.5, decimal_place)

    def test_all_nodes_centrality(self):
        G, _, _ = Hc.create_graph()
        G.add_edge(11, 13)
        centr = Hc.create_own_centrality(G)
        decimal_place = 2

        self.assertAlmostEqual(centr["1"], 1.47, decimal_place)
        self.assertAlmostEqual(centr["6"], 2, decimal_place)
        self.assertAlmostEqual(centr["8"], 1.25, decimal_place)
        self.assertAlmostEqual(centr["15"], 0, decimal_place)

        initial_centr = initial_centrality(G)
        centr = Hc.create_own_centrality_init(G, initial_centr)
        self.assertAlmostEqual(centr["1"], 3.19, decimal_place)
        self.assertAlmostEqual(centr["6"], 2, decimal_place)
        self.assertAlmostEqual(centr["8"], 2.25, decimal_place)
        self.assertAlmostEqual(centr["15"], 0, decimal_place)

    def test_k_central_nodes(self):
        G, _, _ = Hc.create_graph()
        G.add_edge(11, 13)
        nodes, values = Hc.create_own_centrality(G, k=3)
        decimal_place = 2

        self.assertEqual(nodes, ['11', '13', '3'])
        comp_values = [3, 3, 3.25]
        for i in range(len(values)):
            self.assertAlmostEqual(values[i], comp_values[i], decimal_place)

        initial_centr = initial_centrality(G)
        nodes, values = Hc.create_own_centrality_init(G, initial_centr, k=3)

        self.assertEqual(nodes, ['12', '11', '13'])
        comp_values = [6.5, 7, 7]
        for i in range(len(values)):
            self.assertAlmostEqual(values[i], comp_values[i], decimal_place)
