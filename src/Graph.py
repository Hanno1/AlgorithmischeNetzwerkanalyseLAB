from src.Node import Node
import src.CustomExceptions as Exc


class Graph:
    READ_MOD_EDGE_LIST = "edgeList"
    READ_MOD_METIS = "metis"

    def __init__(self, path=None, mode=READ_MOD_EDGE_LIST):
        self.nodes = dict()
        self.edges = dict()
        self.n = 0
        self.m = 0

        if path is not None:
            if mode == self.READ_MOD_EDGE_LIST:
                self.read_graph_as_edge_list(path)
            elif mode == self.READ_MOD_METIS:
                self.read_graph_metis(path)
            else:
                print(f"Unknown mode for reading a file {mode}")

    def read_graph_as_edge_list(self, path):
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
                        raise Exc.UnknownSyntaxException(line_index, line)
                    self.add_edge(int(split[0]), int(split[1]))
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
                code_number: int = 0
                while not first_line or first_line[0] == "%" or first_line[0] == "#":
                    global_line_number += 1
                    if not first_line:
                        raise Exc.EmptyLineException(global_line_number)
                    first_line = file.readline()
                split = first_line.split(" ")
                n, m = int(split[0]), int(split[1])
                for idx in range(0, n):
                    self.add_node(idx)
                for line in file:
                    line = line.replace("\n", "")
                    if not line:
                        if code_number > n-1:
                            raise Exc.TooManyLinesException(global_line_number, line)
                        global_line_number += 1
                        code_number += 1
                        continue
                    if line[0] == "%" or line[0] == "#":
                        global_line_number += 1
                        continue
                    if code_number > n-1:
                        raise Exc.TooManyLinesException(global_line_number, line)
                    split = line.split(" ")
                    for connection in split:
                        if int(connection) > n-1:
                            raise Exc.BadNodeIdException(global_line_number, connection, n)
                        self.add_edge(code_number, int(connection))
                    code_number += 1
                    global_line_number += 1
                if self.m != m:
                    print("Number of edges is not right!")
                file.close()
        except FileNotFoundError:
            print(f"No such file {path}")
            raise FileNotFoundError

    def save_graph_as_edge_list(self, name):
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

    def save_graph_metis(self, name):
        try:
            f = open(name + ".txt", "x")
        except FileExistsError:
            f = open(name + ".txt", "w")

        f.write(f"{self.n} {self.m}")
        mapping = self.get_internal_mapping()
        for key in self.edges:
            f.write("\n")
            first = True
            for connection in self.edges[key]:
                if first:
                    first = False
                    f.write(f"{mapping[connection]}")
                    continue
                f.write(f" {mapping[connection]}")
        f.close()

    def get_internal_mapping(self):
        counter = 0
        internal_mapping = dict()
        for key in self.nodes:
            internal_mapping[key] = counter
            counter += 1
        return internal_mapping

    def add_node(self, idx: int):
        if type(idx) != int:
            raise ValueError(f"Expected Integer, got {type(idx)} instead!")
        if idx in self.nodes:
            raise ValueError(f"Node with id {idx} exists already!")
        new_node = Node(idx, None)
        self.nodes[idx] = new_node
        self.edges[idx] = set()

        self.n += 1

    def remove_node(self, idx):
        # remove node and all connections to other nodes
        if idx not in self.nodes:
            raise Exc.NodeDoesNotExistException(idx)
        for c in self.edges[idx]:
            self.edges[c].remove(idx)
            self.m -= 1
        del self.edges[idx]
        del self.nodes[idx]

        self.n -= 1

    def add_edge(self, id1, id2):
        if id1 not in self.nodes:
            self.add_node(id1)
        if id2 not in self.nodes:
            self.add_node(id2)
        # check if edge already exist
        if id2 in self.edges[id1]:
            return
        self.edges[id1].add(id2)
        self.edges[id2].add(id1)

        self.m += 1

    def remove_edge(self, id1, id2):
        if id1 not in self.nodes or id2 not in self.nodes or \
                id2 not in self.edges[id1]:
            return
        self.edges[id1].remove(id2)
        self.edges[id2].remove(id1)

        self.m -= 1

    def test_neighbors(self, id1, id2):
        if id1 not in self.nodes:
            raise Exc.NodeDoesNotExistException(id1)
        elif id2 not in self.nodes:
            raise Exc.NodeDoesNotExistException(id2)
        if id2 in self.edges[id1]:
            return True
        return False

    def get_neighbors(self, idx):
        if idx in self.nodes:
            return self.edges[idx]
        raise Exc.NodeDoesNotExistException(idx)

    def get_node_degree(self, idx):
        return len(self.get_neighbors(idx))

    def print_nodes(self):
        s = ""
        for key in self.nodes:
            s += str(self.nodes[key].id) + " "
        print(f"the Graph contains the following Nodes: {s}")

    def print_edges(self):
        for key in self.edges:
            tmp = f"{key}: "
            value = self.edges[key]
            for v in value:
                tmp += str(v) + " "
            print(tmp)
