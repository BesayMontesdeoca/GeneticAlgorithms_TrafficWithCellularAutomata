# -*- coding: utf-8 -*-
# Clase necesaria para la simulación y de la que heredaran las distintas clases que implementan
# el comportamiento de las celdas. Cada celda tiene el método run que dependiendo de los parámetros
# cambiará su estado a libre u ocupado.
class Cell:
    empty = True
    direction = -1
    id = 0

    def __init__(self, direction, isEmpty=True):
        self.direction = direction
        self.empty = isEmpty

    def getIsEmpty(self):
        return self.empty

    def changeCellState(self, state):
        self.empty = state

    def getDirection(self):
        return self.direction

    def setDirection(self, direction):
        self.direction = direction

    def getId(self):
        return self.id

    def setId(self, newId):
        self.id = newId

class InputCell(Cell):
    queue = 0
    id = 1

    def increaseQueue(self):
        self.queue += 1

    def decreaseQueue(self):
        if(self.queue > 0):
            self.queue -= 1

    def getQueueValue(self):
        return self.queue

    def run(self, nextCell):
        if(self.getIsEmpty() == False):
            if(nextCell.getIsEmpty() == True):
                if(self.getQueueValue() > 0):
                    self.decreaseQueue()
                else:
                    self.changeCellState(True)
        else:
            if(self.getQueueValue() > 0):
                self.changeCellState(False)
                self.decreaseQueue()


class OutputCell(Cell):
    cont = 0
    id = 2

    def increaseCont(self):
        self.cont += 1;

    def getCont(self):
        return self.cont

    def run(self, prevCell):
        if(self.getIsEmpty() == False):
            self.increaseCont()
        if(prevCell.getIsEmpty() == True):
            self.changeCellState(True)
        else:
            self.changeCellState(False)

class SemaphoreCell(Cell):
    semaphoreState = True
    id = 3

    def getSemaphoreState(self):
        return self.semaphoreState

    def setSemaphoreState(self, state):
        self.semaphoreState = state

    def run(self, prevCell, interCell):
        if(self.getIsEmpty() == False):
            if(self.getSemaphoreState() == True and interCell.getIsEmpty() == True):
                self.changeCellState(True)
        else:
            if(prevCell.getIsEmpty() == False):
                self.changeCellState(False)

class IntersectionCell(Cell):
    id = 4

    def run(self, sem_1, postInter_1, sem_2, postInter_2):
        dirSem = True if(sem_1.getSemaphoreState() == True) else False
        dirInt = True if(self.getDirection() == 1) else False
        if(self.getIsEmpty() == True):
            if(dirSem):
                if(sem_1.getIsEmpty() == False):
                    self.changeCellState(False)
                    self.setDirection(1)
            else:
                if(sem_2.getIsEmpty() == False):
                    self.changeCellState(False)
                    self.setDirection(2)
        else:
            if(dirInt):
                if(postInter_1.getIsEmpty() == True):
                    self.changeCellState(True)
            else:
                if(postInter_2.getIsEmpty() == True):
                    self.changeCellState(True)


class PostinterCell(Cell):
    id = 5

    def run(self, prevCell, nextCell):
        if(self.getIsEmpty() == True):
            if(prevCell.getDirection() == self.getDirection() and prevCell.getIsEmpty() == False):
                self.changeCellState(False)
        else:
            if(nextCell.getIsEmpty() == True):
                self.changeCellState(True)

class NormalCell(Cell):
    id = 6

    def run(self, prevCell, nextCell):
         if(self.getIsEmpty() == True):
            if(prevCell.getIsEmpty() == False):
                self.changeCellState(False)
         else:
             if(nextCell.getIsEmpty() == True):
                 self.changeCellState(True)