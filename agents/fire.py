from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
import operator
import space.aStar
import configuration.settings
from configuration.BuildingGrid import *

class Fire(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.fire = True
        self.N = 0
        self.movements = []
        self.distance = 0
        
    def step(self):
        #Aumentar el tamaño
        if self.fire == True:
            #print("Hay fuego y su posicion es:", self.model.fireCells[0])
            # print("Dimensiones:", self.model.roomFire.dx, self.model.roomFire.dy)
            # print("Celdas conectadas:", self.model.roomFire.roomsConected)
            # print("Habitaciones conectadas:", self.model.roomFire.conectedTo)
            # for room in self.model.roomFire.roomsConected:
            #     self.movements, self.distance = space.aStar.getPath(self.model, self.model.roomFire.pos, room.pos)
            #     self.N = self.distance * (1/configuration.settings.speed) * (1/configuration.settings.time_by_step)
            #     # print("Distancia:", self.distance)
            #     # print("Num steps:", self.N)
            #     print(room.name)
            #     print(room.pos, room.dx, room.dy)
            self.N = 0