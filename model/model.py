from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from configuration.BuildingGrid import *

from collections import defaultdict
import random
import os
import os.path

import configuration.settings
import configuration.defineOccupancy
import configuration.defineOccupancyFamily
import configuration.defineMap

from log.log import Log
from model.time import Time
from agents.occupant import Occupant
from agents.fire import Fire
from space.room import Room
from space.door import Door
from space.wall import Wall

class CESBAModel(Model):

    def __init__(self, width, height, modelWay = None):

        #Init configurations and defines
        configuration.settings.init()
        configuration.defineOccupancy.init()
        configuration.defineOccupancyFamily.init()
        configuration.defineMap.init()

        #Mesa
        self.schedule = BaseScheduler(self)
        self.grid = BuildingGrid(width, height, False)
        self.running = True
        
        #Control of time
        offsetTime = 7000
        self.clock = Time(offsetTime, self)

        #Log
        self.log = Log()
        self.agentsWorkingByStep = []
        self.agentsBurnedByStep = []
        self.occupantsInRoomByTime = {}

        #Vars of control
        self.num_occupants = 0
        self.day = self.clock.day
        self.NStep = 0
        self.placeByStateByTypeAgent = {}
        self.activation = 0.0
        self.fire = False
        self.id_fire = 3000
        self.reactTime = 0
        self.roomFire = "Office1"
        self.firePos = (0,0)
        self.fireCells = []
        self.NStepFire = 0
        self.burned = 0
        self.outBuilding = (14,2)
        self.family1 = []
        self.family2 = []
        self.posChild1 = (14,2)
        self.posChild2 = (14,2)

        #Create the map
        self.createRooms()
        BuildingGrid.createWalls(self,width, height)
        BuildingGrid.createDoors(self,width, height)


        #Create agents
        self.setAgents()
        
    def isConected(self, pos):
        nextRoom = False
        for room in self.rooms:
            if room.pos == pos:
                nextRoom = room
        if nextRoom == False:
            return False
        for x in range(0, width):
            for y in range(0, height):
                self.pos_out_of_map.append(x, y)
        for room in self.rooms:
            self.pos_out_of_map.remove(room.pos)

    def createRooms(self):
        rooms = configuration.defineMap.rooms_json
        self.rooms = []
        for room in rooms:
            newRoom  = 0
            name = room['name']
            door = room['door']
            x = room['x']
            y = room['y']
            newRoom = Room(name, door)
            for xr in x:
                newRoom.x.append(xr)
            for yr in y:
                newRoom.y.append(yr)
            self.rooms.append(newRoom)
        #log
        for room in self.rooms:
            self.occupantsInRoomByTime[room.name] = []

    def setAgents(self):
        # Identifications
        id_offset = 1000

        # Height and Width
        height = self.grid.height
        width = self.grid.width

        # CREATE AGENTS

        id_occupant = id_offset
        self.agents = []
        # Create occupants
        for n_type_occupants in configuration.defineOccupancy.occupancy_json:
            self.placeByStateByTypeAgent[n_type_occupants['type']] = n_type_occupants['states']
            n_agents = n_type_occupants['N']
            for i in range(0, n_agents):
                a = Occupant(id_occupant, self, n_type_occupants)
                self.agents.append(a)
                id_occupant = 1 + id_occupant
                self.schedule.add(a)
                self.grid.place_agent(a, self.outBuilding)
                self.pushAgentRoom(a, self.outBuilding)
                self.num_occupants = self.num_occupants + 1
                if len(self.family1) < 5:
                    a.family = 1
                    if len(self.family1) < 1:
                        a.child = True
                    elif len(self.family1) < 2:
                        a.parent = True
                    self.family1.append(a)
                elif len(self.family2) < 5:
                    a.family = 2
                    if len(self.family2) < 1:
                        a.child = True
                    elif len(self.family2) < 2:
                        a.parent = True
                    self.family2.append(a)
        self.schedule.add(self.clock)

    def getPosState(self, name, typeA):
        placeByStateByTypeAgent = self.placeByStateByTypeAgent
        n = 0
        for state in self.placeByStateByTypeAgent[typeA]:
            if state.get('name') == name:
                pos1 = state.get('position')
                if isinstance(pos1, dict):
                    for k,v in pos1.items():
                        if v > 0:
                            placeByStateByTypeAgent[typeA][n]['position'][k] = v - 1
                            self.placeByStateByTypeAgent = placeByStateByTypeAgent
                            return k
                    return list(pos1.keys())[-1]
                else:
                    return pos1
            n = n +1

    def thereIsOccupant(self, pos):
        possible_occupant = self.grid.get_cell_list_contents([pos])
        if (len(possible_occupant) > 0):
            for occupant in possible_occupant:
                if isinstance(occupant,Occupant):
                    if (pos == configuration.settings.Out1) or (pos == configuration.settings.OutBuildingC):
                        return False
                    else:
                        return True
        return False

    def occupant_going_to_my_pos(self, pos, pos1):
        possible_occupant = self.grid.get_cell_list_contents([pos])
        if (len(possible_occupant) > 0):
            for occupant in possible_occupant:
                if isinstance(occupant,Occupant):
                    if (pos == configuration.settings.Out1) or (pos == configuration.settings.OutBuildingC):
                        return False
                    else:
                        if occupant.N < len(occupant.movements):
                            #print(occupant.pos, "NEXT POS:", occupant.movements[occupant.N], "PLACE TO GO:", occupant.place_to_go, "MY POS:", pos1)
                            if occupant.movements[occupant.N] == pos1:
                                print("EL ocupante va a mi posicion")
                                return True
                            else:
                                return False
                        else:
                            return False
        return False

    def thereIsFire(self, pos):
        possible_fire = self.grid.get_cell_list_contents([pos])
        if (len(possible_fire) > 0):
            for fire in possible_fire:
                if isinstance(fire,Fire):
                    return True
        return False

    def getRoom(self, pos):
        xpos,ypos = pos
        for room in self.rooms:
            if xpos in room.x and ypos in room.y:
                return room
        return False

    def pushAgentRoom(self, agent, pos):
        room = self.getRoom(pos)
        room.agentsInRoom.append(agent)

    def popAgentRoom(self, agent, pos):
        room = self.getRoom(pos)
        room.agentsInRoom.remove(agent)

    def getMatrix(self,agent):
        new_matrix = configuration.defineOccupancy.returnMatrix(agent, self.clock.clock)
        agent.markov_matrix = new_matrix
    
    def getTimeInState(self, agent):
        matrix_time_in_state = configuration.defineOccupancy.getTimeInState(agent, self.clock.clock)
        return matrix_time_in_state

    def isBurned(self, agent, pos):
        for fire in self.fireCells:
            if pos == fire:
                self.burned = self.burned + 1
                print("Agente quemado", self.burned, agent.unique_id, "AgenteViejo:", agent.oldMan)
                for agentBurned in self.agents:
                    if agentBurned.unique_id == agent.unique_id:
                        agentBurned.dead = True                

    def step(self):
        for member in self.family1:
            if member.child:
                self.posChild1 = member.pos
        for member in self.family2:
            if member.child:
                self.posChild2 = member.pos
        if configuration.settings.activationFire == self.clock.clock:
            self.fire = True
            a = Fire(self.id_fire,self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            for room in self.rooms:
                if room.name == 'Office8':
                    self.roomFire = room
            possible_cells_fire = []
            for x in self.roomFire.x:
                    for y in self.roomFire.y:
                        cell = (x,y)
                        possible_cells_fire.append(cell)
            self.firePos = (64,15)#random.choice(possible_cells_fire)
            self.grid.place_agent(a, self.firePos)
            self.fireCells.append((self.firePos))
            #self.pushAgentRoom(a, self.firePos)
            print("Hora activacion fuego:", configuration.settings.activationFire, "y posicion donde se ha creado", self.roomFire.name) 
        
        if self.fire == True:
            self.NStepFire = self.NStepFire + 1 
            self.reactTime = self.reactTime + 1 
            if self.reactTime < 60:
                for agent in self.agents:
                    if self.getRoom(agent.pos) == self.roomFire:
                        print("ROOM:", self.getRoom(agent.pos))    
                        print("POS:", agent.pos)
                        if agent.state != 'emergency':
                            agent.markov = True
            if self.reactTime == 60:
                for agent in self.agents:
                    if agent.state != 'emergency':
                        agent.markov = True
            for agent in self.agents:
                if agent.dead == True:
                    self.schedule.remove(agent)
            if self.NStepFire == 30:
                newFireCells = []
                for fire in self.fireCells:
                    possible_steps = self.grid.get_neighborhood(
                    fire,
                    moore=True,
                    include_center=False)
                    for is_wall in self.Walls:
                        w = (is_wall.x, is_wall.y)
                        for cell in possible_steps:
                            if w == cell or self.thereIsFire(cell):
                                #print("Muro:", w, "PosibleStep:", cell)
                                possible_steps.remove(cell)
                    for spread_fire in possible_steps:
                        self.id_fire = self.id_fire + 1
                        a = Fire(self.id_fire,self)
                        self.schedule.add(a)
                        self.grid.place_agent(a, spread_fire)
                        newFireCells.append((spread_fire))
                for new in newFireCells:
                    self.fireCells.append((new))
                    newFireCells.remove(new)
                self.NStepFire = 0

        #log
        for room in self.rooms:
            self.occupantsInRoomByTime[room.name].append(len(room.agentsInRoom))
        aw = 0
        for agent in self.agents:
            if agent.dead == True:
                aw = aw + 1
        self.agentsBurnedByStep.append(aw)
        self.schedule.step()


        if (self.clock.day > self.day):
            self.day = self.day + 1
        self.NStep = self.NStep + 1