class Species:
    def __init__(self):
        self.members = []
        self.fitness = 0.0
        self.new_size = 0

    def calculate_fitnesses(self, fitness_evaluator):
        for i in self.members:
            i.fitness = fitness_evaluator.evaluate(i) / len(self.members)
            self.fitness += i.fitness
        sum_fitnesses = self.fitness
        self.fitness /= len(self.members)
        self.new_size = round(sum_fitnesses / self.fitness)

