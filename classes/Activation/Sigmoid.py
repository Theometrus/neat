import math

from classes.Activation.ActivationFunction import ActivationFunction


class Sigmoid(ActivationFunction):
    def compute(self, z):
        if z > 10:
            return 1.0 - 1e10
        elif z < -1e-10:
            return 1e-10
        return 1.0 / (1 + math.exp(-z))
