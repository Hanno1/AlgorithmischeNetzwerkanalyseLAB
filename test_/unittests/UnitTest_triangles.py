from unittest import TestCase
import test_.HelperClass as HelperClass
import src.triangleAlgorithms as tri


class TestImplementationOnTriangles(TestCase):
    def test_node_iterator(self):
        G, n, m = HelperClass.create_graph()
        number, triangles = tri.algorithm_node_iterator(G)
        self.assertEqual(number, 1)
        self.assertEqual(triangles, [['3', '4', '5']])

        G.add_edge(7, 8)
        number, triangles = tri.algorithm_node_iterator(G)
        self.assertEqual(number, 2)
        self.assertEqual(triangles, [['3', '4', '5'], ['6', '7', '8']])

    def test_chiba_and_nishizeki(self):
        G, n, m = HelperClass.create_graph()
        number, triangles = tri.algorithm_chiba_and_nishizeki(G)
        self.assertEqual(number, 1)
        self.assertEqual(triangles, [['3', '4', '5']])

        G.add_edge(7, 8)
        number, triangles = tri.algorithm_chiba_and_nishizeki(G)
        self.assertEqual(number, 2)
        self.assertEqual(triangles, [['3', '4', '5'], ['6', '7', '8']])

    def test_edge_iterator(self):
        G, n, m = HelperClass.create_graph()
        number, triangles = tri.algorithm_edge_iterator(G)
        self.assertEqual(number, 1)
        self.assertEqual(triangles, [['3', '5', '4']])

        G.add_edge(7, 8)
        number, triangles = tri.algorithm_edge_iterator(G)
        self.assertEqual(number, 2)
        self.assertEqual(triangles, [['3', '5', '4'], ['6', '8', '7']])

    def test_triangle_counter_ayz(self):
        G, n, m = HelperClass.create_graph()
        number, _ = tri.algorithm_triangle_counter_ayz_internal_ids(G, 1)
        self.assertEqual(number, 1)

        G.add_edge(7, 8)
        number, _ = tri.algorithm_triangle_counter_ayz_internal_ids(G, 2)
        self.assertEqual(number, 2)
