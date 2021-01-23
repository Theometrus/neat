import math
from decimal import Decimal, getcontext


class XORFitnessEvaluator:
    def __init__(self):
        self.networks = {}

    def calculate(self, network, outs):
        # 11 10 01 00

        ans = outs[network]  # Length 4

        fitness = 1 / (abs(1 - ans[0]) + abs(0 - ans[1]) + abs(1 - ans[2]) + abs(0 - ans[3]))

        # print(ans)
        # print(fitness)
        network.fitness = fitness
        self.networks[network] = network.fitness

    def evaluate(self, network):
        return self.networks[network]
