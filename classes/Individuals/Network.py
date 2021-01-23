import sys

from config.settings import INPUT_NODES, OUT_NODE_X, IN_NODE_X, BIAS_NODE_X


class Network:
    def __init__(self, genome):
        self.species = None
        self.genome = genome
        self.fitness = 0.0
        self.outputs = []

    def get_child(self, partner, template):
        # The function makes assumptions, so the parameters must be given in the right order
        if self.fitness >= partner.fitness:
            return Network(self.genome.get_child(partner.genome, template))
        else:
            return Network(partner.genome.get_child(self.genome, template))

    def calculate(self, inputs):
        if len(inputs) != INPUT_NODES:
            print("Critical error: INPUT MISMATCH. Exiting")
            sys.exit()
        input_ctr = 0

        # Since the nodes are sorted by X, we can assume the sensors are all at the start
        for i in self.genome.nodes:
            if i.x >= OUT_NODE_X:
                self.outputs.append(i.calculate(inputs[input_ctr]))
            else:
                i.calculate(inputs[input_ctr])

            if input_ctr + 1 < len(inputs) and i.x != BIAS_NODE_X:
                input_ctr += 1

        return self.outputs

    def mutate(self):
        self.genome.mutate()

    def compare_to(self, network):
        return self.genome.compare_to(network.genome)
