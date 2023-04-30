from unittest import TestCase
import unittest
import HelperClass


class TestImplementationOnGivenNetworks(TestCase):
    def test(self):
        G = HelperClass.read_graph_as_edge_list("../networks/bio-celegans.mtx")

if __name__ == '__main__':
    unittest.main()