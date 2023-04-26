from src.Graph import Graph


def create_graph():
    G = Graph()
    n = 0
    m = 0

    for i in range(-1, 14):
        G.add_node(i)
        n += 1
    G.add_node(15)
    n += 1

    # connected component 1
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    G.add_edge(3, 5)
    m += 5

    # 2
    G.add_edge(6, 7)
    G.add_edge(6, 8)
    m += 2

    # 3
    G.add_edge(0, -1)
    m += 1

    # 4
    G.add_edge(10, 11)
    G.add_edge(11, 12)
    G.add_edge(12, 13)
    G.add_edge(10, 13)
    m += 4

    return G, n, m


def create_graph_text():
    G = Graph()

    G.add_node("Node1")
    G.add_node("Node2")

    G.add_edge("Node3", "Node4")
    G.add_edge("Node1", 2)
    G.add_edge("Node1", "HelloWorld")
    G.add_edge(2, 3)
    G.add_edge(3, "Node4")
    G.add_edge(":)", ":(")

    return G, 9, 6


def read_graph_as_edge_list(path):
    return Graph(path, Graph.READ_MOD_EDGE_LIST)


def read_graph_metis(path):
    return Graph(path, Graph.READ_MOD_METIS)
