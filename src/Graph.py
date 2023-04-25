from src.Node import Node
import src.exception as exc


class Graph:
    READ_MOD_EDGE_LIST = "edgeList"
    READ_MOD_METIS = "metis"

    def __init__(self, path=None, modus=READ_MOD_EDGE_LIST):
        self.nodes = dict()
        self.edges = dict()
        self.n = 0
        self.m = 0

        self.internal_mapping = dict()

        if path is not None:
            if modus == self.READ_MOD_EDGE_LIST:
                self.readGraphAsEdgeList(path)
            elif modus == self.READ_MOD_METIS:
                self.read_graph_metis(path)
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
        try:
            with open(path) as file:
                for line in file:
                    line_index += 1
                    if line[0] == "%" or line[0] == "#":
                        continue
                    split = line.split(" ")
                    if split[0] == "" or len(split) != 2:
                        raise exc.UnknownSyntax(line_index, line)
                    self.addEdge(int(split[0]), int(split[1]))
                file.close()
        except FileNotFoundError:
            print(f"No such file {path}")
            raise FileNotFoundError

    def read_graph_metis(self, path):
        try:
            with open(path) as file:
                first_line = file.readline()
                # global line number encodes the real line in the file we read. It will count comment lines.
                # code_number wont count comment lines
                global_line_number: int = 0
                code_number: int = 1
                while not first_line or first_line[0] == "%" or first_line[0] == "#":
                    global_line_number += 1
                    if not first_line:
                        raise exc.EmptyLine(global_line_number)
                    first_line = file.readline()
                split = first_line.split(" ")
                n, m = int(split[0]), int(split[1])
                for idx in range(1, n + 1):
                    self.addNode(idx)
                for line in file:
                    line = line.replace("\n", "")
                    if not line:
                        if code_number > n:
                            raise exc.TooManyLines(global_line_number, line)
                        global_line_number += 1
                        code_number += 1
                        continue
                    if line[0] == "%" or line[0] == "#":
                        global_line_number += 1
                        continue
                    if code_number > n:
                        raise exc.TooManyLines(global_line_number, line)
                    split = line.split(" ")
                    for connection in split:
                        if int(connection) > n:
                            raise exc.BadNodeId(global_line_number, connection, n)
                        self.addEdge(code_number, int(connection))
                    code_number += 1
                    global_line_number += 1
                if self.m != m:
                    print("Number of edges is not right!")
                file.close()
        except FileNotFoundError:
            print(f"No such file {path}")
            raise FileNotFoundError

    def saveGraphAsEdgeList(self, name):
        try:
            f = open(name + ".txt", "x")
        except FileExistsError:
            f = open(name + ".txt", "w")
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
            f = open(name + ".txt", "w")

        f.write(f"{self.n} {self.m}")
        mapNodeId = dict()
        c = 1
        for key in self.nodes:
            mapNodeId[key] = c
            c += 1
        for key in self.edges:
            f.write("\n")
            first = True
            for connection in self.edges[key]:
                if not first:
                    f.write(" ")
                first = False
                f.write(f"{mapNodeId[connection]}")
        f.close()

    def addNode(self, idx: int):
        if type(idx) != int:
            print(f"Expected Integer, got {type(idx)} instead!")
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
            raise exc.NodeDoesNotExist(idx)
        for c in self.edges[idx]:
            self.edges[c].remove(idx)
            self.m -= 1
        del self.edges[idx]
        del self.nodes[idx]

        self.n -= 1

    def addEdge(self, id1, id2):
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
        if id1 not in self.nodes:
            raise exc.NodeDoesNotExist(id1)
        elif id2 not in self.nodes:
            raise exc.NodeDoesNotExist(id2)
        if id2 in self.edges[id1]:
            return True
        return False

    def getNeighbors(self, idx):
        if idx in self.nodes:
            return self.edges[idx]
        raise exc.NodeDoesNotExist(idx)

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
