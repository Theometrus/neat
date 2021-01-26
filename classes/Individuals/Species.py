from config.settings import DELTA_THRESHOLD


class Species:
    def __init__(self):
        self.members = []
        self.total_fitness = 0.0
        self.new_size = 0
        self.private_delta = DELTA_THRESHOLD

    def calculate_fitnesses(self, fitness_evaluator):
        if len(self.members) == 0:
            self.total_fitness = 0.0
            return

        for i in self.members:
            i.fitness = fitness_evaluator.evaluate(i) / len(self.members)
            self.total_fitness += i.fitness
