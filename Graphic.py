# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

# Método auxiliar que una vez ejecutado el algoritmo genético, representa
# las gráficas de mejor fitness y media
def fitness_average(bestFitness, average):
    plt.figure()
    plt.plot(bestFitness)
    plt.hold(True)
    plt.plot(average)
    plt.legend(('Mejor Fitness', 'Media'), loc='lower right')
    plt.xlabel('Generacion', fontsize=15)
    plt.ylabel('Fitness', fontsize=15)
    plt.show()
