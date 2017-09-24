from mesa.space import MultiGrid
import random
from space.wall import Wall
from space.door import Door
import configuration.defineMap
import math

class BuildingGrid(MultiGrid):

    def createWalls(self, width, height):
        walls = configuration.defineMap.walls_json
        corners = configuration.defineMap.corners_json
        self.Walls = []
        for wall in walls:
            xRef = -164.037
            yRef = 787.988
            factor = 102.626
            corner1 = wall['corner1']
            corner2 = wall['corner2']
            for corner in corners:
                if corner1 in corner: 
                    c = corner[corner1]
                    #print(corner)
                    xCorner1 = c['x']
                    yCorner1 = c['y']
                    # print(xCorner1)
                    # print(yCorner1)
                if corner2 in corner:
                    c = corner[corner2]
                    #print(corner)
                    xCorner2 = c['x']
                    yCorner2 = c['y']
                    #print(xCorner2)
                    #print(yCorner2)
            xGridCorner1 = abs(round(((xCorner1 - xRef)/factor)))  
            yGridCorner1 = abs(round(((yCorner1 - yRef)/factor))) +3
            xGridCorner2 = abs(round(((xCorner2 - xRef)/factor))) 
            yGridCorner2 = abs(round(((yCorner2 - yRef)/factor))) +3
            #print("Coordenadas x,y de corner 1", xGridCorner1, yGridCorner1)
            #print("Coordenadas x,y de corner 2", xGridCorner2, yGridCorner2)
            if xGridCorner1 == xGridCorner2:
                if yGridCorner1 > yGridCorner2:
                    for yWall in range(yGridCorner2, yGridCorner1):
                        wall = Wall(xGridCorner1, yWall)
                        self.Walls.append(wall)
                        #print("X iguales, metemos muro recorriendo y, yGridCorner1 MAYOR yGridCorner2", xGridCorner1, yWall)
                else:
                    for yWall in range(yGridCorner1, yGridCorner2):
                        wall = Wall(xGridCorner1, yWall)
                        self.Walls.append(wall)
                        #print("X iguales, metemos muro recorriendo y, yGridCorner1 menor yGridCorner2", xGridCorner1, yWall)    
            elif yGridCorner1 == yGridCorner2:
                if xGridCorner1 > xGridCorner2:
                    for xWall in range(xGridCorner2, xGridCorner1):
                        wall = Wall(xWall, yGridCorner1)
                        self.Walls.append(wall)
                        #print("Y iguales, metemos muro recorriendo y, xGridCorner1 MAYOR xGridCorner2", xGridCorner1, yWall)
                else:
                    for xWall in range(xGridCorner1, xGridCorner2):
                        wall = Wall(xWall, yGridCorner1)
                        self.Walls.append(wall)
                        #print("Y iguales, metemos muro recorriendo y, xGridCorner1 menor xGridCorner2", xGridCorner1, yWall) 

            

    def createDoors(self, width, height):
        doors = configuration.defineMap.doors_json
        principalDoor1 = Door(14,3)
        principalDoor2 = Door(15,3)
        principalDoor3 = Door(16,3)
        door1 = Door(33,6)
        door2 = Door(46,6)
        door3 = Door(51,6)
        self.Doors = [principalDoor1, principalDoor2, principalDoor3, door1, door2, door3]
        for door in doors:
            #print(door)
            xRef = -164.037
            yRef = 787.988
            factor = 102.626
            xDoor = door['xpos']
            zYdoor = door['zpos']
            xGridDoor = abs(round(((xDoor - xRef)/factor)))  
            yGridDoor = abs(round(((zYdoor - yRef)/factor))) +3
            #print("Coordenadas x,y de door", xGridDoor, yGridDoor)
            d = Door(xGridDoor,yGridDoor)
            self.Doors.append(d)
        # Clean positions of doors
        for wall in self.Walls:
            for door in self.Doors:
                door.state = False
                if ((wall.x == door.x) and (wall.y == door.y )):
                    self.Walls.remove(wall)


