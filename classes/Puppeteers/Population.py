from classes.Individuals.Genome import Genome
from classes.Individuals.Network import Network
from classes.Puppeteers.InnovationGuardian import InnovationGuardian
from config.settings import INPUT_NODES, OUTPUT_NODES, IN_NODE_X, OUT_NODE_X, POPULATION_SIZE


class Population:
    def __init__(self):
        # Note: fresh networks are created with no connections whatsoever. Connections must be mutated into
        self.networks = []
        self.species = []
        self.innovation_guard = InnovationGuardian()

        # Template nodes for new networks to copy from
        self.initial_nodes = []
        self.make_starting_nodes()
        self.make_starting_networks()

    # TODO CONSIDER THE BELOW TWO FUNCTIONS. How will fitness / propagation be abstracted from the user?
    def propagate(self, inputs):
        outputs = []
        for i in self.networks:
            outputs.append(i.calculate(inputs))

        return outputs

    def set_fitness(self, idx, fitness):
        self.networks[idx].fitness = fitness

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
        # Prevent empty species lists from cluttering the program
        for species in self.species:
            if len(species.members) == 0:
                self.species.remove(species)

    def calculate_fitness(self):
        pass

    def cull(self):
        pass

    def crossover(self):
        pass

    def mutate(self):
        pass

    def create_empty_genome(self):
        nodes_clone = []

        for node in self.initial_nodes:
            nodes_clone.append(node.clone())

        return Genome(nodes_clone)

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
