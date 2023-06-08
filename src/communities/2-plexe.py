from src.Graph import Graph
from src.printGraph import draw_graph
import test_.HelperClass as Hc


def test_2_plex(G: Graph):
    n = G.n
    for internal_node in G.internal_ids_node_ids:
        if len(G.get_internal_neighbors(internal_node)) < n-2:
            return False
    return True


def filter_2_plex(list_):
    maximal_length = 0
    new_list = []
    for G in list_:
        if G.n > maximal_length:
            maximal_length = G.n
    for G in list_:
        if G.n == maximal_length:
            return G


def search_2_plex_rec(H: Graph):
    H.print_nodes()
    if test_2_plex(H):
        print("found 2 plex")
        if H.n > 2:
            all_2_plex.append(H)
        return

    node_id_internal_id = H.node_ids_internal_ids
    for v in node_id_internal_id:
        print(v)
        # Case 1: v is not in max 2 plex
        # remove v
        newGraph = H.copy_graph()
        newGraph.remove_node(v)

        search_2_plex_rec(newGraph)

        # Case 2: v is in max 2 plex -> all neighbors might be too as well as one additional neighbor
        # remove not neighborhood
        neighborhood_v = H.get_neighbors(v)

        for u in neighborhood_v:
            newGraph = H.copy_graph()
            newGraph.remove_node(u)
            search_2_plex_rec(newGraph)


# G = Graph("../../networks/out.ucidata-zachary_")
# draw_graph(G, label_on=True)
G = Graph()
G.add_edge(10, 11)
G.add_edge(10, 13)
G.add_edge(11, 12)
G.add_edge(12, 13)
G.add_edge(13, 14)
G.add_edge(14, 15)
G.add_node(0)
# G, _, _ = Hc.create_graph()

all_2_plex = []
search_2_plex_rec(G)

filtering = filter_2_plex(all_2_plex)
filtering.print_edges()
