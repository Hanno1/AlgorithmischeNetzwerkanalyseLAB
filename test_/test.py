import src.communities.two_plexe as Tp
import src.shortestPaths as Sp
from src.Graph import Graph


G = Graph("../../networks/out.ucidata-zachary_")

all_pairs_shortest_paths = Sp.all_pairs_shortest_path_single(G)

print(Tp._search_2_plex_rec_orig(G, G.get_nodes(), []))
print(Tp._search_2_plex_rec_first(G, G.get_nodes(), [], []))
print(Tp._search_2_plex_rec_second(G, all_pairs_shortest_paths, G.get_nodes(), [], []))
print(Tp._search_2_plex_rec_third(G, all_pairs_shortest_paths, G.get_nodes(), [], []))
print(Tp._search_2_plex_rec_fourth(G, all_pairs_shortest_paths, G.get_nodes(), [], []))

"""
G = Graph("../../networks/out.ucidata-zachary_")

all_pairs_shortest_paths = Sp.all_pairs_shortest_path_single(G)

nodes = list(G.node_ids_internal_ids.keys())
nodes.sort()

print(search_2_plex_rec_orig(G, nodes, []))
print(search_2_plex_rec_first(G, nodes, [], []))
print(search_2_plex_rec_second(G, all_pairs_shortest_paths, nodes, [], []))
print(search_2_plex_rec_third(G, all_pairs_shortest_paths, nodes, [], []))
print(search_2_plex_rec_fourth(G, all_pairs_shortest_paths, nodes, [], []))
"""
