import random

from classes.Individuals.Connection import Connection
from classes.Individuals.Node import Node
from config.settings import *


class Genome:
    def __init__(self, nodes, innovation_guardian):
        self.nodes = nodes  # Note: Must be sorted by X value for more efficient computation in the future
        self.connections = []  # Note: Must be sorted by innovation number for faster comparisons
        self.connection_dict = {}  # Used for quickly checking if a given connection already exists in this genome
        self.innovation_guardian = innovation_guardian

    def find_enabled_connection(self):
        found = False
        conn = None

        # Will try to find a connection before timing out
        for i in range(100):
            conn = random.choice(self.connections)
            if not conn.is_enabled:  # Prevent nodes from being created on disabled links
                continue

            found = True
            break

        if not found:
            return None

        return conn

    def mutate(self):
        if random.uniform(0.0, 1.0) <= MUT_ADD_NODE:
            self.mutate_add_node()
        if random.uniform(0.0, 1.0) <= MUT_ADD_LINK:
            self.mutate_add_link()
        if random.uniform(0.0, 1.0) <= MUT_TOGGLE_LINK:
            self.mutate_toggle_link()
        if random.uniform(0.0, 1.0) <= MUT_WEIGHT_SHIFT:
            self.mutate_weight_shift()
        if random.uniform(0.0, 1.0) <= MUT_WEIGHT_REASSIGN:
            self.mutate_weight_reassign()

    def mutate_add_node(self):
        if len(self.connections) == 0:
            return

        conn = self.find_enabled_connection()

        if conn is None:
            return

        conn.is_enabled = False
        x = (conn.to_node.x + conn.from_node.x) / 2
        y = ((conn.to_node.y + conn.from_node.y) / 2) * random.uniform(0.6, 1.4)  # Perturb the Y for better drawing

        node: Node = self.innovation_guardian.attempt_create_empty_node(conn.innovation_number, x, y)
        conn_a: Connection = self.innovation_guardian.attempt_create_empty_connection(conn.from_node, node)
        conn_b: Connection = self.innovation_guardian.attempt_create_empty_connection(node, conn.to_node)

        conn_a.weight = 1.0
        conn_b.weight = conn.weight

        node.in_links.append(conn_a)
        node.out_links.append(conn_b)
        node.connections += [conn_a, conn_b]

        conn.from_node.out_links.append(conn_a)
        conn.from_node.connections.append(conn_a)

        conn.to_node.in_links.append(conn_b)
        conn.to_node.connections.append(conn_b)

        self.connections += [conn_a, conn_b]
        self.nodes.append(node)

        self.connection_dict[(conn.from_node.innovation_number, node.innovation_number)] = conn_a
        self.connection_dict[(node.innovation_number, conn.to_node.innovation_number)] = conn_b

        # Insert the new node into this genome in a sorted fashion, for faster computation in the future
        for idx, n in enumerate(self.nodes):
            if n.x <= node.x <= self.nodes[idx + 1].x:
                self.nodes.insert(idx + 1, node)
                break

    def mutate_add_link(self):
        node_a = None
        node_b = None
        found = False

        # Keep trying to find two nodes without a connection between them
        for i in range(100):
            node_a = random.choice(self.nodes)
            node_b = random.choice(self.nodes)

            if node_a == node_b \
                    or self.connection_dict.get((node_a.innovation_number, node_b.innovation_number)) is not None \
                    or self.connection_dict.get((node_b.innovation_number, node_a.innovation_number)) is not None \
                    or node_a.x == node_b.x:  # Prevent connections amongst sensors and output nodes
                continue

            found = True
            break

        if not found:
            return

        # Connections are only created from a lower to a higher X to prevent cycles and assist in calculation sequencing
        if node_a.x > node_b.x:
            temp = node_a
            node_a = node_b
            node_b = temp

        conn = self.innovation_guardian.attempt_create_empty_connection(node_a, node_b)

        conn.weight = random.uniform(-3.0, 3.0)

        for idx, c in enumerate(self.connections):
            if idx + 1 >= len(self.connections):
                self.connections.append(conn)
                break

            if c.innovation_number <= conn.innovation_number <= self.connections[idx + 1].innovation_number:
                self.connections.insert(idx + 1, conn)
                break

        self.connection_dict[(node_a.innovation_number, node_b.innovation_number)] = conn

        node_a.out_links.append(conn)
        node_a.connections.append(conn)

        node_b.in_links.append(conn)
        node_b.connections.append(conn)

    def mutate_toggle_link(self):
        # Randomly turns a connection on or off
        conn = random.choice(self.connections)
        conn.is_enabled = not conn.is_enabled

    def mutate_weight_shift(self):
        # Nudges a connection's weight slightly in a random direction
        conn = self.find_enabled_connection()

        if conn is not None:
            conn.weight += random.uniform(-2.0, 2.0)

    def mutate_weight_reassign(self):
        # Completely randomizes a connection's weight
        conn = self.find_enabled_connection()

        if conn is not None:
            conn.weight = random.uniform(-3.0, 3.0)

    def compare_to(self, genome):
        idx_a = 0
        idx_b = 0
        disjoint = 0
        excess = 0
        similar = 0
        weight_diff = 0.0

        while idx_a <= len(self.connections) and idx_b <= len(genome.connections):
            innov_a = self.connections[idx_a].innovation_number
            innov_b = genome.connections[idx_b].innovation_number

            if innov_a == innov_b:
                similar += 1
                idx_a += 1
                idx_b += 1
                weight_diff += abs(self.connections[idx_a] - genome.connections[idx_b])

            elif innov_a < innov_b:
                disjoint += 1
                idx_a += 1

            else:
                disjoint += 1
                idx_b += 1

        excess = abs(len(self.connections) - len(genome.connections))
        weight_diff /= similar
        length = max(len(self.connections), len(genome.connections))

        delta = (EXCESS_COEFFICIENT * excess / length) + (
                    DISJOINT_COEFFICIENT * disjoint / length) + WEIGHT_COEFFICIENT * weight_diff

        return delta
