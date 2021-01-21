class Population:
    def tick(self, inputs):
        pass

    def evolve(self):
        self.speciate()
        self.erase_extinct_species()
        self.calculate_fitness()
        self.cull()
        self.crossover()
        self.mutate()
        pass

    def speciate(self):
        pass

    def erase_extinct_species(self):
        pass

    def calculate_fitness(self):
        pass

    def cull(self):
        pass

    def crossover(self):
        pass

    def mutate(self):
        pass
