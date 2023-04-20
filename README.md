# AlgorithmischeNetzwerkanalyseLAB

1 Milestone:

1.1 

a) We implemented a class "Graph()" that has the attributes G.nodes and G.edges as well as n and m. G.nodes is a Dictionary there the key is the index of a node and the corresponding value is an element of the Node class. The Node class does not do anything for now. G.edges is a dictionary that maps each node idx to a set of other node indicese. For example it may contain the entry "1: {2, 3}" meaning that the node with index 1 is connected to index 2 and 3. This Solution is not optimal since each edge appears 2 times. If we later introduce direction to an edge this will be usefull though.
The variable n is the total number of nodes and m corresponds to the number of edges in the Graph. 

b) To access the neighbors of a node with index i, you call the method G.getNeighbors(i)

c) We can test if nodes i and j are adjacent by calling the method G.testNeighbors(i, j)

d) We can access the degree of a node i by calling G.getNodeDegree(i)

e) To add Nodes and Edges there are the methods G.addNode(i) and G.addEdge(i, j). By adding a Node we check if the node with index i already exists. Adding a Edge checks if the node i and j exists (if not it adds them automatically) and the adds the edge between i and j. To delete Nodes and Edges there are the methods G.removeNode(i) and G.remove(Edge(i, j). If the node / edge does not exist we just return.

f) By just initialising G with Graph() we create an empty Graph

1.2

You can read a Graph from a file with Edgelist-format (i.e. "1 2" means there is a edge between 1 and 2 (undirected)), by initialising G with Graph(path). Additionally you can read a file in metis-format, by calling G = Graph(path, Graph.READ_MOD_METIS). Both reading methods will detect corrupted files. 
You can save a Graph to both formats as well by calling G.saveGraphAsEdgeList(name) or G.saveGraphAsMetis(name). In the case of a metis file it changes the indexing of the nodes.