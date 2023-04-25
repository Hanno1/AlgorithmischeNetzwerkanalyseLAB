from unittest import TestCase
import HelperClass as HelperClass
import src.exception as exc


class TestGraph(TestCase):
    def test_total_number_of_nodes(self):
        G, n, m = HelperClass.createGraph()

        self.assertEqual(G.n, n)
        self.assertEqual(G.m, m)

    def test_remove_node(self):
        G, n, m = HelperClass.createGraph()
        G.removeNode(3)

        self.assertEqual(G.n, n-1)
        self.assertEqual(G.m, m-3)

        # remove node that doesnt exist -> there should be an error
        self.assertRaises(exc.NodeDoesNotExist, G.removeNode, 3)

    def test_remove_edge(self):
        G, n, m = HelperClass.createGraph()

        G.removeEdge(4, 5)
        self.assertEqual(G.n, n)
        self.assertEqual(G.m, m-1)

        G.removeEdge(5, 4)
        self.assertEqual(G.m, m-1)

    def test_neighbors(self):
        G, n, m = HelperClass.createGraph()

        self.assertEqual(G.testNeighbors(1, 2), True)
        self.assertEqual(G.testNeighbors(2, 1), True)
        self.assertEqual(G.testNeighbors(1, 3), False)
        self.assertEqual(G.testNeighbors(-1, 2), False)
        self.assertEqual(G.testNeighbors(-1, 0), True)

        G.removeEdge(1, 2)
        self.assertEqual(G.testNeighbors(1, 2), False)
        self.assertEqual(G.testNeighbors(2, 1), False)

        self.assertEqual(G.testNeighbors(1, 1), False)

        G.removeNode(15)
        self.assertRaises(exc.NodeDoesNotExist, G.testNeighbors, -1, 15)

    def test_get_neighbors(self):
        G, n, m = HelperClass.createGraph()

        self.assertEqual(G.getNeighbors(1), {2})
        self.assertEqual(G.getNeighbors(3), {2, 4, 5})
        self.assertEqual(G.getNeighbors(9), set())

        self.assertRaises(exc.NodeDoesNotExist, G.getNeighbors, 14)

    def test_node_degree(self):
        G, n, m = HelperClass.createGraph()

        self.assertEqual(G.getNodeDegree(1), 1)
        self.assertEqual(G.getNodeDegree(3), 3)
        self.assertEqual(G.getNodeDegree(4), 2)
        self.assertEqual(G.getNodeDegree(9), 0)

        self.assertRaises(exc.NodeDoesNotExist, G.getNodeDegree, 14)

    def test_save_graph_edge_list(self):
        G, n, m = HelperClass.createGraph()

        G.saveGraphAsEdgeList("test")

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
        G, n, m = HelperClass.createGraph()

        G.removeNode(0)
        G.addEdge(1, 10)

        G.saveGraphAsEdgeList("test")
        newG = HelperClass.readGraphEdgeList("test.txt")

        self.assertEqual(newG.n, n-4)
        self.assertEqual(newG.m, m)

    def test_save_graph_metis(self):
        G, n, m = HelperClass.createGraph()
        G.saveGraphAsMetis("test")

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
        G, n, m = HelperClass.createGraph()

        G.removeNode(0)
        G.addEdge(1, 10)

        G.saveGraphAsMetis("test")
        newG = HelperClass.readGraphMetis("test.txt")

        self.assertEqual(newG.n, n - 1)
        self.assertEqual(newG.m, m)
