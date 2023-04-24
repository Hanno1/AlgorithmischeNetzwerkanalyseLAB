from unittest import TestCase
from HelperClass import createGraph


class TestGraph(TestCase):
    def test_total_number_of_nodes(self):
        G, n, m = createGraph()

        self.assertEqual(G.n, n)
        self.assertEqual(G.m, m)

    def test_remove_node(self):
        G, n, m = createGraph()
        G.removeNode(0)
        self.assertEqual(G.n, n-1)
        self.assertEqual(G.m, m-1)
