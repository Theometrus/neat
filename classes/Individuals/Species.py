from config.settings import DELTA_THRESHOLD


class Species:
    def __init__(self, representative):
        self.members = []
        self.total_fitness = 0.0
        self.average_fitness = 0.0
        self.max_fitness = 0.0
        self.improved = False
        self.stagnation_timer = 15
        self.new_size = 0
        self.private_delta = DELTA_THRESHOLD
        self.representative = representative

    def calculate_fitnesses(self, fitness_evaluator):
        self.total_fitness = 0.0
        self.average_fitness = 0.0
        self.improved = False

        if len(self.members) == 0:
            self.total_fitness = 0.0
            return

        for i in self.members:
            i.fitness = fitness_evaluator.evaluate(i) / len(self.members)
            self.total_fitness += i.fitness
            if i.fitness > self.max_fitness:
                self.improved = True
                self.stagnation_timer = 15

        self.average_fitness = self.total_fitness / len(self.members)

        if not self.improved:
            self.stagnation_timer -= 1

