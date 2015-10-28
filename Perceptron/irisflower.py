import numpy as np
import matplotlib.pyplot as plt
from mlxtend.evaluate import plot_decision_regions

import csv
import urllib2

from perceptron import Perceptron

df = list(csv.reader(open('iris.data', 'r')))

# setosa and versicolor
y = np.array([-1 if r[4] == 'Iris-setosa' else 1 for r in df[0:100]])

print('y', y)

# sepal length and petal length
X = np.array([[float(r[0]), float(r[2])] for r in df[0:100]])

print('X', X)

ppn = Perceptron(epochs=10, eta=0.01)

#print('ppn', ppn)

ppn.train(X, y)
print('Weights: %s' % ppn.w_)

plot_decision_regions(X, y, clf=ppn)
plt.title('Perceptron')
plt.xlabel('sepal length [cm]')
plt.ylabel('petal length [cm]')
plt.show()

plt. clf()
plt.plot(range(1, len(ppn.errors_)+1), ppn.errors_, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Missclassifications')
plt.show()


# versicolor and virginica
y2 = np.array([-1 if r[4] == 'Iris-virginica' else 1 for r in df[50:150]])

# sepal width and petal width
X2 = np.array([[float(r[1]), float(r[3])] for r in df[50:150]])

ppn = Perceptron(epochs=25, eta=0.01)
ppn.train(X2, y2)

plt.clf()
plot_decision_regions(X2, y2, clf=ppn)
plt.show()

plt.clf()
plt.plot(range(1, len(ppn.errors_)+1), ppn.errors_, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Missclassifications')
plt.show()


########### Adaline ###########
from adaline import AdalineGD

ada = AdalineGD(epochs=10, eta=0.01).train(X, y)
plt.clf()
plt.plot(range(1, len(ada.cost_)+1), np.log10(ada.cost_), marker='o')
plt.xlabel('Iterations')
plt.ylabel('log(Sum-squared-error)')
plt.title('Adaline - Learning rate 0.01')
plt.show()

ada = AdalineGD(epochs=10, eta=0.001).train(X, y)
plt.clf()
plt.plot(range(1, len(ada.cost_)+1), ada.cost_, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Sum-squared-error')
plt.title('Adaline - Learning rate 0.0001')
plt.show()

# standardize features
X_std = np.copy(X)
X_std[:,0] = (X[:,0] - X[:,0].mean()) / X[:,0].std()
X_std[:,1] = (X[:,1] - X[:,1].mean()) / X[:,1].std()

ada = AdalineGD(epochs=15, eta=0.01)

ada.train(X_std, y)
plt.clf()
plot_decision_regions(X_std, y, clf=ada)
plt.title('Adaline - Gradient Descent')
plt.xlabel('sepal length [standardized]')
plt.ylabel('petal length [standardized]')
plt.show()

plt.plot(range(1, len( ada.cost_)+1), ada.cost_, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Sum-squared-error')
plt.show()
