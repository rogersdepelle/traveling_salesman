import os
import time

from traveling_salesman import GeneticAlgorithm, SimulatedAnnealing

os.system('clear')
while True:
    print '------------------------------------------------'
    print '               Traveling Salesman'
    print '------------------------------------------------\n'
    print '1. Genetic Algorithm'
    print '2. Simulated Annealing'
    print '\n0. Exit\n'

    while True:
        try:
            option = int(raw_input("Choose an option: "))
            if option < 0 or option > 2:
                print "Invalid option"
            else:
                break
        except:
            print "Invalid option"

    os.system('clear')

    if option == 1:
        print '------------------------------------------------'
        print '     Traveling Salesman - Genetic Algorithm'
        print '------------------------------------------------\n'
        print '\nTraveling Salesman\n'
        start = time.time()
        problem = GeneticAlgorithm()
        print "Time: " + str(time.time() - start) + "\n\n"
    elif option == 2:
        print '--------------------------------------------------'
        print '     Traveling Salesman - Simulated Annealing'
        print '--------------------------------------------------\n'
        start = time.time()
        problem = SimulatedAnnealing()
        print "Time: " + str(time.time() - start) + "\n\n"
    else:
        break