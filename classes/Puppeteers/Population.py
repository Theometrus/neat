import math
import random

from classes.Activation.Bias import Bias
from classes.Activation.Identity import Identity
from classes.Activation.Sigmoid import Sigmoid
from classes.Individuals.Genome import Genome
from classes.Individuals.Network import Network
from classes.Individuals.Node import Node
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
        self.innovation_guard.new_generation()
        self.speciate()
        self.erase_extinct_species()
        self.assign_new_representatives()
        self.calculate_fitnesses()
        self.adjust_species_sizes()
        self.cull()
        self.reproduce()
        self.clear_outputs()
        print("f")

    def speciate(self):
        for n in self.networks:
            n.species = None

        reps = []

        # Remove everyone except the rep from species
        for s in self.species:
            s.representative.species = s
            s.members = [s.representative]
            reps.append(s.representative)

        for n in self.networks:
            if n in reps:
                continue

            classified = False

            for s in self.species:
                delta = n.compare_to(s.representative)
                if delta <= DELTA_THRESHOLD:
                    s.members.append(n)
                    n.species = s
                    classified = True
                    break

            if not classified:
                species = Species(n)
                species.members.append(n)
                self.species.append(species)

    def assign_new_representatives(self):
        for s in self.species:
            s.representative = random.choice(s.members)

    def erase_extinct_species(self):
        # Prevent empty species lists from cluttering the program
        orphans = []

        for s in self.species:
            if len(s.members) == 1:  # Reassign lone members to random species
                orphans.append(s.members[0])

        self.species = [x for x in self.species if len(x.members) > 1]

        for o in orphans:
            rand_species = random.choice(self.species)
            rand_species.members.append(o)
            o.species = rand_species

    def calculate_fitnesses(self):
        # Calculate the mean adjusted fitnesses based on the specifications described in the original NEAT paper
        for s in self.species:
            s.calculate_fitnesses(self.fitness_evaluator)

    def adjust_species_sizes(self):
        mean_fitness = 0.0
        for s in self.species:
            mean_fitness += s.average_fitness

        mean_fitness /= len(self.networks)

        for s in self.species:
            if mean_fitness == 0:
                s.new_size = len(s.members)
                return
            s.new_size = round(s.average_fitness / mean_fitness)

    def cull(self):
        # Only keep the top performing members alive
        for s in self.species:
            s.members.sort(key=lambda x: x.fitness)
            cutoff = math.floor((1 - SURVIVORS) * len(s.members))
            if len(s.members) - cutoff < 2:  # Don't eradicate small species
                continue
            s.members = s.members[cutoff:]

    def reproduce(self):
        self.networks = []

        for s in self.species:
            offspring = [s.representative]
            self.networks.append(s.representative)

            for i in range(s.new_size - 1):  # Excluding the representative
                # Decide whether to use sexual (crossover) or asexual reproduction (mutation)
                if random.uniform(0.0, 1.0) <= MUTATION_RATE:
                    child = random.choice(s.members)
                    child.mutate()
                else:
                    parent_a, parent_b = random.sample(s.members, 2)
                    child = parent_a.get_child(parent_b, self.create_empty_genome())
                offspring.append(child)
                self.networks.append(child)
            s.members = offspring

    def clear_outputs(self):
        for i in self.networks:
            i.outputs = []

    def create_empty_genome(self):
        nodes_clone = []

        for node in self.initial_nodes:
            nodes_clone.append(node.clone())

        return Genome(nodes_clone, self.innovation_guard)

    def make_starting_nodes(self):
        for i in range(BIAS_NODES):
            node = Node(self.innovation_guard.node_innov, IN_NODE_X, i, Bias(), "BIAS")
            self.initial_nodes.append(node)
            self.innovation_guard.node_innov += 1

        for i in range(INPUT_NODES):
            node = Node(self.innovation_guard.node_innov, IN_NODE_X, i, Identity(), "SENSOR")
            self.initial_nodes.append(node)
            self.innovation_guard.node_innov += 1

        for i in range(OUTPUT_NODES):
            node = Node(self.innovation_guard.node_innov, OUT_NODE_X, i, Sigmoid(), "OUTPUT")
            self.initial_nodes.append(node)
            self.innovation_guard.node_innov += 1

    def make_starting_networks(self):
        for i in range(POPULATION_SIZE):
            genome = self.create_empty_genome()
            network = Network(genome)
            self.networks.append(network)
