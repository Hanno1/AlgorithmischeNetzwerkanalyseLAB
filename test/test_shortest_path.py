import src.shortestPaths as sP
import HelperClass as HelperClass
from unittest import TestCase


class testShortestPaths(TestCase):
    def test_single_source_shortest_path(self):
        G, n, m = HelperClass.createGraph()
        dist = sP.single_source_shortest_path(G, 1)

        self.assertEqual(dist[0], float('inf'))
        self.assertEqual(dist[1], 0)
        self.assertEqual(dist[2], 1)
        self.assertEqual(dist[3], 1)
        self.assertEqual(dist[5], 2)

    def test_all_pair_shortest_path(self):
        G, n, m = HelperClass.createGraph()
        dist = sP.all_pair_shortest_path(G)

        print(dist)
