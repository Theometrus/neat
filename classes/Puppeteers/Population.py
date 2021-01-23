import random

from classes.Individuals.Genome import Genome
from classes.Individuals.Network import Network
from classes.Individuals.Species import Species
from classes.Puppeteers.InnovationGuardian import InnovationGuardian
from config.settings import INPUT_NODES, OUTPUT_NODES, IN_NODE_X, OUT_NODE_X, POPULATION_SIZE, DELTA_THRESHOLD, \
    SURVIVORS


class Population:
    def __init__(self, fitness_evaluator):
        # Note: fresh networks are created with no connections whatsoever. Connections must be mutated into
        self.networks = []
        self.species = []
        self.fitness_evaluator = fitness_evaluator
        self.innovation_guard = InnovationGuardian()

        self.initial_nodes = []
        self.make_starting_nodes()  # Template nodes for new networks to copy from
        self.make_starting_networks()  # Initial population members

    def propagate(self, inputs):
        outputs = []
        for i in self.networks:
            outputs.append(i.calculate(inputs))

        return outputs

    def evolve(self):
        self.speciate()
        self.erase_extinct_species()
        self.calculate_fitnesses()
        self.cull()
        self.crossover()
        self.mutate()

    def speciate(self):
        self.species = []

        for n in self.networks:
            classified = False

            for s in self.species:
                rep = random.choice(s.members)
                delta = n.compare_to(rep)
                if delta <= DELTA_THRESHOLD:
                    s.members.append(n)
                    n.species = s
                    classified = True
                    break

            if not classified:
                species = Species()
                species.members.append(n)
                self.species.append(species)

    def erase_extinct_species(self):
        # Prevent empty species lists from cluttering the program
        for s in self.species:
            if len(s.members) <= 1:
                if len(s.members == 1):
                    # Toss the remaining survivor into a random species and wish him all the best
                    random.choice(self.species).members.append(s.members[0])
                self.species.remove(s)

    def calculate_fitnesses(self):
        # Calculate the mean adjusted fitnesses based on the specifications described in the original NEAT paper
        for s in self.species:
            s.calculate_fitnesses()

    def cull(self):
        # Only keep the top performing members alive
        for s in self.species:
            s.members.sort(key=lambda x: x.fitness)
            cutoff = round((1 - SURVIVORS) * len(s.members))
            s.members = s.members[cutoff:]

    def crossover(self):
        self.networks = []

        for s in self.species:
            for i in range(s.new_size):
                parent_a, parent_b = random.sample(s.members, 2)
                child = parent_a.get_child(parent_b, self.create_empty_genome())
                s.members.append(child)
                self.networks.append(child)

    def mutate(self):
        for i in self.networks:
            i.mutate()

    def create_empty_genome(self):
        nodes_clone = []

        for node in self.initial_nodes:
            nodes_clone.append(node.clone())

        return Genome(nodes_clone, self.innovation_guard)

    def make_starting_nodes(self):
        for i in range(INPUT_NODES):
            node = self.innovation_guard.attempt_create_empty_node(len(self.initial_nodes), IN_NODE_X, i)
            self.initial_nodes.append(node)

        for i in range(OUTPUT_NODES):
            node = self.innovation_guard.attempt_create_empty_node(len(self.initial_nodes), OUT_NODE_X, i)
            self.initial_nodes.append(node)

    def make_starting_networks(self):
        for i in range(POPULATION_SIZE):
            genome = self.create_empty_genome()
            network = Network(genome)
            self.networks.append(network)
