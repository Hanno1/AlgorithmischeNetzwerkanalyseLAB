class UnknownSyntax(Exception):
    def __init__(self, number=None, line=None):
        if number is not None and line is not None:
            super().__init__(f"Unknown Syntax at line {number}: {line}")
        super().__init__("Unknown Syntax.")


class EmptyLine(Exception):
    def __init__(self, number=None):
        if number is not None:
            super().__init__(f"Empty Line at line {number}")
        super().__init__("Empty Line in File.")


class TooManyLines(Exception):
    def __init__(self, number=None, max_lines=None):
        if number and max_lines:
            super().__init__(f"File has too many Lines (found {number}, expected {max_lines}).")
        super().__init__("File has too many Lines.")


class BadNodeId(Exception):
    def __init__(self, line_number, idx, max_id):
        super().__init__(f"Unknown Node id {idx} at line {line_number}. Maximal possible node id is {max_id}.")


class NodeDoesNotExist(Exception):
    def __init__(self, idx):
        super().__init__(f"Node with id {idx} does not exist!")
