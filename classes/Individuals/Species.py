class Species:
    def __init__(self):
        self.members = []
        self.fitness = 0.0
        self.new_size = 0

    def calculate_fitnesses(self, fitness_evaluator):
        if len(self.members) == 0:
            self.fitness = 0.0
            return

        for i in self.members:
            i.fitness = fitness_evaluator.evaluate(i) / len(self.members)
            self.fitness += i.fitness
        sum_fitnesses = self.fitness
        self.fitness /= len(self.members)
        self.new_size = 0 if self.fitness == 0 else round(sum_fitnesses / self.fitness)
