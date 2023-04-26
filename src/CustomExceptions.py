class UnknownSyntaxException(Exception):
    def __init__(self, number, line):
        super().__init__(f"Unknown Syntax at line {number}: {line}")


class EmptyLineException(Exception):
    def __init__(self, number):
        super().__init__(f"Empty Line at line {number}")


class TooManyLinesException(Exception):
    def __init__(self, number, max_lines):
        super().__init__(f"File has too many Lines (found {number}, expected {max_lines}).")


class BadNodeIdException(Exception):
    def __init__(self, line_number, idx, max_id):
        super().__init__(f"Unknown Node id {idx} at line {line_number}. Maximal possible node id is {max_id}.")


class NodeDoesNotExistException(Exception):
    def __init__(self, idx):
        super().__init__(f"Node with id {idx} does not exist!")


class EdgeDoesNotExistException(Exception):
    def __init__(self, idx1, idx2):
        super().__init__(f"Edge between id {idx1} and {idx2} does not exist!")
