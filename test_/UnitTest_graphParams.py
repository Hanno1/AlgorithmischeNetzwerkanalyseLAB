import src.graphParameters as gP
from src.Graph import Graph
import HelperClass as HelperClass
from unittest import TestCase
import unittest
import networkx as nx

#test-graph
nodes = list(range(1,11))
edges = [(3,2),(3,5),(3,5),(4,2),(4,5),(4,7),(4,8),(4,9),(9,7),(9,8),(9,10),(10,7),(10,8),(8,7)]

nxG = nx.Graph()
G = Graph()
for n in nodes:
    nxG.add_node(str(n))
    G.add_node(str(n))
for e in edges:
    i,j = e
    nxG.add_edge(str(i),str(j))
    G.add_edge(str(i),str(j))

class TestShortestPaths(TestCase):
    def test_hindex(self):
        self.assertEqual(gP.h_index(G), 4)

    def test_degeneracy(self):
        degeneracy, degeneracy_order = gP.degeneracy(G)

        self.assertEqual(degeneracy, 3)

        self.assertEqual(set(degeneracy_order), set(G.node_ids_internal_ids.keys()))
        for n in degeneracy_order:
            if G.get_node_degree(n) <= degeneracy:
                continue
            n_index = degeneracy_order.index(n)
            neighb_higher_order = 0
            for nn in G.get_neighbors(n):
                if degeneracy_order.index(nn) > n_index:
                    neighb_higher_order += 1
            self.assertGreaterEqual(degeneracy,neighb_higher_order)

    def test_cluster(self):
        glob_cluster = gP.global_clustering_coefficient(G)
        loc_cluster = {i:gP.local_clustering_coefficient(G,i) for i in G.node_ids_internal_ids.keys()}
        loc_cluster_nx = nx.clustering(nxG)
        for k in loc_cluster.keys():
            self.assertEqual(loc_cluster[k],loc_cluster_nx[k])

    def test_kcore(self):
        cores = gP.k_core_decomposition(G)
        core = set(G.node_ids_internal_ids.keys())
        for k in cores.keys():
            self.assertEqual(core,set(nx.k_core(nxG,k=int(k)).nodes))
            core = core - cores[k]

if __name__ == '__main__':
    unittest.main()