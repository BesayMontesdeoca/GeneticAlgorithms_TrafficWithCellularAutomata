# -*- coding: utf-8 -*-
import FitnessSimulator
import numpy as np
import random

# Método que inicializa la población con un número de individuos y un ancho de cromosoma
# especificado por parámetro
def ini_pob(size, width):
    pop = []
    for h in range(size):
        ind = np.random.rand(*(4,width))
        for i in range(ind.shape[0]):
            for j in range(ind.shape[1]):
                ind[i,j] = round(ind[i,j])
        pop.append(ind)
    return pop

# Método que calcula el fitness de toda la población y devuelve el resultado en un array
def fitness(pop):
    fitPop = []
    for i in range(len(pop)):
        fitPop.append(FitnessSimulator.getFitness(pop[i]))
    return fitPop

# Método auxiliar que devuelve un numero aleatorio distinto del pasado por parámetro
def randomPair(limit1, limit2, numdis=-1):
    num1 = numdis
    while(num1 == numdis):
        num1 = random.randint(limit1, limit2)
    return num1

# Método que implementa la selección por torneo
def torneoSelection(fitPop, pop, percentage):
    selPop = []
    selPopFitness = []
    iterations = percentage*len(pop)/100
    for i in range(iterations):
        ind1 = randomPair(0, len(fitPop)-1)
        ind2 = randomPair(0, len(fitPop)-1, ind1)
        if fitPop[ind1] >= fitPop[ind2]:
            selPop.append(pop[ind1])
            selPopFitness.append(fitPop[ind1])
        else:
            selPop.append(pop[ind2])
            selPopFitness.append(fitPop[ind2])
    return selPop, selPopFitness

# Método que implementa la selección por truncamiento
def truncateSelection(fitPop, pop, percentage):
    # Método auxiliar que devuelve el índice de elemento mayor
    def getMax(fitPop):
        fit = max(fitPop)
        for i in range(len(fitPop)):
            if(fitPop[i] == fit): return i

    selPop = []
    iterations = percentage*len(pop)/100
    for i in range(iterations):
        index = getMax(fitPop)
        selPop.append(pop[index])
        fitPop[index] = 0
    return selPop

# Método que implementa el cruce uniforme y que genera la nueva generación de
# tamaño especificado por parámetro
def uniformCrossover(size, selPop,  mutationProbability):
    newPop = []
    newPop.append(selPop[0])
    newPop.append(selPop[1])

    while(len(newPop) < size):
        newSon = np.zeros((4, selPop[0].shape[1]))
        ind1 = randomPair(0, len(selPop)-1)
        ind2 = randomPair(0, len(selPop)-1, ind1)
        for i in range(selPop[0].shape[1]):
            pro = np.random.rand()
            if pro > 0.5:
                newSon[:, i] = selPop[ind1][:, i]
            else:
                newSon[:, i] = selPop[ind2][:, i]
        bitStringMutation(newPop, mutationProbability)
        newPop.append(newSon)
    return newPop

# Método que implementa el operador de mutación bit String Mutation
def bitStringMutation(son, probability):
    pro = probability/100
    mut = np.random.rand()
    if mut <= pro:
        x = random.randint(0, son.shape[0]-1)
        y = random.randint(0, son.shape[1]-1)
        son[x, y] = 1 if(son[x, y] == 0) else 0

