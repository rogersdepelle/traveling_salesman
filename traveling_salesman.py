import random, math
import matplotlib.pyplot as plt


class City(object):

    """ToDo"""

    x = 0
    y = 0
    max_x = 200
    max_y = 200

    def __init__(self, x=None, y=None):
        super(City, self).__init__()
        if x:
            self.x = x
        else:
            self.x = random.randint(0, self.max_x)
        if y:
            self.y = y
        else:
            self.y = random.randint(0, self.max_y)
    
    def distance(self, city):
        return math.sqrt((math.fabs(self.x - city.x)) ** 2 + (math.fabs(self.y - city.y)) ** 2)

    def __str__(self):
        return str(self.x) + ", " + str(self.y)


class Tour(object):
    """Class that can encode our routes"""

    tour = []
    fitness = 0;
    distance = 0;

    def __init__(self, tour=None):
        super(Tour, self).__init__()
        if tour:
            self.tour = list(tour)
        else:
            self.tour = list([None] * len(DESTINATION_CITIES))

    def set_city(self, tour_position, city):
        self.tour[tour_position] = city
        self.fitness = 0
        self.distance = 0

    def get_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / self.get_distance()
        return self.fitness

    def get_distance(self):
        if self.distance == 0:
            tour_distance = 0

            for city_index in xrange(0,len(self.tour)):
                from_city = self.tour[city_index]
                if(city_index + 1 < len(self.tour)):
                    destination_city = self.tour[city_index+1];
                else:
                    destination_city = self.tour[0];
                self.distance += from_city.distance(destination_city);

        return self.distance

    def plot_map(self, position, g, title):

        x_points = []
        y_points = []
        for c in self.tour:
            x_points.append(c.x)
            y_points.append(c.y)

        plt.subplot(position)
        plt.cla()
        plt.axis([0, c.max_x, 0, c.max_y])
        g.set_title(title)
        plt.fill(x_points, y_points, fill=False)
        plt.plot(x_points, y_points, 'ro')
        plt.grid(True)

    def __str__(self):
        return str([str(x) for x in self.tour])


class Population(object):
    """Manages a population of candidate tours"""

    tours = []

    def __init__(self, population_size=10, initialise=True):
        super(Population, self).__init__()
        if initialise:
            for x in xrange(0,population_size):
                new_tour = Tour(DESTINATION_CITIES)
                random.shuffle(new_tour.tour)
                self.tours.append(new_tour)
        else:
            self.tours = [Tour()] * population_size

    def get_fittest(self):
        fittest = self.tours[0]
        for i in xrange(1,len(self.tours)):
            if fittest.get_fitness() <= self.tours[i].get_fitness():
                fittest = self.tours[i]
        return fittest

    def __str__(self):
        return str([str(x) for x in self.tours])


class GeneticAlgorithm(object):
    """Manages algorithms for evolving population"""

    mutation_rate = 0.015;
    tournament_size = 5;
    elitism = True;

    def __init__(self):
        super(GeneticAlgorithm, self).__init__()

        figure = plt.figure()
        top = figure.add_subplot(211)
        botton = figure.add_subplot(212)

        pop = Population(50, True);
        fittest = pop.get_fittest()
        fittest.plot_map(211, top, "Initial Tour")
        print "Initial distance: " + str(fittest.get_distance())

        pop = self.evolve_population(pop);

        for x in xrange(0,100):
            pop = self.evolve_population(pop);
            pop.get_fittest().plot_map(212, botton, "Currently Tour")
            plt.pause(0.001)

        print "Final distance: " + str(pop.get_fittest().get_distance())
        fittest = pop.get_fittest()
        print "\nTour:" + str(fittest)
        fittest.plot_map(212, botton, "Final Tour")
        plt.pause(0.001)
        

    def evolve_population(self, pop):
        new_population = Population(len(pop.tours), False)
        elitism_offset = 0

        if(self.elitism):
            new_population.tours[0] = pop.get_fittest()
            elitism_offset = 1

        for x in xrange(elitism_offset, len(new_population.tours)):
            parent1 = self.tournament_selection(pop)
            parent2 = self.tournament_selection(pop)
            new_population.tours[x] = self.crossover(parent1, parent2)
       
        for x in xrange(elitism_offset, len(new_population.tours)):
            self.mutate(new_population.tours[x].tour)

        return new_population

    def crossover(self, parent1, parent2):
        child = Tour()

        start = random.randint(0, len(parent1.tour) - 1)
        end = random.randint(0, len(parent1.tour) - 1)

        for i in xrange(0, len(child.tour)):
            if (start < end and i > start and i < end):
                child.set_city(i, parent1.tour[i])
            elif start > end:
                if not(i < start and i > end):
                    child.set_city(i, parent1.tour[i])

        for i in xrange(0, len(parent2.tour)):
            if parent2.tour[i] not in child.tour:
                for y in xrange(0, len(child.tour)):
                    if child.tour[y] == None:
                        child.set_city(y, parent2.tour[i])
                        break

        return child

    def mutate(self, tour):
        for tour_pos1 in xrange(0,len(tour)):
            if random.random() < self.mutation_rate:
                tour_pos2 = random.randint(0, len(tour) - 1)

                city1 = tour[tour_pos1]
                city2 = tour[tour_pos2]

                tour[tour_pos1] = city2
                tour[tour_pos2] = city1

    def tournament_selection(self, pop):
        tournament = Population(self.tournament_size, False)

        for i in xrange(0,self.tournament_size):
            tournament.tours[i] = pop.tours[random.randint(0, len(pop.tours) - 1)]

        return tournament.get_fittest()

class SimulatedAnnealing(object):
    """Simulated Annealing Algorithm"""

    def __init__(self):
        super(SimulatedAnnealing, self).__init__()

        temp = 10000;
        cooling_rate = 0.003;
        current_solution = Tour(DESTINATION_CITIES)
        random.shuffle(current_solution.tour)
        best = Tour(current_solution.tour)
        print "Initial distance: " + str(current_solution.get_distance())

        figure = plt.figure()
        top = figure.add_subplot(211)
        botton = figure.add_subplot(212)

        best.plot_map(211, top, "Initial Tour")

        while temp > 1:
            new_solution = Tour(current_solution.tour)

            pos1 = random.randint(0, len(current_solution.tour) - 1)
            pos2 = random.randint(0, len(current_solution.tour) - 1)

            city_swap1 = new_solution.tour[pos1]
            city_swap2 = new_solution.tour[pos2]

            new_solution.set_city(pos2, city_swap1)
            new_solution.set_city(pos1, city_swap2)

            current_energy = current_solution.get_distance()
            neighbour_energy = new_solution.get_distance()

            if self.acceptance_probability(current_energy, neighbour_energy, temp) > random.random():
                current_solution = Tour(new_solution.tour)

            if current_solution.get_distance() < best.get_distance():
                best = Tour(current_solution.tour)
                new_solution.plot_map(212, botton, "Currently Tour")
                plt.pause(0.001)

            temp *= 1 - cooling_rate

        print "Final distance: " + str(best.get_distance())
        print "\nTour:" + str(best)
        best.plot_map(212, botton, "Final Tour")
        plt.pause(0.001)

    def acceptance_probability(self, energy, new_energy, temperature):
        if (new_energy < energy):
            return 1.0;
        return math.exp((energy - new_energy) / temperature)


DESTINATION_CITIES = []
AMOUNT_OF_CITIES = 30
for x in xrange(0,AMOUNT_OF_CITIES):
    DESTINATION_CITIES.append(City())