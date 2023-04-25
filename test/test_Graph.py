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
        G.removeNode(1)

        self.assertEqual(G.n, n-1)
        self.assertEqual(G.m, m-2)

        # remove node that doesnt exist -> there should be an error
        self.assertRaises(exc.NodeDoesNotExist, G.removeNode, 1)

    def test_remove_edge(self):
        G, n, m = HelperClass.createGraph()

        G.removeEdge(1, 2)
        self.assertEqual(G.n, n)
        self.assertEqual(G.m, m-1)

        G.removeEdge(1, 2)
        self.assertEqual(G.m, m-1)

    def test_neighbors(self):
        G, n, m = HelperClass.createGraph()

        self.assertEqual(G.testNeighbors(1, 2), True)
        self.assertEqual(G.testNeighbors(2, 1), True)
        self.assertEqual(G.testNeighbors(1, 3), True)
        self.assertEqual(G.testNeighbors(-1, 2), False)
        self.assertEqual(G.testNeighbors(-1, 12), True)

        G.removeEdge(1, 2)
        self.assertEqual(G.testNeighbors(1, 2), False)
        self.assertEqual(G.testNeighbors(2, 1), False)

        self.assertEqual(G.testNeighbors(1, 1), False)

        G.removeNode(12)
        self.assertRaises(exc.NodeDoesNotExist, G.testNeighbors, -1, 12)

    def test_get_neighbors(self):
        G, n, m = HelperClass.createGraph()

        self.assertEqual(G.getNeighbors(1), {2, 3})
        self.assertEqual(G.getNeighbors(-1), {12})
        self.assertEqual(G.getNeighbors(4), set())

        self.assertRaises(exc.NodeDoesNotExist, G.getNeighbors, 13)

    def test_node_degree(self):
        G, n, m = HelperClass.createGraph()

        self.assertEqual(G.getNodeDegree(1), 2)
        self.assertEqual(G.getNodeDegree(3), 1)
        self.assertEqual(G.getNodeDegree(4), 0)

        self.assertRaises(exc.NodeDoesNotExist, G.getNodeDegree, 10)

    def test_save_graph_edge_list(self):
        G, n, m = HelperClass.createGraph()

        G.saveGraphAsEdgeList("test")

        with open("test.txt") as file:
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "0 11")
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "1 2")
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "1 3")
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "2 5")

    def test_read_graph_edge_list(self):
        G, n, m = HelperClass.createGraph()

        G.removeNode(0)
        G.addNode(10)
        G.addEdge(1, 10)

        G.saveGraphAsEdgeList("test")

        newG = HelperClass.readGraphEdgeList("test.txt")

        self.assertEqual(newG.n, 9)
        self.assertEqual(newG.m, m)

    def test_save_graph_metis(self):
        G, n, m = HelperClass.createGraph()
        G.saveGraphAsMetis("test")

        with open("test.txt") as file:
            line = file.readline().replace("\n", "")
            self.assertEqual(line, f"{n} {m}")
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "10")
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "2 3")
            line = file.readline().replace("\n", "")
            self.assertEqual(line, "1 5")

    def test_read_graph_metis(self):
        G, n, m = HelperClass.createGraph()

        G.removeNode(0)
        G.addNode(10)
        G.addEdge(1, 10)

        G.saveGraphAsMetis("test")

        newG = HelperClass.readGraphMetis("test.txt")

        self.assertEqual(newG.n, n)
        self.assertEqual(newG.m, m)
