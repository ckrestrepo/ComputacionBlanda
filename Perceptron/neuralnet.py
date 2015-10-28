from neuralnet import *
from sklearn import datasets

from NeuralNetwork import NeuralNetwork

digits = datasets.load_digits()

X = digits.data


y = digits.target

print y[0]

X -= X.min() # normalizar los datos
X /= X.max() # para valor 0 -1

nn = NeuralNetwork([64, 100, 10], 'tanh')