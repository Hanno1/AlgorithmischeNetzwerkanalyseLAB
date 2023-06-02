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
        centr = Hc.create_own_centrality_fast(G, 10)

        centr.single_node_centrality(10)
        centr.single_node_centrality(15)
        centr.all_nodes_centrality()
        centr.k_central_nodes(4)
        centr.most_central_node()

    def test_single_node_centrality(self):
        G, _, _ = Hc.create_graph()
        G.add_edge(11, 13)
        centr = Hc.create_own_centrality(G)

        decimal_place = 2
        self.assertAlmostEqual(centr.single_node_centrality(1), 1.47, decimal_place)
        self.assertAlmostEqual(centr.single_node_centrality(6), 2, decimal_place)
        self.assertAlmostEqual(centr.single_node_centrality(8), 1.25, decimal_place)
        self.assertAlmostEqual(centr.single_node_centrality(15), 0, decimal_place)

        initial_centr = initial_centrality(G)
        centr = Hc.create_own_centrality_init(G, initial_centr)

        self.assertAlmostEqual(centr.single_node_centrality(1), 3.19, decimal_place)
        self.assertAlmostEqual(centr.single_node_centrality(6), 2, decimal_place)
        self.assertAlmostEqual(centr.single_node_centrality(8), 2.25, decimal_place)
        self.assertAlmostEqual(centr.single_node_centrality(15), 0, decimal_place)

    def test_all_nodes_centrality(self):
        G, _, _ = Hc.create_graph()
        G.add_edge(11, 13)
        centr = Hc.create_own_centrality(G)
        decimal_place = 2
        all_centr = centr.all_nodes_centrality()

        self.assertAlmostEqual(all_centr["1"], 1.47, decimal_place)
        self.assertAlmostEqual(all_centr["6"], 2, decimal_place)
        self.assertAlmostEqual(all_centr["8"], 1.25, decimal_place)
        self.assertAlmostEqual(all_centr["15"], 0, decimal_place)

        initial_centr = initial_centrality(G)
        centr = Hc.create_own_centrality_init(G, initial_centr)
        all_centr = centr.all_nodes_centrality()

        self.assertAlmostEqual(all_centr["1"], 3.19, decimal_place)
        self.assertAlmostEqual(all_centr["6"], 2, decimal_place)
        self.assertAlmostEqual(all_centr["8"], 2.25, decimal_place)
        self.assertAlmostEqual(all_centr["15"], 0, decimal_place)

    def test_most_central_node(self):
        G, _, _ = Hc.create_graph()
        G.add_edge(11, 13)
        centr = Hc.create_own_centrality(G)
        decimal_place = 2
        node, value = centr.most_central_node()

        self.assertEqual(node, ['3'])
        self.assertAlmostEqual(value, 3.25, decimal_place)

        initial_centr = initial_centrality(G)
        centr = Hc.create_own_centrality_init(G, initial_centr)
        node, value = centr.most_central_node()

        self.assertEqual(node, ['11', '13'])
        self.assertAlmostEqual(value, 7.0, decimal_place)

    def test_k_central_nodes(self):
        G, _, _ = Hc.create_graph()
        G.add_edge(11, 13)
        centr = Hc.create_own_centrality(G)
        decimal_place = 2
        nodes, values = centr.k_central_nodes(3)

        self.assertEqual(nodes, ['11', '13', '3'])
        comp_values = [3, 3, 3.25]
        for i in range(len(values)):
            self.assertAlmostEqual(values[i], comp_values[i], decimal_place)

        initial_centr = initial_centrality(G)
        centr = Hc.create_own_centrality_init(G, initial_centr)
        nodes, values = centr.k_central_nodes(3)

        self.assertEqual(nodes, ['12', '11', '13'])
        comp_values = [6.5, 7, 7]
        for i in range(len(values)):
            self.assertAlmostEqual(values[i], comp_values[i], decimal_place)
