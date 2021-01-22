class Network:
    def __init__(self, genome):
        self.species = None
        self.genome = genome
        self.fitness = 0.0

    def compare(self, network):
        pass

    def get_offspring(self, partner):
        pass

    def calculate(self, inputs):
        pass

    def mutate(self):
        self.genome.mutate()

    def compare_to(self, network):
        return self.genome.compare_to(network.genome)
