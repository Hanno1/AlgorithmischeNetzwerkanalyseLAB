from unittest import TestCase
import HelperClass as HelperClass
import src.CustomExceptions as Exc


class TestGraph(TestCase):
    def test_total_number_of_nodes(self):
        G, n, m = HelperClass.create_graph()

        self.assertEqual(G.n, n)
        self.assertEqual(G.m, m)

    def test_remove_node(self):
        G, n, m = HelperClass.create_graph()
        G.remove_node(3)

        self.assertEqual(G.n, n-1)
        self.assertEqual(G.m, m-3)

        # remove node that doesnt exist -> there should be an error
        self.assertRaises(Exc.NodeDoesNotExistException, G.remove_node, 3)

    def test_remove_edge(self):
        G, n, m = HelperClass.create_graph()

        G.remove_edge(4, 5)
        self.assertEqual(G.n, n)
        self.assertEqual(G.m, m-1)

        G.remove_edge(5, 4)
        self.assertEqual(G.m, m-1)

    def test_neighbors(self):
        G, n, m = HelperClass.create_graph()

        self.assertEqual(G.test_neighbors(1, 2), True)
        self.assertEqual(G.test_neighbors(2, 1), True)
        self.assertEqual(G.test_neighbors(1, 3), False)
        self.assertEqual(G.test_neighbors(-1, 2), False)
        self.assertEqual(G.test_neighbors(-1, 0), True)

        G.remove_edge(1, 2)
        self.assertEqual(G.test_neighbors(1, 2), False)
        self.assertEqual(G.test_neighbors(2, 1), False)

        self.assertEqual(G.test_neighbors(1, 1), False)

        G.remove_node(15)
        self.assertRaises(Exc.NodeDoesNotExistException, G.test_neighbors, -1, 15)

    def test_get_neighbors(self):
        G, n, m = HelperClass.create_graph()

        self.assertEqual(G.get_neighbors(1), {2})
        self.assertEqual(G.get_neighbors(3), {2, 4, 5})
        self.assertEqual(G.get_neighbors(9), set())

        self.assertRaises(Exc.NodeDoesNotExistException, G.get_neighbors, 14)

    def test_node_degree(self):
        G, n, m = HelperClass.create_graph()

        self.assertEqual(G.get_node_degree(1), 1)
        self.assertEqual(G.get_node_degree(3), 3)
        self.assertEqual(G.get_node_degree(4), 2)
        self.assertEqual(G.get_node_degree(9), 0)

        self.assertRaises(Exc.NodeDoesNotExistException, G.get_node_degree, 14)

    def test_save_graph_edge_list(self):
        G, n, m = HelperClass.create_graph()

        G.save_graph_as_edge_list("test")

        with open("test.txt") as file:
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "-1 0")
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "1 2")
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "2 3")
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "3 4")

    def test_read_graph_edge_list(self):
        G, n, m = HelperClass.create_graph()

        G.remove_node(0)
        G.add_edge(1, 10)

        G.save_graph_as_edge_list("test")
        newG = HelperClass.read_graph_as_edge_list("test.txt")

        self.assertEqual(newG.n, n-4)
        self.assertEqual(newG.m, m)

    def test_save_graph_metis(self):
        G, n, m = HelperClass.create_graph()
        G.save_graph_metis("test")

        with open("test.txt") as file:
            line = file.readline().replace("\n", "")
            self.assertEqual(line, f"{n} {m}")
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "2")
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "1")
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "4")

    def test_read_graph_metis(self):
        G, n, m = HelperClass.create_graph()

        G.remove_node(0)
        G.add_edge(1, 10)

        G.save_graph_metis("test")
        newG = HelperClass.read_graph_metis("test.txt")

        self.assertEqual(newG.n, n - 1)
        self.assertEqual(newG.m, m)
