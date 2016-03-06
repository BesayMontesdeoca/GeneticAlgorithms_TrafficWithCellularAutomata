# -*- coding: utf-8 -*-
import AG
import Graphic

# Parámetros del algoritmo.
Npob = 200
chromosomeWidth = 12
generations = 50
mutationProbability = 30
selectionPercentage = 30

# Algoritmo principal
pop = AG.ini_pob(Npob, chromosomeWidth)
bestFitness = []
average = []
for i in range(generations):
    print 'Iteracion: {}'.format(i)
    fitPop = AG.fitness(pop)
    maxFitness = max(fitPop)
    averageFit = sum(fitPop)/len(pop)
    bestFitness.append(maxFitness)
    average.append(averageFit)
    print 'Mejor fitness: {}\nMedia: {}'.format(maxFitness, averageFit)
    selPop = AG.truncateSelection(fitPop, pop, selectionPercentage)
    pop = AG.uniformCrossover(Npob, selPop, mutationProbability)
Graphic.fitness_average(bestFitness, average)



