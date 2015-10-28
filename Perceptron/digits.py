from sklearn import datasets
import matplotlib.pyplot  as plt

digits = datasets.load_digits()

print digits

plt.figure(1, figsize=(3,3))

plt.imshow(digits.images[5], cmap = plt.cm.gray_r, interpolation = 'nearest')

plt.show()
