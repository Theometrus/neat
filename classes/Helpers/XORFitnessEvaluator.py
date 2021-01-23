class XORFitnessEvaluator:
    def __init__(self):
        self.networks = {}

    def calculate(self, inputs, network):
        correct_output = inputs[0] ^ inputs[1]
        diff = abs(correct_output - network.outputs[0])
        network.fitness = 1 / diff
        self.networks[network] = network.fitness

    def evaluate(self, network):
        return self.networks[network]
