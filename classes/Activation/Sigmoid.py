import math

from classes.Activation.ActivationFunction import ActivationFunction


class Sigmoid(ActivationFunction):
    def compute(self, z):
        return 1.0 / (1 + math.exp(-z))
