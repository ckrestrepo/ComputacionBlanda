__author__ = 'Camilo'
#!/env/python
# -*- coding: utf-8 -*-

import re, math, random

# =======================================================================
# TourManager
# =======================================================================
TourManager = (
	("Arauca, Arauca", "07°05'05\"N", "70°45'33\"W"),
	("Armenia, Quindio", "04°32'02\"N", "75°40'52\"W"),
	("Barranquilla, Atlantico", "10°57'50\"N", "74°47'47\"W"),
	("Bogota, Cundinamarca", "04°36'35\"N", "74°04'54\"W"),
	("Bucaramanga, Santander", "07°07'31\"N", "73°07'11\"W"),
	("Cali, Valle", "03°26'14\"N", "76°31'21\"W"),
	("Cartgena, Bolivar", "10°23'59\"N", "75°30'52\"W"),
	("Cucuta, Norte de Santander", "07°53'00\"N", "72°30'19\"W"),
	("Florencia, Caqueta", "01°36'52\"N", "75°36'22\"W"),
	("Ibague, Tolima", "04°26'20\"N", "75°13'56\"W"),
	("Leticia, Amazonas", "04°12'55''S", "69°56'26\"W"),
	("Manizales, Caldas", "05°04'08\"N", "75°31'03\"W"),
	("Medellin, Antioquia", "06°15'07\"N", "75°33'49\"W"),
	("Mitu, Vaupes", "01°11'54\"N", "70°10'24\"W"),
	("Mocoa, Putumayo", "01°08'58\"N", "76°38'48\"W"),
	("Monteria, Cordoba", "08°44'53\"N", "75°52'53\"W"),
	("Neiva, Huila", "02°55'38\"N", "75°16'55\"W"),
	("Pasto, Nariño", "01°12'57\"N", "77°16'45\"W"),
	("Pereira, Risaralda", "04°48'48\"N", "75°41'46\"W"),
	("Popayan, Cauca", "02°26'18\"N", "76°36'47\"W"),
	("Puerto Carreño, Vichada", "06°11'21\"N", "67°29'09\"W"),
	("Inirida, Guainia", "03°52'15\"N", "67°55'16\"W"),
	("Quibdo, Choco", "05°41'41\"N", "76°39'40\"W"),
	("Riohacha, La Guajira", "11°32'40\"N", "72°54'26\"W"),
	("San Andres, San Andres y Providencia", "12°35'05\"N", "81°42'02\"W"),
	("San Jose del Guaviare, Guaviare", "02°34'22\"N", "72°38'45\"W"),
	("Santa Marta, Magdalena", "11°14'27\"N", "74°11'57\"W"),
	("Sincelejo, Sucre", "09°18'17\"N", "75°23'52\"W"),
	("Tunja, Boyaca", "05°32'07\"N", "73°22'04\"W"),
	("Valledupar, Cesar", "10°25'00\"N", "73°35'00\"W"),
	("Villavicencio, Meta", "04°08'31\"N", "73°37'36\"W"),
	("Yopal, Casanare", "05°20'16\"N", "72°23'45\"W")
)

# =======================================================================
# Ciudad
# =======================================================================

class City:

	RADIUS_EARTH_KM = 6370.97327862

	def __init__(self, name, coor):
		self.name = name
		self.coor = coor

	def __eq__(self, city):
		if city == None: return False
		return self.name == city.name

	def __str__(self):
		return '%s (%f,%f)' % (self.name, self.coor[0], self.coor[1])

	def __repr__(self):
		return '%s (%f,%f)' % (self.name, self.coor[0], self.coor[1])

	def distance(self, city):
		lat1, lon1 = self.coor
		lat2, lon2 = city.coor

		dlat = math.radians(lat2-lat1)
		dlon = math.radians(lon2-lon1)
		a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
			* math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		d = City.RADIUS_EARTH_KM * c

		return d

# =======================================================================
# Tour
# =======================================================================
class Tour:

	def __init__(self, tour = None):
		self.fitness = 0.0
		self.distance = 0
		if tour == None: tour = [None] * len(TourManager)
		self.tour = tour

	def __str__(self):
		geneString = ''
		for i in range(len(self.tour)):
			geneString += str(self.tour[i]) + "\n"
		return geneString;

	# Gets a city from the tour
	def __getitem__(self, tourPosition):
		return self.tour[tourPosition]

	# Sets a city in a certain position within a tour
	def __setitem__(self, tourPosition, city):
		self.tour[tourPosition] = city
		#If the tours been altered we need to reset the fitness and distance
		self.fitness = 0.0
		self.distance = 0

	# Get number of cities on our tour
	def __len__(self):
		return len(self.tour)

	# Check if the tour contains a city
	def __contains__(self, city):
		return city in self.tour

	# Creates a random individual
	def generateIndividual(self):
		# Loop through all our destination cities and add them to our tour
		for cityIndex in range(len(TourManager)):
			city = TourManager[cityIndex][0]
			coor = [dms2dec(TourManager[cityIndex][1]), dms2dec(TourManager[cityIndex][2])]
			self.tour[cityIndex] = City(city, coor)

		# Randomly reorder the tour
		random.shuffle(self.tour)

	# Gets the tours fitness
	def getFitness(self):
		if self.fitness == 0:
			self.fitness = 1 / self.getDistance()
		return self.fitness

	# Gets the total distance of the tour
	def getDistance(self):

		if self.distance == 0:
			tourDistance = 0

			# Loop through our tour's cities
			for cityIndex in range(len(self.tour)):
				# Get city we're travelling from
				fromCity = self.tour[cityIndex]
				# City we're travelling to
				# Check we're not on our tour's last city, if we are set our
				# tour's final destination city to our starting city
				if cityIndex + 1 < len(self.tour):
					destCity = self.tour[cityIndex+1]
				else:
					destCity = self.tour[0]
				tourDistance += fromCity.distance(destCity)
			self.distance = tourDistance

		return self.distance

# =======================================================================
# Population
# =======================================================================
class Population:

	# Construct a population
	def __init__(self, populationSize, initialise = False):
		self.tours = [None] * populationSize
		# If we need to initialise a population of tours do so
		if initialise:
			# Loop and create individuals
			for i in range(len(self.tours)):
				newTour = Tour()
				newTour.generateIndividual()
				self.tours[i] = newTour

	# Gets a tour from population
	def __getitem__(self, index):
		return self.tours[index]

	# Saves a tour
	def __setitem__(self, index, tour):
		self.tours[index] = tour

	# Gets population size
	def __len__(self):
		return len(self.tours)

	# Gets the best tour in the population
	def getFittest(self):
		fittest = self.tours[0]
		# Loop through individuals to find fittest
		for i in range(len(self.tours)):
			if fittest.getFitness() < self.tours[i].getFitness():
				fittest = self.tours[i]
		return fittest

# =======================================================================
# GA
# =======================================================================
class GA:

	# GA parameters
	mutationRate = 0.015
	tournamentSize = 5
	elitism = True

	# Evolves a population over one generation
	@staticmethod
	def evolvePopulation(pop):
		newPopulation = Population(len(pop))

		# Keep our best individual if elitism is enabled
		elitismOffset = 0
		if GA.elitism:
			newPopulation[0] = pop.getFittest()
			elitismOffset = 1

		# Crossover population
		# Loop over the new population's size and create individuals from
		# Current population
		for i in range(elitismOffset, len(newPopulation)):
			# Select parents
			parent1 = GA.tournamentSelection(pop)
			parent2 = GA.tournamentSelection(pop)
			# Crossover parents
			child = GA.crossover(parent1, parent2);
			# Add child to new population
			newPopulation[i] = child

		# Mutate the new population a bit to add some new genetic material
		for i in range(elitismOffset, len(newPopulation)):
			GA.mutate(newPopulation[i]);

		return newPopulation;

	# Applies crossover to a set of parents and creates offspring
	@staticmethod
	def crossover(parent1, parent2):
		# Create new child tour
		child = Tour()

		# Get start and end sub tour positions for parent1's tour
		spos = random.randint(0, len(parent1)-1)
		epos = random.randint(0, len(parent1)-1)

		# Loop and add the sub tour from parent1 to our child
		for i in range(len(child)):
			# If our start position is less than the end position
			if spos < epos and i > spos and i < epos:
				child[i] = parent1[i]
			# If our start position is larger
			elif spos > epos:
				if not(i < spos and i > epos):
					child[i] = parent1[i]

		# Loop through parent2's city tour
		for i in range(len(parent2)):
			# If child doesn't have the city add it
			if parent2[i] not in child:
				# Loop to find a spare position in the child's tour
				for ii in range(len(child)):
					# Spare position found, add city
					if child[ii] == None:
						child[ii] = parent2[i]
						break
		return child

	# Mutate a tour using swap mutation
	@staticmethod
	def mutate(tour):
		# Loop through tour cities
		for tourPos1 in range(len(tour)):
			# Apply mutation rate
			if random.random() < GA.mutationRate:
				# Get a second random position in the tour
				tourPos2 = random.randint(0, len(tour)-1)

				# Get the cities at target position in tour
				city1 = tour[tourPos1]
				city2 = tour[tourPos2]

				# Swap them around
				tour[tourPos2] = city1
				tour[tourPos1] = city2

	# Selects candidate tour for crossover
	@staticmethod
	def tournamentSelection(pop):
		# Create a tournament population
		tournament = Population(GA.tournamentSize)
		# For each place in the tournament get a random candidate tour and
		# add it
		for i in range(GA.tournamentSize):
			randomId = random.randint(0, len(pop)-1)
			tournament[i] = pop[randomId]
		# Get the fittest tour
		fittest = tournament.getFittest()
		return fittest

# =======================================================================
# Mis
# =======================================================================
def dms2dec(dms_str):
	dms_str = re.sub(r'\s', '', dms_str)
	sign = -1 if re.search(r'[swSW]', dms_str) else 1
	(deg, mnt, sec, junk) = re.split('\D+', dms_str, maxsplit=3)
	return sign * (int(deg) + float(mnt)/60 + float(sec)/3600)

if __name__ == '__main__':
	# Initialize population
	pop = Population(50, True)
	print "Distancia inicial: %f" % pop.getFittest().getDistance()
	# Evolve population for 100 generations
	pop = GA.evolvePopulation(pop)
	for i in range(100):
		pop = GA.evolvePopulation(pop)
		print i, pop.getFittest().getDistance()

	# Print final results
	print "Finished"
	print "Final distance: %f" % pop.getFittest().getDistance()

	print "Solution:"
	print pop.getFittest()