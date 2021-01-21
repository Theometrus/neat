class Connection:
    def __init__(self, from_node, to_node, innovation_number):
        self.innovation_number = innovation_number
        self.from_node = from_node
        self.to_node = to_node
        self.weight = 0

    def clone(self):
        return Connection(self.from_node.clone(), self.to_node.clone(), self.innovation_number)
