import src.networkCentrality.myCentrality as MyCentr
import test_.HelperClass as Hc
from src.printGraph import draw_graph as draw_graph
from src.Graph import Graph


G = Graph("../networks/out.ucidata-zachary_", mode=Graph.READ_MOD_EDGE_LIST)
print(MyCentr.ownCentrality(G, k=3))
