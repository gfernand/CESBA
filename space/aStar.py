import random
import configuration.settings
import bisect
from configuration.BuildingGrid import *
import sys
from heapq import heappush, heappop

class Cell(object):
    def __init__(self, pos):
        self.x, self.y = pos
        self.parent = None
        self.G = 0
    def __lt__(self, other):
        return self.G < other.G
    def __repr__(self):
        return "<x: %s y: %s, G: %s, parent: %s>" % (self.x, self.y, self.G, self.parent)

def calculateCost(model, cell, other):
    ux = cell.x
    uy = cell.y
    nx = other.x
    ny = other.y
    posCell = ux, uy
    posOther = nx, ny
    for room in model.rooms:
        rx, ry = room.pos
        if room.pos == posCell:
        #Cost as steps
            if (rx == nx):
                costMovemenToNewRoom = room.dy/2 #* (1/configuration.settings.speed) * (1/configuration.settings.time_by_step)# m * seg/m * step/seg
            if (ry == ny):
                costMovemenToNewRoom = room.dx/2 #* (1/configuration.settings.speed) * (1/configuration.settings.time_by_step)
        if room.pos == posOther:
            if (rx == ux):
                costMovementInNewRoom = room.dy/2 #* (1/configuration.settings.speed) * (1/configuration.settings.time_by_step)
            if (ry == uy):
                costMovementInNewRoom = room.dx/2 #* (1/configuration.settings.speed) * (1/configuration.settings.time_by_step)
    cost = costMovementInNewRoom + costMovemenToNewRoom
    #print("Distancia entre:", cell.x, ",", cell.y, "y", other.x, ",", other.y, "=", cost)
    return cost

def getPath(model, start, finish):
    finish = Cell(finish)
    start = Cell(start)
    not_visited = []
    visited = []
    not_visited = [start]
    finishCell = None
    #notFinished = True
    while len(not_visited) > 0: # if not_visited is empty
        current = not_visited.pop(0)
        if not is_member(current, visited):
            visited = visited + [current]
        if current.x == finish.x and current.y == finish.y:
            finishCell = current
            break
        cells = get_conected_cells(model, current) #create adject cells with conection
        for connected in cells:
            if not is_member(connected, visited) and not is_member(connected, not_visited):
                connected.parent = current
                connected.G = current.G + 1
                bisect.insort_left(not_visited, connected) 

    cellWay = [finishCell]
    cell = finishCell
    totalCost = cell.G
    while not (cellWay[len(cellWay)-1] is start):
        cell = cell.parent;
        cellWay = cellWay + [cell]
    cellWay.pop()
    way = []
    for cell in cellWay:
        pos = (cell.x, cell.y)
        way = way + [pos]
    way.reverse()
    return way, totalCost

def get_conected_cells(model, cell):
    x,y = cell.x, cell.y
    pos = (x,y)
    possible_steps = model.grid.get_neighborhood(
            pos,
            moore=False,
            include_center=False)
    for is_wall in model.Walls:
            w = (is_wall.x, is_wall.y)
            for cell in possible_steps:
                if w == cell:
                    #print("Muro:", w, "PosibleStep:", cell)
                    possible_steps.remove(cell)
    cells = []
    for cellp in possible_steps:
        cell = Cell(cellp)
        cells = cells + [cell]
    return cells

def is_member(cell, cells):
    for c in cells:
        if c.x == cell.x and c.y == cell.y:
            return True
    return False

def getNearOut(model, start):
    wayOut1, costOut1 = getPath(model, start, configuration.settings.Out1)
    wayOut2, costOut2 = getPath(model, start, configuration.settings.OutBuildingC)
    print("Distancia Salida 1:", costOut1, "Distancia EdC=", costOut2)
    if costOut1 > costOut2:
        print("Elegido camino 2")
        #print("Camino a Out2:", wayOut2)
        return wayOut2, configuration.settings.OutBuildingC
    else:
        print("Elegido camino 1")
        #print("Camino a Out1:", wayOut1)
        return wayOut1, configuration.settings.Out1

def getSafestOut(model, start):
    wayFire1, costFireOut1 = getPath(model, model.firePos, configuration.settings.Out1)
    wayFire2, costFireOut2 = getPath(model, model.firePos, configuration.settings.OutBuildingC)
    print("Distancia Salida 1 al fuego:", costFireOut1, "Distancia EdC al fuego=", costFireOut2)
    if start == (14,2):
        return start, configuration.settings.Out1
    elif costFireOut1 > costFireOut2:
        wayOut1, costOut1 = getPath(model, start, configuration.settings.Out1)
        for room in wayOut1:
            if room == model.firePos:
                wayOut2, costOut2 = getPath(model, start, configuration.settings.OutBuildingC)
                print("Elegido camino 2 porque el 1 pasaba por el fuego", model.roomFire)
                return wayOut2, configuration.settings.OutBuildingC
        print("Elegido camino 1")
        return wayOut1, configuration.settings.Out1
    else:
        wayOut2, costOut2 = getPath(model, start, configuration.settings.OutBuildingC)
        for room in wayOut2:
            if room == model.firePos:
                wayOut1, costOut1 = getPath(model, start, configuration.settings.Out1)
                print("Elegido camino 1 porque el 2 pasaba por el fuego", model.roomFire)
                return wayOut1, configuration.settings.Out1
        print("Elegido camino 2")
        return wayOut2, configuration.settings.OutBuildingC