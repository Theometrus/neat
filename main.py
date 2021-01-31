import pprint
import random

from classes.Helpers.XORFitnessEvaluator import XORFitnessEvaluator
from classes.Puppeteers.Population import Population


def main():
    """
    Sample application of NEAT to solve the XOR problem.
    """

    xor = XORFitnessEvaluator()
    pop = Population(xor)

    gen = 0
    timeout = 500
    xor_inputs = [[1, 1], [0, 0], [1, 0], [0, 1]]

    # =========================== TRAINING SECTION =========================== #
    print("TRAINING COMMENCED")
    print()
    while timeout > 0:
        xor.networks = {}
        outs = {}
        random.shuffle(xor_inputs)
        inputs = [item for sublist in xor_inputs for item in sublist]
        ctr = 0

        # Feed all four combinations of inputs to networks
        for i in range(4):
            pop.propagate([inputs[ctr], inputs[ctr + 1]])
            ctr += 2

        for i in pop.networks:
            outs[i] = i.outputs

            xor.calculate(i, outs, inputs)  # Get the fitness of each network

        pop.evolve()
        gen += 1

        print("GENERATION " + str(gen))
        print()
        print("SPECIES SIZES:")
        print("POPULATION SIZE: {}".format(len(pop.networks)))
        total = 0.0
        sizes = []

        for s in pop.species:
            sizes.append(len(s.members))

        print(sizes)
        print()

        for n, v in xor.networks.items():
            total += v
        total /= len(xor.networks)

        print("MEAN SCORE THIS GENERATION: " + str(round(total, 2)))
        print("GENERATION " + str(gen) + " END")
        print("=======================================================")

        if total >= 14.0:  # Arbitrary threshold which has been deemed sufficiently fit
            break
        timeout -= 1

    # =========================== RESULTS SECTION =========================== #
    outs = {}

    pop.propagate([1, 1])
    pop.propagate([1, 0])
    pop.propagate([0, 1])
    pop.propagate([0, 0])

    for i in pop.networks:
        outs[i] = i.outputs
        xor.calculate(i, outs, [1, 1, 1, 0, 0, 1, 0, 0])

    avg_0 = 0.0
    avg_1 = 0.0
    avg_2 = 0.0
    avg_3 = 0.0

    nets = sorted(pop.networks, key=lambda x: x.fitness)

    avg_nodes = 0
    avg_conns = 0

    for i in nets:
        avg_nodes += len(i.genome.nodes)
        avg_conns += len(i.genome.connections)
        avg_0 += i.outputs[0]
        avg_1 += i.outputs[1]
        avg_2 += i.outputs[2]
        avg_3 += i.outputs[3]

    avg_0 /= len(pop.networks)
    avg_1 /= len(pop.networks)
    avg_2 /= len(pop.networks)
    avg_3 /= len(pop.networks)
    avg_nodes /= len(pop.networks)
    avg_conns /= len(pop.networks)

    print("XOR TEST RESULTS:")
    print("1^1 : " + str(1 if avg_0 > 0.5 else 0))
    print("1^0 : " + str(1 if avg_1 > 0.5 else 0))
    print("0^1 : " + str(1 if avg_2 > 0.5 else 0))
    print("0^0 : " + str(1 if avg_3 > 0.5 else 0))

    print()

    print("EXACT VALUES:")
    answers = {
        '1^1': avg_0,
        '1^0': avg_1,
        '0^1': avg_2,
        '0^0': avg_3
    }

    pprint.pprint(answers)
    print()
    print("AVERAGE NODES PER NETWORK: {}, AVERAGE CONNECTIONS PER NETWORK: {}".format(round(avg_nodes, 2),
                                                                                      round(avg_conns, 2)))
    print("=======================================================")


if __name__ == '__main__':
    main()
