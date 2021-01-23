from config.settings import IN_NODE_X


class Node:
    def __init__(self, innovation_number, x, y, activation_fn):
        """
        :param x: X coordinate. Used for drawing, preventing cycles, and determining order of calculations
        :param y: Y coordinate. Used for drawing
        """
        self.innovation_number = innovation_number
        self.in_links = []
        self.out_links = []
        self.x = x
        self.y = y
        self.output = 0.0
        self.activation_fn = activation_fn

    def calculate(self, input_val):
        if self.x <= IN_NODE_X:  # Sensor node
            self.output = self.activation_fn.compute(input_val)

        else:  # Hidden or output node
            for link in self.in_links:
                self.output += link.weight * link.from_node.output

            self.output = self.activation_fn.compute(self.output)
        return self.output

    def clone(self):
        return Node(self.innovation_number, self.x, self.y, self.activation_fn)
