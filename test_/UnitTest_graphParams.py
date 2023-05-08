import src.graphParameters as gP
from src.Graph import Graph
import HelperClass as HelperClass
from unittest import TestCase
import unittest


class TestShortestPaths(TestCase):
    def test_hindex(self):
        G = Graph()
        G.add_node(1)
        G.add_edge(3,2)
        self.assertEqual(gP.h_index(G), 1)
        G.add_edge(3,5)
        G.add_edge(3,6)
        self.assertEqual(gP.h_index(G), 1)
        G.add_edge(4,2)
        self.assertEqual(gP.h_index(G), 2)
        G.add_edge(4,5)
        G.add_edge(4,7)
        G.add_edge(4,8)
        G.add_edge(4,9)
        G.add_edge(9,7)
        self.assertEqual(gP.h_index(G), 2)
        G.add_edge(9,8)
        self.assertEqual(gP.h_index(G), 3)
        G.add_edge(9,10)
        G.add_edge(10,7)
        G.add_edge(8,7)
        self.assertEqual(gP.h_index(G), 3)
        G.add_edge(10,8)
        self.assertEqual(gP.h_index(G), 4)

    def test_degeneracy(self):
        G = Graph()
        G.add_node(1)
        G.add_edge(3,2)
        G.add_edge(3,5)
        G.add_edge(3,6)
        G.add_edge(4,2)
        G.add_edge(4,5)
        G.add_edge(4,7)
        G.add_edge(4,8)
        G.add_edge(4,9)
        G.add_edge(9,7)
        G.add_edge(9,8)
        G.add_edge(9,10)
        G.add_edge(10,7)
        G.add_edge(8,7)
        G.add_edge(10,8)
        degeneracy, degeneracy_order = gP.degeneracy(G)
        self.assertEqual(degeneracy, 3)

        for n in degeneracy_order:
            if G.get_node_degree(n) <= degeneracy:
                continue
            n_index = degeneracy_order.index(n)
            neighb_higher_order = 0
            for nn in G.get_neighbors(n):
                if degeneracy_order.index(nn) > n_index:
                    neighb_higher_order += 1
            self.assertGreaterEqual(degeneracy,neighb_higher_order)

if __name__ == '__main__':
    unittest.main()