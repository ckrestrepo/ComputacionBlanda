import numpy as np

A = '''
.XXXX.
X....X
X....X
XXXXXX
X....X
X....X
X....X
'''

B = '''
XXXXX.
X....X
X....X
XXXXX.
X....X
X....X
XXXXX.
'''

C = '''
.XXXXX
X.....
X.....
X.....
X.....
X.....
.XXXXX
'''

D = '''
XXXX..
X...X.
X....X
X....X
X....X
X...X.
XXXX..
'''

def to_pattern(letter):
	from numpy import array
	return array([+1 if c == 'X' else -1 for c in letter.replace('\n','')])

def display(pattern):
	from pylab import imshow, cm, show
	imshow(pattern.reshape((7,6)), cmap=cm.binary, interpolation='nearest')
	show()

def train(patterns):
	from numpy import zeros, outer, diag_indices
	patterns.shape
	r,c = patterns.shape
	W = zeros((c,c))
	for p in patterns:
		W += outer(p,p)
	W[diag_indices(c)] = 0
	return W/r

def recall(W, patterns, steps=5):
	from numpy import vectorize, dot
	sgn = vectorize(lambda x: -1 if x<0 else +1)
	for _ in xrange(steps):
		patterns = sgn(dot(patterns,W))
	return patterns

def hopfield_energy(W, patterns):
	from numpy import array, dot
	return array([-0.5*dot(dot(p.T,W),p) for p in patterns])

test1 = '''
.XX..X
X.XX..
.X...X
XXXX..
X..X..
X.X...
X..X.X
'''

patterns = np.array([to_pattern(A), to_pattern(B), to_pattern(C), to_pattern(D)])

hf = train(patterns)

test = to_pattern(test1)
for _ in range(5):
	display(test)
	test = recall(hf, test, 1)
