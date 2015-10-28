### Revisar los datos que se estan trabajando.

from sklearn import datasets

digits = datasets.load_digits()

## print digits

print digits.images.shape

import pylab as pl

pl.imshow(digits.images[1], cmap=pl.cm.gray_r)

pl.show()


