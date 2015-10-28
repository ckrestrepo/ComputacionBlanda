import numpy as np
import matplotlib.pyplot as plt
from mlxtend.evaluate import plot_decision_regions

import csv

from perceptron import Perceptron

df = list(csv.reader(open('patrones.data', 'r')))

print ('df', df)

#y = np.array([1 if r[2] == '1' else 0 for r in df[0:7]])
y = np.array([1, 1, 1, 0, 0, 0, 1])

print ('y', y)

#X = np.array([[float(r[0]), float(r[1])] for r in df[0:7]])
X = np.array([[0,2],[-2,2],[-2,-2],[0,-2],[2,-2],[2,0],[2,2]])

print('X', X)

ppn = Perceptron(epochs=1000, eta=0.9)

ppn.train(X, y)
print('Weights: %s' % ppn.w_)


plot_decision_regions(X, y, clf=ppn)
plt.title('Perceptron')
plt.xlabel('Pattern 1')
plt.ylabel('Pattern 2')
plt.show()

plt. clf()
plt.plot(range(1, len(ppn.errors_)+1), ppn.errors_, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Missclassifications')
plt.show()

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
