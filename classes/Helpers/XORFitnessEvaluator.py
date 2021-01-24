import math
from decimal import Decimal, getcontext


class XORFitnessEvaluator:
    def __init__(self):
        self.networks = {}

    def calculate(self, network, outs, ins):
        # 11 10 01 00

        ans = outs[network]

        fitness = 0.0
        ctr = 0
        for i in range(int(len(ins) / 2)):
            my_ans = ins[ctr] ^ ins[ctr + 1]
            fitness += abs(my_ans - ans[i])
            ctr += 2

        if fitness != 0.0:
            fitness = min(1 / fitness, 100)

        # print(ans)
        # print(fitness)
        network.fitness = fitness
        self.networks[network] = network.fitness

    def evaluate(self, network):
        return self.networks[network]
