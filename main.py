import random
import time

import numpy

'''
- On innovation numbers: nodes and connections share them (?)
- Innovation numbers are passed on through crossover; mutations result in brand new innovation numbers
- For each generation, keep a list of innovations. If the same innovations happens more than once, give it the same num
- Species representatives
- Ordered list of species
- Avg of fitnesses, not sum! For num of children
- During speciation, each network is compared against the representative from the *previous* generation (random!)
- 75% for gene to be disabled if disabled in either parent
- Elitism
- Kill off stagnated species
- 25% of offspring result from mutation without crossover
'''

from classes.Helpers.XORFitnessEvaluator import XORFitnessEvaluator
from classes.Puppeteers.Population import Population


def main():
    xor = XORFitnessEvaluator()
    pop = Population(xor)
    gen = 0
    mean = 0.0
    total = 0.0

    # pop.networks[0].genome.mutate_add_link()
    # # pop.networks[0].genome.mutate_add_node()
    # print(pop.networks[0].calculate([0, 1]))
    timeout = 100
    xor_inputs = [[1, 1], [0, 0], [1, 0], [0, 1]]
    while timeout > 0:
        xor = XORFitnessEvaluator()
        outs = {}
        pop.fitness_evaluator = xor
        random.shuffle(xor_inputs)
        inputs = [item for sublist in xor_inputs for item in sublist]
        ctr = 0
        for i in range(4):
            pop.propagate([inputs[ctr], inputs[ctr + 1]])
            ctr += 2

        # pop.propagate([1, 0])
        #
        # pop.propagate([0, 1])
        #
        # pop.propagate([0, 0])

        for i in pop.networks:
            outs[i] = i.outputs

            xor.calculate(i, outs, inputs)


        pop.evolve()
        gen += 1
        print("GENERATION " + str(gen))
        print(inputs)
        print('----------------')
        mean_score = 0.0
        for s in pop.species:
            print(str(len(s.members)))
            print("************")
        # mean_score /= 1000
        for n, v in xor.networks.items():
            # mean_score += v
            total += v
        # mean_score /= len(xor.networks.items())
        total /= len(xor.networks)
        print("MEAN SCORE: " + str(total/gen))
        print("================================")
        # time.sleep(1)
        timeout -= 1

    # print(xor.networks.items())
    # print(len(xor.networks.items()))
    # best = max(xor.networks, key=xor.networks.get)

    xor = XORFitnessEvaluator()
    outs = {}
    pop.fitness_evaluator = xor
    pop.propagate([1, 0])
    pop.propagate([0, 0])
    pop.propagate([1, 1])
    pop.propagate([0, 1])
    for i in pop.networks:
        outs[i] = i.outputs
        xor.calculate(i, outs, [1, 0, 0, 0, 1, 1, 0, 1])
    # outs = {best: best.calculate([0, 1])}
    # xor.calculate(best, outs, [0, 1])
    avg_0 = 0.0
    avg_1 = 0.0
    avg_2 = 0.0
    avg_3 = 0.0
    nets = sorted(pop.networks, key=lambda x: x.fitness)
    # nets = nets[:int(len(nets) * 0.2)]
    for i in nets:
        avg_0 += i.outputs[0]
        avg_1 += i.outputs[1]
        avg_2 += i.outputs[2]
        avg_3 += i.outputs[3]
        # print(i.outputs)
    avg_0 /= len(pop.networks)
    avg_1 /= len(pop.networks)
    avg_2 /= len(pop.networks)
    avg_3 /= len(pop.networks)
    print([avg_0, avg_1, avg_2, avg_3])
    # print(outs[best][4])


if __name__ == '__main__':
    main()

# pop = Population(None)
#
# na = pop.networks[0]
# nb = pop.networks[1]
#
# timeout = 5
# while timeout > 0:
#     pop.mutate()
#
#     timeout -= 1
#
# timeout = 5
# while timeout > 0:
#     children = []
#     for i in range(100):
#         child = pop.networks[random.choice(list(range(0, 99)))].get_child(pop.networks[random.choice(list(range(0, 99)))], pop.create_empty_genome())
#         children.append(child)
#     pop.networks = children
#     timeout -= 1
#     print(timeout)
#
# pop.mutate()
# print("he")



