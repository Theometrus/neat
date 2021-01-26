from config.settings import DELTA_THRESHOLD


class Species:
    def __init__(self, representative):
        self.members = []
        self.total_fitness = 0.0
        self.average_fitness = 0.0
        self.new_size = 0
        self.private_delta = DELTA_THRESHOLD
        self.representative = representative

    def calculate_fitnesses(self, fitness_evaluator):
        self.total_fitness = 0.0
        self.average_fitness = 0.0

        if len(self.members) == 0:
            self.total_fitness = 0.0
            return

        for i in self.members:
            i.fitness = fitness_evaluator.evaluate(i) / len(self.members)
            self.total_fitness += i.fitness

        self.average_fitness = self.total_fitness / len(self.members)
