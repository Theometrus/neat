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
        xor = XORFitnessEvaluator()
        outs = {}
        pop.fitness_evaluator = xor
        # inputs = [1, random.choice([0, 1]), random.choice([0, 1])]
        pop.propagate([0, 1])

        pop.propagate([0, 0])

        pop.propagate([1, 0])

        pop.propagate([1, 1])

        for i in pop.networks:
            outs[i] = i.outputs

            xor.calculate(i, outs)

        pop.evolve()
        gen += 1
        print("GENERATION " + str(gen))
        mean_score = 0.0
        for s in pop.species:
            print(str(len(s.members)))
            print("************")
        # mean_score /= 1000
        for n, v in xor.networks.items():
            mean_score += v
        mean_score /= 1000
        print("MEAN SCORE: " + str(mean_score))
        print("================================")
        # time.sleep(1)


if __name__ == '__main__':
    main()
