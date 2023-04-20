from Node import Node


class Graph:
    READ_MOD_EDGE_LIST = "edgeList"
    READ_MOD_METIS = "metis"

    def __init__(self, path=None, modus=READ_MOD_EDGE_LIST):
        self.nodes = dict()
        self.edges = dict()
        self.n = 0
        self.m = 0

        if path is not None:
            if modus == self.READ_MOD_EDGE_LIST:
                self.readGraphAsEdgeList(path)
            elif modus == self.READ_MOD_METIS:
                self.readGraphAsMetis(path)
            else:
                print(f"Unknown mode for reading a file {modus}")

    def readGraphAsEdgeList(self, path):
        """
        read Graph as a edge list. meaning lines in the file have the form "1 2"...
        We will ignore comments that start with a "#" or a "%"
        throw an exception if the file is corrupted i.e. the line has not a correct format

        :param path: path there the file is stored
        """
        line_index = 0
        line = ""
        try:
            with open(path) as file:
                for line in file:
                    line_index += 1
                    if line[0] == "%" or line[0] == "#":
                        continue
                    split = line.split(" ")
                    if split[0] == "" or len(split) != 2:
                        raise IndexError
                    self.addEdge(split[0], split[1])
                file.close()
        except FileNotFoundError:
            print(f"No such file {path}")
            raise FileNotFoundError
        except IndexError:
            print(f"Found bad format at line number {line_index}: {line}")
            raise IndexError

    def readGraphAsMetis(self, path):
        try:
            with open(path) as file:
                first_line = file.readline()
                while not first_line or first_line[0] == "%" or first_line[0] == "#":
                    if not first_line:
                        print("Empty first line. Please correct format!")
                        raise Exception
                    first_line = file.readline()
                split = first_line.split(" ")
                n, m = int(split[0]), int(split[1])
                for idx in range(1, n + 1):
                    self.addNode(idx)
                counter = 1
                for line in file:
                    line = line.replace("\n", "")
                    if not line:
                        if counter > n:
                            raise ValueError
                        counter += 1
                        continue
                    if line[0] == "%" or line[0] == "#":
                        continue
                    if counter > n:
                        raise ValueError
                    split = line.split(" ")
                    for connection in split:
                        if int(connection) > n:
                            raise IndexError
                        self.addEdge(counter, int(connection))
                    counter += 1
                if self.m != m:
                    print("Number of edges is not right!")
        except FileNotFoundError:
            print(f"No such file {path}")
            raise FileNotFoundError
        except ValueError:
            print("too many lines. Please check file!")
            raise ValueError
        except IndexError:
            print(f"the node ids have to be numbers between 1 and {n}.")
            raise IndexError

    def saveGraphAsEdgeList(self, name):
        try:
            f = open(name + ".txt", "x")
        except FileExistsError:
            f = open(name + "txt", "w")
        for key in self.edges:
            value = self.edges[key]
            for connection in value:
                if connection >= key:
                    f.write(f"{key} {connection}\n")
        f.close()

    def saveGraphAsMetis(self, name):
        try:
            f = open(name + ".txt", "x")
        except FileExistsError:
            f = open(name + "txt", "w")

        f.write(f"{self.n} {self.m}")
        mapNodeId = dict()
        c = 1
        for key in self.nodes:
            mapNodeId[key] = c
            c += 1

        for key in self.edges:
            f.write("\n")
            for connection in self.edges[key]:
                f.write(f"{mapNodeId[connection]} ")
        f.close()

    def addNode(self, idx):
        if idx in self.nodes:
            print(f"Node with id {idx} exists already!")
            raise ValueError
        newNode = Node(idx, None)
        self.nodes[idx] = newNode
        self.edges[idx] = set()

        self.n += 1

    def removeNode(self, idx):
        # remove node and all connections to other nodes
        if idx not in self.nodes:
            return
        for c in self.edges[idx]:
            self.edges[c].remove(idx)
        del self.edges[idx]
        del self.nodes[idx]

        self.n -= 1

    def addEdge(self, id1, id2):
        if id1 == id2:
            print("Paths have to connect different nodes!")
            raise ValueError
        if id1 not in self.nodes:
            self.addNode(id1)
        if id2 not in self.nodes:
            self.addNode(id2)
        # check if edge already exist
        if id2 in self.edges[id1]:
            return
        self.edges[id1].add(id2)
        self.edges[id2].add(id1)

        self.m += 1

    def removeEdge(self, id1, id2):
        if id1 not in self.nodes or id2 not in self.nodes or \
                id2 not in self.edges[id1]:
            return
        self.edges[id1].remove(id2)
        self.edges[id2].remove(id1)

        self.m -= 1

    def testNeighbors(self, id1, id2):
        if id1 not in self.nodes or id2 not in self.nodes:
            print(f"Node {id1} or {id2} do not exist")
        if id1 in self.edges[id1]:
            return True
        return False

    def getNeighbors(self, idx):
        if idx in self.nodes:
            return self.edges[idx]
        print(f"Node {idx} does not exist")
        raise ValueError

    def getNodeDegree(self, idx):
        return len(self.getNeighbors(idx))

    def printNodes(self):
        s = ""
        for key in self.nodes:
            s += str(self.nodes[key].id) + " "
        print(f"the Graph contains the following Nodes: {s}")

    def printEdges(self):
        for key in self.edges:
            tmp = f"{key}: "
            value = self.edges[key]
            for v in value:
                tmp += str(v) + " "
            print(tmp)
