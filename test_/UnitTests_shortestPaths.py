import src.shortestPaths as sP
import HelperClass as HelperClass
from unittest import TestCase
import math


class TestShortestPaths(TestCase):
    def test_single_source_shortest_path(self):
        G, n, m = HelperClass.create_graph()
        dist = sP.single_source_shortest_path(G, 1)

        self.assertEqual(dist["0"], math.inf)
        self.assertEqual(dist["1"], 0)
        self.assertEqual(dist["2"], 1)
        self.assertEqual(dist["3"], 2)
        self.assertEqual(dist["5"], 3)
        self.assertEqual(dist["-1"], math.inf)
        self.assertEqual(dist["9"], math.inf)

    def test_all_pair_shortest_path(self):
        G, n, m = HelperClass.create_graph()
        dist = sP.all_pair_shortest_path(G)

        self.assertEqual(dist["0"]["-1"], 1)
        self.assertEqual(dist["7"]["8"], 2)
        self.assertEqual(dist["1"]["4"], 3)
        self.assertEqual(dist["10"]["13"], 1)
        self.assertEqual(dist["9"]["15"], math.inf)
        self.assertEqual(dist["-1"]["0"], 1)

    def test_bi_directional_search(self):
        G, n, m = HelperClass.create_graph()
        path, number = sP.shortest_s_t_path(G, 1, 5)

        self.assertEqual(path, ["1", "2", "3", "5"])
        self.assertEqual(number, 3)

        path, _ = sP.shortest_s_t_path(G, 1, 9)
        self.assertEqual(path, [])

    def test_connected_components(self):
        G, n, m = HelperClass.create_graph()

        self.assertEqual(sP.connected_components(G), [{'-1', '0'}, {'2', '3', '5', '1', '4'}, {'7', '6', '8'}, {'9'},
                                                      {'11', '12', '10', '13'}, {'15'}])
