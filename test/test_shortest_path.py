import src.shortestPaths as sP
import HelperClass as HelperClass
from unittest import TestCase
import math


class testShortestPaths(TestCase):
    def test_single_source_shortest_path(self):
        G, n, m = HelperClass.createGraph()
        dist = sP.single_source_shortest_path(G, 1)

        self.assertEqual(dist[0], math.inf)
        self.assertEqual(dist[1], 0)
        self.assertEqual(dist[2], 1)
        self.assertEqual(dist[3], 2)
        self.assertEqual(dist[5], 3)
        self.assertEqual(dist[-1], math.inf)
        self.assertEqual(dist[9], math.inf)

    def test_all_pair_shortest_path(self):
        G, n, m = HelperClass.createGraph()
        dist = sP.all_pair_shortest_path(G)

        print(dist)

    def test_bi_directional_search(self):
        G, n, m = HelperClass.createGraph()
        path, number = sP.biDirSearch(G, 1, 5)
        print(path, number)

    def test_connected_components(self):
        G, n, m = HelperClass.createGraph()
        self.assertEqual(sP.connected_components(G), [{0, -1}, {1, 2, 3, 4, 5}, {8, 6, 7}, {9}, {10, 11, 12, 13}, {15}])
