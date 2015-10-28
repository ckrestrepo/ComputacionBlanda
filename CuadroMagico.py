__author__ = 'Camilo'
import scoop.futures   as futures
import deap.algorithms as algorithms
import deap.base    as base
import deap.creator as creator
import deap.tools   as tools
import numpy        as np
import random

N = 4; N2 = N ** 2

creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register('indices', random.sample, range(1,N2+1), N2)

# Structure initializers
toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalMS(individual):
	a = np.array(individual).reshape((N,N))
	tot = 0; k = N * (N2 + 1) / 2
	for i in range(N):
		tot += abs(k - sum(a[i,:]))	# rows
		tot += abs(k - sum(a[:,i]))	# columns
	tot += abs(k - sum(a.diagonal()))
	tot += abs(k - sum(np.rot90(a).diagonal()))
	return tot,

def cxPartialyMatched(ind1, ind2):
	size = min(len(ind1), len(ind2))
	p1, p2 = [0]*(size+1), [0]*(size+1)

	# Initialize the position of each indices in the individuals
	for i in xrange(size):
		p1[ind1[i]] = i
		p2[ind2[i]] = i
	# Choose crossover points
	cxpoint1 = random.randint(0, size)
	cxpoint2 = random.randint(0, size - 1)
	if cxpoint2 >= cxpoint1:
		cxpoint2 += 1
	else: # Swap the two cx points
		cxpoint1, cxpoint2 = cxpoint2, cxpoint1

	# Apply crossover between cx points
	for i in xrange(cxpoint1, cxpoint2):
		# Keep track of the selected values
		temp1 = ind1[i]
		temp2 = ind2[i]
		# Swap the matched value
		ind1[i], ind1[p1[temp2]] = temp2, temp1
		ind2[i], ind2[p2[temp1]] = temp1, temp2
		# Position bookkeeping
		p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
		p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

	return ind1, ind2

toolbox.register("mate", cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evalMS)
toolbox.register("map", futures.map)

def main():
	random.seed(169)

	pop = toolbox.population(n=300)

	hof = tools.HallOfFame(1)

	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", np.mean)
	stats.register("std", np.std)
	stats.register("min", np.min)
	stats.register("max", np.max)

	algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 100, stats=stats, halloffame=hof)
	return pop, stats, hof

if __name__ == '__main__':
	main()[2][0]
