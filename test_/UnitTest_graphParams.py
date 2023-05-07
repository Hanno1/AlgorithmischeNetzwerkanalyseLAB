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
        self.assertEqual(gP.degeneracy(G), 3)
    


if __name__ == '__main__':
    unittest.main()