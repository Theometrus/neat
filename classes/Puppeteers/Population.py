import math
import random

from classes.Individuals.Genome import Genome
from classes.Individuals.Network import Network
from classes.Individuals.Species import Species
from classes.Puppeteers.InnovationGuardian import InnovationGuardian
from config.settings import *


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
        self.calculate_fitnesses()
        self.adjust_species_sizes()
        self.cull()
        self.crossover()
        self.erase_extinct_species()
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
        self.species = [x for x in self.species if len(x.members) >= 1]

    def calculate_fitnesses(self):
        # Calculate the mean adjusted fitnesses based on the specifications described in the original NEAT paper
        for s in self.species:
            s.calculate_fitnesses(self.fitness_evaluator)

    def adjust_species_sizes(self):
        mean_fitness = 0.0
        for s in self.species:
            mean_fitness += s.total_fitness

        mean_fitness /= len(self.networks)

        for s in self.species:
            s.new_size = round(s.total_fitness / mean_fitness)

    def cull(self):
        # Only keep the top performing members alive
        for s in self.species:
            s.members.sort(key=lambda x: x.fitness)
            cutoff = math.floor((1 - SURVIVORS) * len(s.members))
            s.members = s.members[cutoff:]

    def crossover(self):
        self.networks = []

        for s in self.species:
            offspring = []

            if len(s.members) == 1:
                # Asexual reproduction for 1 member species
                s.members.append(s.members[0].get_child(s.members[0], self.create_empty_genome()))
            elif len(s.members) == 0:
                continue

            for i in range(s.new_size):
                parent_a, parent_b = random.sample(s.members, 2)
                child = parent_a.get_child(parent_b, self.create_empty_genome())
                offspring.append(child)
                self.networks.append(child)
            s.members = offspring

    def mutate(self):
        for i in self.networks:
            i.mutate()

    def create_empty_genome(self):
        nodes_clone = []

        for node in self.initial_nodes:
            nodes_clone.append(node.clone())

        return Genome(nodes_clone, self.innovation_guard)

    def make_starting_nodes(self):
        for i in range(BIAS_NODES):
            node = self.innovation_guard.attempt_create_empty_node(len(self.initial_nodes), IN_NODE_X, i, "BIAS")
            self.initial_nodes.append(node)

        for i in range(INPUT_NODES):
            node = self.innovation_guard.attempt_create_empty_node(len(self.initial_nodes), IN_NODE_X, i, "SENSOR")
            self.initial_nodes.append(node)

        for i in range(OUTPUT_NODES):
            node = self.innovation_guard.attempt_create_empty_node(len(self.initial_nodes), OUT_NODE_X, i, "OUTPUT")
            self.initial_nodes.append(node)

    def make_starting_networks(self):
        for i in range(POPULATION_SIZE):
            genome = self.create_empty_genome()
            network = Network(genome)
            self.networks.append(network)
