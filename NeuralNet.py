import random
import math

class Perceptron:
    def __init__(self, n):
        self.weights = [random.uniform(-1, 1) for _ in range(n)]
        self.c = 0.1
    
    def feedForward(self, inputs):
        # Sum all inputs * relevant weight, then divide for average
        # This would have been much more customized to slime volleyball
        # and had multiple implementations had I used a more complex
        # neural network.
        sum = 0
        for i in range(len(inputs)):
            sum += inputs[i] * self.weights[i]
        sum /= len(inputs)
        #sum *= 0.5
        return self.activate(sum)
        
    def activate(self, value):
        #print(str(value) + ":" + str(math.tanh(value)))
        return (1 if math.tanh(value) > 0 else -1)    # The idea to use tanh for the activation function came from Github user hardmaru
    
    
class Bot:
    def __init__(self):
        self.pForward = Perceptron(8)
        self.pBackward = Perceptron(8)
        self.pJump = Perceptron(8)
        
    def setPerceptrons(self, pF, pB, pJ):
        self.pForward, self.pBackward, self.pJump = pF, pB, pJ