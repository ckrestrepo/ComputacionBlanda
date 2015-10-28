##Entrenar una red neuronal para que reconozca digitos

from sklearn import datasets

import numpy as np

import pylab as pl

from neuralnetwork import NeuralNetwork

##
def to_pattern(digit):
    from numpy import array
    return array([+1 if c=='x' else 0 for c in digit.replace('\n','')])

def display(pattern):
    from pylab import imshow, cm, show
    imshow(pattern.reshape((8,8)), cmap = cm.binary, interpolation='nearest')
    show()

def to_bit(digit):
    v = 1
    while v <= digit/2:
        v*=2
    binary = []

    while v > 0:
        if digit < v:
            binary.append(0)
        else:
            binary.append(1)
            digit -=v
        v /= 2

    while len(binary) < 4:
        binary.insert(0,0)

    return binary


print to_bit(0)
print to_bit(1)
print to_bit(2)
print to_bit(3)
print to_bit(4)
print to_bit(5)
print to_bit(6)
print to_bit(7)
print to_bit(8)
print to_bit(9)
print to_bit(10)
##

digits = datasets.load_digits()

print digits.images.shape

pl.matshow(digits.images[0])

X = digits.data

print ('X', X)

y = np.array([to_bit(x) for x in digits.target])

print ('y', y)

X -= X.min() ## 0 - 1
X /= X.max() ##

nn = NeuralNetwork([64, 100, 100], 'tanh')

nn.train(X, y, epochs= 10)

one = '''
....x...
...xx...
..x.x...
....x...
....x...
....x...
....x...
....x...
'''

one_pattern = to_pattern(one)

#print nn.predict(one_pattern)


