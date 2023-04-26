import src.shortestPaths as sP
import HelperClass as HelperClass
from unittest import TestCase
import math


class TestShortestPaths(TestCase):
    def test_single_source_shortest_path(self):
        G, n, m = HelperClass.create_graph()
        dist = sP.single_source_shortest_path(G, 1)

        self.assertEqual(dist[0], math.inf)
        self.assertEqual(dist[1], 0)
        self.assertEqual(dist[2], 1)
        self.assertEqual(dist[3], 2)
        self.assertEqual(dist[5], 3)
        self.assertEqual(dist[-1], math.inf)
        self.assertEqual(dist[9], math.inf)

        mapping = G.get_internal_mapping()

        dist, mapping = sP.single_source_shortest_path_vector(G, 1, mapping)

        self.assertEqual(dist[mapping[0]], math.inf)
        self.assertEqual(dist[mapping[1]], 0)
        self.assertEqual(dist[mapping[4
        ]], 3)

    def test_all_pair_shortest_path(self):
        G, n, m = HelperClass.create_graph()
        dist, mapping = sP.all_pair_shortest_path_matrix(G)

        self.assertEqual(dist[mapping[0]][mapping[-1]], 1)
        self.assertEqual(dist[mapping[-1]][mapping[0]], 1)

        self.assertEqual(dist[mapping[1]][mapping[1]], 0)

        self.assertEqual(dist[mapping[2]][mapping[5]], 2)
        self.assertEqual(dist[mapping[3]][mapping[5]], 1)
        self.assertEqual(dist[mapping[1]][mapping[5]], 3)
        self.assertEqual(dist[mapping[4]][mapping[1]], 3)
        self.assertEqual(dist[mapping[5]][mapping[3]], 1)

        self.assertEqual(dist[mapping[0]][mapping[1]], math.inf)

        self.assertEqual(dist[mapping[9]][mapping[1]], math.inf)
        self.assertEqual(dist[mapping[10]][mapping[13]], 1)

    def test_bi_directional_search(self):
        G, n, m = HelperClass.create_graph()
        path, number = sP.shortest_s_t_path(G, 1, 5)

        self.assertEqual(path, [1, 2, 3, 5])
        self.assertEqual(number, 3)

        path, _ = sP.shortest_s_t_path(G, 1, 9)
        self.assertEqual(path, [])

    def test_connected_components(self):
        G, n, m = HelperClass.create_graph()
        self.assertEqual(sP.connected_components(G), [{0, -1}, {1, 2, 3, 4, 5}, {8, 6, 7}, {9}, {10, 11, 12, 13}, {15}])
