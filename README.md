# GeneticAlgorithms_TrafficWithCellularAutomata
Algoritmo genético implementado en Python que calcula la mejor configuración de semáforos para simulación de tráfico basado en autómatas celulares.

![alt tag](https://github.com/BesayMontesdeoca/GeneticAlgorithms_TrafficWithCellularAutomata/blob/master/modelo.PNG)

El objetivo del programa es obtener la secuencia de estados de semáforos óptima, desde el punto de vista del ancho de banda de salida (vehículos por minuto), medido durante durante un cierto número de iteraciones.

Para cada par de semáforos, se optimizará un ciclo de 2 minutos. La duración mínima de un estado es de 10 segundos (una iteración del simulador será equivalente a un segundo). Por ello, la longitud de genes del cromosoma será de 4x12 (4 pares de semáforos, secuencias de 12 estados en cada uno de ellos).
El perfil de demanda será muy exigente: un nuevo vehículo en cada entrada cada 5 segundos/iteraciones.
