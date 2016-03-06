# -*- coding: utf-8 -*-
import Cell
import numpy as np
from copy import deepcopy
# Método que devuelve un tablero con la configuración de celdas inicial
def getBoard():
    board = []
    aa = Cell.IntersectionCell(1)
    ab = Cell.IntersectionCell(1)
    ba = Cell.IntersectionCell(1)
    bb = Cell.IntersectionCell(1)

    board.append([Cell.InputCell(1), Cell.NormalCell(1), Cell.NormalCell(1), Cell.SemaphoreCell(1), aa,
               Cell.PostinterCell(1), Cell.NormalCell(1), Cell.NormalCell(1), Cell.SemaphoreCell(1), ab,
               Cell.PostinterCell(1), Cell.NormalCell(1), Cell.NormalCell(1), Cell.OutputCell(1)])

    board.append([Cell.InputCell(1), Cell.NormalCell(1), Cell.NormalCell(1), Cell.SemaphoreCell(1), ba,
               Cell.PostinterCell(1), Cell.NormalCell(1), Cell.NormalCell(1), Cell.SemaphoreCell(1), bb,
               Cell.PostinterCell(1), Cell.NormalCell(1), Cell.NormalCell(1), Cell.OutputCell(1)])

    board.append([Cell.InputCell(2), Cell.NormalCell(2), Cell.NormalCell(2), Cell.SemaphoreCell(2), aa,
               Cell.PostinterCell(2), Cell.NormalCell(2), Cell.NormalCell(2), Cell.SemaphoreCell(2), ba,
               Cell.PostinterCell(2), Cell.NormalCell(2), Cell.NormalCell(2), Cell.OutputCell(2)])

    board.append([Cell.InputCell(2), Cell.NormalCell(2), Cell.NormalCell(2), Cell.SemaphoreCell(2), ab,
               Cell.PostinterCell(2), Cell.NormalCell(2), Cell.NormalCell(2), Cell.SemaphoreCell(2), bb,
               Cell.PostinterCell(2), Cell.NormalCell(2), Cell.NormalCell(2), Cell.OutputCell(2)])
    return board

# Método que inserta la configuraron de semáforos pasada por parámetro accediendo
# a la celda en cuestión y modificando el atributo asociado.
def semaphoreInsert(board, configuration):
    conf0 = True if(configuration[0] == 0) else False
    board[0][3].setSemaphoreState(conf0)
    board[2][3].setSemaphoreState(not conf0)

    conf1 = True if(configuration[1] == 0) else False
    board[0][8].setSemaphoreState(conf1)
    board[3][3].setSemaphoreState(not conf1)

    conf2 = True if(configuration[2] == 0) else False
    board[1][3].setSemaphoreState(conf2)
    board[2][8].setSemaphoreState(not conf2)

    conf3 = True if(configuration[3] == 0) else False
    board[1][8].setSemaphoreState(conf3)
    board[3][8].setSemaphoreState(not conf3)

def vehiclesInsert(board):
    board[0][0].increaseQueue()
    board[1][0].increaseQueue()
    board[2][0].increaseQueue()
    board[3][0].increaseQueue()

def getVehiclesExit(board):
    cont = 0
    for i in range(4): cont += board[i][13].getCont()
    return cont


def getFitness(pop):
    board = getBoard()
    iterations = pop.shape[1]*10
    inputVehicles = 0
    contPop = 0
    for i in range(iterations):
        if i%10 == 0:
            semaphoreInsert(board, pop[:, contPop])
            contPop += 1
        if i%3==0:
            vehiclesInsert(board)
            inputVehicles += 4
        boardStatus = deepcopy(board) #Estado actual del tablero

        #Ejecución de las celdas
        for i in range(14):
            type = board[0][i].getId()
            if(type == 1):
                board[0][i].run(boardStatus[0][i+1])
                board[1][i].run(boardStatus[1][i+1])
                board[2][i].run(boardStatus[2][i+1])
                board[3][i].run(boardStatus[3][i+1])
            elif(type == 2):
                board[0][i].run(boardStatus[0][i-1])
                board[1][i].run(boardStatus[1][i-1])
                board[2][i].run(boardStatus[2][i-1])
                board[3][i].run(boardStatus[3][i-1])
            elif(type == 3 or type == 5 or type == 6):
                board[0][i].run(boardStatus[0][i-1], boardStatus[0][i+1])
                board[1][i].run(boardStatus[1][i-1], boardStatus[1][i+1])
                board[2][i].run(boardStatus[2][i-1], boardStatus[2][i+1])
                board[3][i].run(boardStatus[3][i-1], boardStatus[3][i+1])
            else: continue #intersección

        #Intersecciones
        board[0][4].run(boardStatus[0][3], boardStatus[0][5], boardStatus[2][3], boardStatus[2][5])
        board[0][9].run(boardStatus[0][8], boardStatus[0][10], boardStatus[3][3], boardStatus[3][5])
        board[1][4].run(boardStatus[1][3], boardStatus[1][5], boardStatus[2][8], boardStatus[2][10])
        board[1][9].run(boardStatus[1][8], boardStatus[1][10], boardStatus[3][8], boardStatus[3][10])
    bandwidth = float(getVehiclesExit(board))/float(inputVehicles)
    return bandwidth

def showBoard(board):
    def extractValue(semaphoreCell):
        if(semaphoreCell.getSemaphoreState() == True and semaphoreCell.getIsEmpty() == True):
            return 2
        elif(semaphoreCell.getSemaphoreState() == True and semaphoreCell.getIsEmpty() == False):
            return 3
        elif(semaphoreCell.getSemaphoreState() == False and semaphoreCell.getIsEmpty() == True):
            return 4
        else:
            return 5

    aux = np.full((14, 14), -1)
    for i in range(14):
        if (i == 3 or i == 8):
            aux[4, i] = extractValue(board[0][i])
            aux[9, i] = extractValue(board[1][i])
            aux[i, 4] = extractValue(board[2][i])
            aux[i, 9] = extractValue(board[3][i])
        else:
            aux[4, i] = 0 if(board[0][i].getIsEmpty() == True) else 1
            aux[9, i] = 0 if(board[1][i].getIsEmpty() == True) else 1
            aux[i, 4] = 0 if(board[2][i].getIsEmpty() == True) else 1
            aux[i, 9] = 0 if(board[3][i].getIsEmpty() == True) else 1

    result = ""
    for x in range(14):
        for y in range(14):
            if(aux[x,y] == -1):
                result += "   "
            else:
                if(aux[x, y] == 0): result += " . "
                elif(aux[x, y] == 1): result += " x "
                elif(aux[x, y] == 2): result += " V "
                elif(aux[x, y] == 3): result += " V'"
                elif(aux[x, y] == 4): result += " R "
                else: result += " R'"
            if(y == 13): result += "\n"
    print result