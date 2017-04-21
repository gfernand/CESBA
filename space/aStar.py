import heapq
import random

class Cell(object):
    def __init__(self, pos):
        self.x, self.y = pos
        self.parent = None

def getPath(model, start, finish):
    finish = Cell(finish)
    start = Cell(start)
    not_visited = [start]
    visited = []
    finishCell = None
    notFinished = True
    while notFinished:
        for cell_not_visited in not_visited:
            if cell_not_visited.x == finish.x and cell_not_visited.y == finish.y:
                finishCell = cell_not_visited
                notFinished = False
            else:
                cells = get_conected_cells(model, cell_not_visited) #create adject cells with conection
                for cell in cells:
                    cell_already_visited = isCellVisited(cell, visited)
                    if not cell_already_visited:
                        cell.parent = cell_not_visited
                        not_visited.append(cell)
                not_visited.remove(cell_not_visited)
                visited.append(cell_not_visited)
    cellWay = [finishCell]
    cell = finishCell
    while not (cellWay[len(cellWay)-1] is start):
        cell = cell.parent;
        cellWay.append(cell)
    cellWay.pop()
    way = []
    for cell in cellWay:
        pos = (cell.x, cell.y)
        way.append(pos)
    way.reverse()
    return way

def get_conected_cells(model, cell):
    room = model.getRoom((cell.x, cell.y))
    rooms = room.roomsConected
    cells = []
    for room in rooms:
        cell = Cell(room.pos)
        cells.append(cell)
    return cells

def isCellVisited(cell, visited):
    for cells in visited:
        if cells.x == cell.x and cells.y == cell.y:
            return True
    return False