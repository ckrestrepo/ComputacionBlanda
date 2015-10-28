__author__ = 'Camilo'

creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register('indices', random.sample, range(1,N2+1), N2)

# Structure initializers
toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalMS(individual):
       pass

def cxPartialyMatched(ind1, ind2):
       pass

toolbox.register("mate", cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evalMS)

def main():
	random.seed(169)

	pop = toolbox.population(n=300)

	hof = tools.HallOfFame(1)

	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", np.mean)
	stats.register("std", np.std)
	stats.register("min", np.min)
	stats.register("max", np.max)

	algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 50, stats=stats, halloffame=hof)
	return pop, stats, hof

if __name__ == '__main__':
	print main()[2]
