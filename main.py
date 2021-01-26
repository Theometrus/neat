import random

'''
- 75% for gene to be disabled if disabled in either parent
- Kill off stagnated species
'''

from classes.Helpers.XORFitnessEvaluator import XORFitnessEvaluator
from classes.Puppeteers.Population import Population


def main():
    xor = XORFitnessEvaluator()
    pop = Population(xor)
    gen = 0

    timeout = 500
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

        for i in pop.networks:
            outs[i] = i.outputs

            xor.calculate(i, outs, inputs)

        pop.evolve()
        gen += 1
        print("GENERATION " + str(gen))
        print(inputs)
        print('----------------')
        total = 0.0
        for s in pop.species:
            print(str(len(s.members)))
            print("************")
        # mean_score /= 1000
        for n, v in xor.networks.items():
            total += v
        total /= len(xor.networks)
        print("MEAN SCORE: " + str(total))
        print("================================")
        if total >= 14.0:
            break
        # time.sleep(1)
        timeout -= 1

    xor = XORFitnessEvaluator()
    outs = {}
    pop.fitness_evaluator = xor
    pop.propagate([0, 0])
    pop.propagate([0, 1])
    pop.propagate([1, 0])
    pop.propagate([1, 1])
    for i in pop.networks:
        outs[i] = i.outputs
        xor.calculate(i, outs, [1, 0, 0, 0, 1, 1, 0, 1])
    avg_0 = 0.0
    avg_1 = 0.0
    avg_2 = 0.0
    avg_3 = 0.0
    nets = sorted(pop.networks, key=lambda x: x.fitness)

    for i in nets:
        avg_0 += i.outputs[0]
        avg_1 += i.outputs[1]
        avg_2 += i.outputs[2]
        avg_3 += i.outputs[3]
    avg_0 /= len(pop.networks)
    avg_1 /= len(pop.networks)
    avg_2 /= len(pop.networks)
    avg_3 /= len(pop.networks)
    print([avg_0, avg_1, avg_2, avg_3])


if __name__ == '__main__':
    main()
