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

        dist, mapping = sP.single_source_shortest_path_vector(G, 1)

        self.assertEqual(dist[mapping.index(0)], math.inf)
        self.assertEqual(dist[mapping.index(1)], 0)
        self.assertEqual(dist[mapping.index(4)], 3)

    def test_all_pair_shortest_path(self):
        G, n, m = HelperClass.createGraph()
        dist, mapping = sP.all_pair_shortest_path_matrix(G)

        self.assertEqual(dist[mapping.index(0)][mapping.index(-1)], 1)
        self.assertEqual(dist[mapping.index(-1)][mapping.index(0)], 1)

        self.assertEqual(dist[mapping.index(1)][mapping.index(1)], 0)

        self.assertEqual(dist[mapping.index(2)][mapping.index(5)], 2)
        self.assertEqual(dist[mapping.index(3)][mapping.index(5)], 1)
        self.assertEqual(dist[mapping.index(1)][mapping.index(5)], 3)
        self.assertEqual(dist[mapping.index(4)][mapping.index(1)], 3)
        self.assertEqual(dist[mapping.index(5)][mapping.index(3)], 1)

        self.assertEqual(dist[mapping.index(0)][mapping.index(1)], math.inf)

        self.assertEqual(dist[mapping.index(9)][mapping.index(1)], math.inf)
        self.assertEqual(dist[mapping.index(10)][mapping.index(13)], 1)

    def test_bi_directional_search(self):
        G, n, m = HelperClass.createGraph()
        path, number = sP.biDirSearch(G, 1, 5)

        self.assertEqual(path, [1, 2, 3, 5])
        self.assertEqual(number, 3)

        path, _ = sP.biDirSearch(G, 1, 9)
        self.assertEqual(path, [])

    def test_connected_components(self):
        G, n, m = HelperClass.createGraph()
        self.assertEqual(sP.connected_components(G), [{0, -1}, {1, 2, 3, 4, 5}, {8, 6, 7}, {9}, {10, 11, 12, 13}, {15}])
