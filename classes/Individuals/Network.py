class Network:
    def __init__(self, genome):
        self.species = None
        self.genome = genome
        self.fitness = 0.0
        self.outputs = []

    def compare(self, network):
        return self.genome.compare_to(network.genome)

    def get_child(self, partner, template):
        # The function makes assumptions, so the parameters must be given in the right order
        if self.fitness >= partner.fitness:
            return self.genome.get_child(partner, template)
        else:
            return partner.genome.get_child(self, template)

    def calculate(self, inputs):
        for i in self.genome.nodes:
            i.calculate(inputs)

    def mutate(self):
        self.genome.mutate()

    def compare_to(self, network):
        return self.genome.compare_to(network.genome)
