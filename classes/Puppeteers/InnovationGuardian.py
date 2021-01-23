from classes.Activation.Bias import Bias
from classes.Activation.Identity import Identity
from classes.Activation.ReLU import ReLU
from classes.Activation.Sigmoid import Sigmoid
from classes.Individuals.Connection import Connection
from classes.Individuals.Node import Node
from config.settings import INPUT_NODES, OUTPUT_NODES, IN_NODE_X, OUT_NODE_X


class InnovationGuardian:
    """
    Responsible for keeping track of all unique nodes and connections,
    and assigning innovation numbers to them.
    """

    def __init__(self):
        self.nodes = {}  # Keys are innovation numbers based on the connection this node split (except initial nodes)
        self.connections = {}  # Keys are tuples consisting of innovation numbers of (from_node, to_node)
        self.latest_innovation = INPUT_NODES + OUTPUT_NODES - 1  # Node and connection innovation numbers are shared

    def attempt_create_empty_node(self, innovation_number, x, y, node_type):
        # Will return a shell of an existing node if possible, otherwise create a new one
        if self.nodes.get(innovation_number) is not None:
            return self.nodes.get(innovation_number).clone()

        if node_type == "SENSOR":
            activation_fn = Identity()

        elif node_type == "OUTPUT":
            activation_fn = Sigmoid()

        elif node_type == "BIAS":
            activation_fn = Bias()

        else:  # Hidden node
            activation_fn = ReLU()
            node_type = "HIDDEN"

        node = Node(innovation_number, x, y, activation_fn, node_type)
        self.nodes[innovation_number] = node.clone()

        return node

    def attempt_create_empty_connection(self, from_node, to_node):
        from_innovation = from_node.innovation_number
        to_innovation = to_node.innovation_number

        if self.connections.get((from_innovation, to_innovation)) is not None:
            return self.connections.get((from_innovation, to_innovation)).clone()

        self.latest_innovation += 1

        conn = Connection(from_node, to_node, self.latest_innovation)
        self.connections[(from_innovation, to_innovation)] = conn.clone()

        return conn
