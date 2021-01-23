import random
import time

'''
known bugs: 
-species exploding
-calc always -0.5
-wrong nodes in connections
'''

from classes.Helpers.XORFitnessEvaluator import XORFitnessEvaluator
from classes.Puppeteers.Population import Population


def main():
    xor = XORFitnessEvaluator()
    pop = Population(xor)
    gen = 0

    # pop.networks[0].genome.mutate_add_link()
    # # pop.networks[0].genome.mutate_add_node()
    # print(pop.networks[0].calculate([0, 1]))
    while True:
        inputs = [random.choice([0, 1]), random.choice([0, 1])]
        pop.propagate(inputs)

        for i in pop.networks:
            xor.calculate(inputs, i)

        pop.evolve()
        gen += 1
        print("GENERATION " + str(gen))
        for s in pop.species:
            print(str(len(s.members)) + " -- " + str(s.fitness))
            print("************")
        print("================================")
        # time.sleep(1)
        xor = XORFitnessEvaluator()
        pop.fitness_evaluator = xor


if __name__ == '__main__':
    main()
