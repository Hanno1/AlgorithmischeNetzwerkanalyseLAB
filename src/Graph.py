import src.CustomExceptions as Exc


class Graph:
    READ_MOD_EDGE_LIST = "edgeList"
    READ_MOD_METIS = "metis"

    def __init__(self, path=None, mode=READ_MOD_EDGE_LIST):
        self.edges = dict()
        self.n = 0
        self.m = 0

        self.max_idx = 0
        self.node_ids_internal_ids = dict()
        self.internal_ids_node_ids = dict()

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
                    line = line.replace("\n", "")
                    line_index += 1
                    if line[0] == "%" or line[0] == "#":
                        continue
                    split = line.split(" ")
                    if split[0] == "" or len(split) != 2:
                        raise Exc.UnknownSyntaxException(line_index, line)
                    self.add_edge(split[0], split[1])
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
            node_id = self.internal_ids_node_ids[key]
            value = self.edges[key]
            for connection in value:
                if connection >= key:
                    node_id_connection = self.internal_ids_node_ids[connection]
                    f.write(f"{node_id} {node_id_connection}\n")
        f.close()

    def save_graph_metis(self, name):
        try:
            f = open(name + ".txt", "x")
        except FileExistsError:
            f = open(name + ".txt", "w")

        f.write(f"{self.n} {self.m}")
        new_internal_mapping = dict()
        counter = 0
        for key in self.internal_ids_node_ids:
            new_internal_mapping[key] = counter
            counter += 1
        for key in self.edges:
            f.write("\n")
            first = True
            for connection in self.edges[key]:
                if first:
                    first = False
                    f.write(f"{new_internal_mapping[connection]}")
                    continue
                f.write(f" {new_internal_mapping[connection]}")
        f.close()

    def add_node(self, idx):
        if idx in self.node_ids_internal_ids:
            return
        internal_id = self.max_idx

        self.edges[internal_id] = set()

        self.node_ids_internal_ids[idx] = internal_id
        self.internal_ids_node_ids[internal_id] = idx
        self.max_idx += 1

        self.n += 1

    def remove_node(self, idx):
        # remove node and all connections to other nodes
        if idx not in self.node_ids_internal_ids:
            raise Exc.NodeDoesNotExistException(idx)

        internal_id = self.node_ids_internal_ids[idx]
        for c in self.edges[internal_id]:
            self.edges[c].remove(internal_id)
            self.m -= 1

        del self.edges[internal_id]

        del self.internal_ids_node_ids[internal_id]
        del self.node_ids_internal_ids[idx]

        self.n -= 1

    def add_edge(self, id1, id2):
        if id1 not in self.node_ids_internal_ids:
            self.add_node(id1)
        if id2 not in self.node_ids_internal_ids:
            self.add_node(id2)
        if id1 == id2:
            raise ValueError(f"Nodes have to be different!")
        # check if edge already exist
        if self.node_ids_internal_ids[id2] in self.edges[self.node_ids_internal_ids[id1]]:
            return

        self.edges[self.node_ids_internal_ids[id1]].add(self.node_ids_internal_ids[id2])
        self.edges[self.node_ids_internal_ids[id2]].add(self.node_ids_internal_ids[id1])

        self.m += 1

    def remove_edge(self, id1, id2):
        if id1 not in self.node_ids_internal_ids:
            raise Exc.NodeDoesNotExistException(id1)
        if id2 not in self.node_ids_internal_ids:
            raise Exc.NodeDoesNotExistException(id2)

        internal_id1 = self.node_ids_internal_ids[id1]
        internal_id2 = self.node_ids_internal_ids[id2]

        if internal_id1 not in self.edges[internal_id2]:
            raise Exc.EdgeDoesNotExistException(id1, id2)

        self.edges[internal_id1].remove(internal_id2)
        self.edges[internal_id2].remove(internal_id1)

        self.m -= 1

    def test_neighbors(self, id1, id2):
        if id1 not in self.node_ids_internal_ids:
            raise Exc.NodeDoesNotExistException(id1)
        elif id2 not in self.node_ids_internal_ids:
            raise Exc.NodeDoesNotExistException(id2)

        internal_id1 = self.node_ids_internal_ids[id1]
        internal_id2 = self.node_ids_internal_ids[id2]
        if internal_id1 in self.edges[internal_id2]:
            return True
        return False

    def get_neighbors(self, idx):
        if idx in self.node_ids_internal_ids:
            internal_id = self.node_ids_internal_ids[idx]
            edges = self.edges[internal_id]
            ret_edges = set()
            for edge in edges:
                ret_edges.add(self.internal_ids_node_ids[edge])
            return ret_edges
        raise Exc.NodeDoesNotExistException(idx)

    def get_node_degree(self, idx):
        return len(self.get_neighbors(idx))

    def print_nodes(self):
        s = ""
        for key in self.node_ids_internal_ids:
            s += str(key) + " "
        print(f"the Graph contains the following Nodes: {s}")

    def print_edges(self):
        for key in self.edges:
            node_id = self.internal_ids_node_ids[key]
            tmp = f"{node_id}: "
            value = self.edges[key]
            for v in value:
                node_id = self.internal_ids_node_ids[v]
                tmp += str(node_id) + " "
            print(tmp)
