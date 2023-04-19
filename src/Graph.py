from Node import Node


class Graph:
    def __init__(self, path=None, modus="edgeList"):
        self.maxNodeId = 0
        self.nodes = dict()
        self.edges = dict()

    def readGraphAsEdgeList(self, path):
        pass

    def readGraphAsMetis(self, path):
        pass

    def saveGraphAsEdgeList(self, path):
        pass

    def saveGraphAsMetis(self, path):
        pass

    def addNode(self):
        newNode = Node(self.maxNodeId)
        self.nodes[self.maxNodeId] = newNode
        self.maxNodeId += 1

    def addEdge(self, id1, id2):
        node1 = self.nodes[id1]
        node2 = self.nodes[id2]

        
