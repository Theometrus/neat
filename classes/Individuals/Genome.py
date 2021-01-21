import random
from config.settings import *


class Genome:
    def __init__(self, nodes):
        self.nodes = nodes  # Has to be sorted by X value for more efficient computation in the future
        self.connections = []

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
        pass

    def mutate_add_link(self):
        pass

    def mutate_toggle_link(self):
        pass

    def mutate_weight_shift(self):
        pass

    def mutate_weight_reassign(self):
        pass
