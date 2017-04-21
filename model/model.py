from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import MultiGrid
from mesa.space import ContinuousSpace

from collections import defaultdict
import random
import os
import os.path

import configuration.settings
import configuration.defineOccupancy
import configuration.defineMap

from log.log import Log

from model.time import Time

from agents.occupant import Occupant

from space.door import Door
from space.room import Room
from space.window import Window
from space.wall import Wall

class SOBAModel(Model):

	def __init__(self, width, height, modelWay = None):

		#Init configurations and defines
		configuration.settings.init()
		configuration.defineOccupancy.init()
		configuration.defineMap.init()

		#Way of working
		if modelWay is None:
			self.modelWay = configuration.settings.model
		else:
			self.modelWay = modelWay

		#Mesa
		self.schedule = BaseScheduler(self)
		self.grid = MultiGrid(width, height, False)
		self.running = True

		#Control of time
		self.clock = Time()

		#Log
		self.log = Log()
		self.roomsSchedule = []
		self.agentSatisfationByStep = []
		self.fangerSatisfationByStep = []
		self.occupantsValues = False
		if self.modelWay != 0 and os.path.isfile('../log/tmp/occupants.txt'):
			self.occupantsValues = self.log.getOccupantsValues()

		#Vars of control
		self.complete = False
		self.num_occupants = 0
		self.day = self.clock.day
		self.NStep = 0
		self.timeToSampling = 'init' # Temperature ThermalLoads
		self.placeByStateByTypeAgent = {}

		#Create the map
		self.createRooms()
		self.setMap(width, height)
		self.createDoors()
		self.createWindows()
		self.createWalls()

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
		#occupantsByTypeRoom = configuration.defineMap.NumberOccupancyByTypeRoom
		for room in rooms:
			newRoom  = 0
			name = room['name']
			typeRoom = room['type']
			if typeRoom != 'out':
				conectedTo = room.get('conectedTo')
				nameThermalZone = room.get('thermalZone')
				entrance = room.get('entrance')
				measures = room['measures']
				dx = measures['dx']
				dy = measures['dy']
				dh = measures['dh']
				jsonWindows = room.get('windows')
				newRoom = Room(name, typeRoom, conectedTo, nameThermalZone, dx, dy, dh, jsonWindows)
				newRoom.entrance = entrance
			else:
				newRoom = Room(name, typeRoom, None, False, 0, 0, 0, {})
				self.outBuilding = newRoom
			self.rooms.append(newRoom)
		for room1 in self.rooms:
			if room1.conectedTo is not None:
				for otherRooms in list(room1.conectedTo.values()):
					for room2 in self.rooms:
						if room2.name == otherRooms:
							room1.roomsConected.append(room2)
							room2.roomsConected.append(room1)
		for room in self.rooms:
			room.roomsConected = list(set(room.roomsConected))
		sameRoom = {}
		for room in self.rooms:
			if sameRoom.get(room.name.split(r".")[0]) is None:
				sameRoom[room.name.split(r".")[0]] = 1
			else:
				sameRoom[room.name.split(r".")[0]] = sameRoom[room.name.split(r".")[0]] + 1

	def setMap(self, width, height):
		rooms_noPos = self.rooms
		rooms_using = []
		rooms_used = []
		for room in self.rooms:
			if room.entrance is not None:
				room.pos = (int(1), 2)
				rooms_using.append(room)
				rooms_used.append(room)
				rooms_noPos.remove(room)
				break
		while len(rooms_noPos) > 0:
			for roomC in rooms_using:
				xc, yc = roomC.pos
				rooms_conected = roomC.conectedTo
				rooms_using.remove(roomC)
				if rooms_conected is not None:
					orientations = list(rooms_conected.keys())
					for orientation in orientations:
						if orientation == 'R':
							for room in rooms_noPos:
								if room.name == rooms_conected['R']:
									room.pos = (int(xc + 1), yc)
									rooms_noPos.remove(room)
									rooms_used.append(room)
									rooms_using.append(room)
						elif orientation == 'U':
							for room in rooms_noPos:
								if room.name == rooms_conected['U']:
									room.pos = (xc, int(yc + 1))
									rooms_noPos.remove(room)
									rooms_used.append(room)
									rooms_using.append(room)
						elif orientation == 'D':
							for room in rooms_noPos:
								if room.name == rooms_conected['D']:
									room.pos = (xc, int(yc - 1))
									rooms_noPos.remove(room)
									rooms_used.append(room)
									rooms_using.append(room)
						elif orientation == 'L':
							for room in rooms_noPos:
								if room.name == rooms_conected['L']:
									room.pos = (int(xc -1), yc)
									rooms_noPos.remove(room)
									rooms_used.append(room)
									rooms_using.append(room)
				else:
					pass
		self.rooms = rooms_used

	def createDoors(self):
		self.doors = []
		for roomC in self.rooms:
			roomsConected = roomC.roomsConected
			for room in roomsConected:
				door_created = False
				same_corridor = False
				if room.name != roomC.name:
					for door in self.doors:
						if (door.room1.name == roomC.name and door.room2.name == room.name) or (door.room2.name == roomC.name and door.room1.name == room.name):
							door_created = True
						if room.name.split(r".")[0] == roomC.name.split(r".")[0]:
							same_corridor = True
					if door_created == False and same_corridor == False:
						d = Door(roomC, room)
						self.doors.append(d)
						room.doors.append(d)
						roomC.doors.append(d)

	def createWindows(self):
		for room in self.rooms:
			windows = []
			json = room.jsonWindows
			if json is None:
				pass
			else:
				for k in json:
					window = Window(k, json[k]['l1'], json[k]['l2'])
					windows.append(window)
			room.windows = windows

	def createWalls(self):
		for room in self.rooms:
			if room.typeRoom != 'out':
				walls = []
				innerWalls = []
				adjRooms = []
				xr, yr = room.pos
				roomA = self.getRoom((xr, yr+1))
				if roomA != False:
					if roomA.typeRoom != 'out':
						if roomA.name.split(r".")[0] == room.name.split(r".")[0]:
							pass
						else:
							wall = Wall(room.dx, room.dh, room, roomA)
							innerWalls.append(wall)
							adjRooms.append(roomA)
					else:
						wall = Wall(room.dx, room.dh, orientation = 'N')
						walls.append(wall)
				else:
					wall = Wall(room.dx, room.dh, orientation = 'N')
					walls.append(wall)
				roomB = self.getRoom((xr, yr-1))
				if roomB != False:
					if roomB.typeRoom != 'out':
						if roomB.name.split(r".")[0] == room.name.split(r".")[0]:
							pass
						else:
							wall = Wall(room.dx, room.dh, room, roomB)
							innerWalls.append(wall)
							adjRooms.append(roomB)
					else:
						wall = Wall(room.dx, room.dh, orientation = 'S')
						walls.append(wall)
				else:
					wall = Wall(room.dx, room.dh, orientation = 'S')
					walls.append(wall)
				roomC = self.getRoom((xr+1, yr))
				if roomC != False:
					if roomC.typeRoom != 'out':
						if roomC.name.split(r".")[0] == room.name.split(r".")[0]:
							pass
						else:
							wall = Wall(room.dy, room.dh, room, roomC)
							innerWalls.append(wall)
							adjRooms.append(roomC)
					else:
						wall = Wall(room.dy, room.dh, orientation = 'E')
						walls.append(wall)
				else:
					wall = Wall(room.dy, room.dh, orientation = 'E')
					walls.append(wall)
				roomD = self.getRoom((xr-1, yr))
				if roomD != False:
					if roomD.typeRoom != 'out':
						if roomD.name.split(r".")[0] == room.name.split(r".")[0]:
							pass
						else:
							wall = Wall(room.dy, room.dh, room, roomD)
							innerWalls.append(wall)
							adjRooms.append(roomD)
					else:
						wall = Wall(room.dy, room.dh, orientation = 'W')
						walls.append(wall)
				else:
					wall = Wall(room.dy, room.dh, orientation = 'W')
					walls.append(wall)
				room.walls = walls
				room.innerWalls = innerWalls
				room.roomsAdj = adjRooms

	def setAgents(self):
		# Identifications
		id_offset = 1000

		# Height and Width
		height = self.grid.height
		width = self.grid.width

		# CREATE AGENTS
		id_occupant = 0
		self.workplaces = []
		self.agents = []
		# Create occupants
			
		for n_type_occupants in configuration.defineOccupancy.occupancy_json:
			self.placeByStateByTypeAgent[n_type_occupants['type']] = n_type_occupants['states']
			n_agents = n_type_occupants['N']
			for i in range(0, n_agents):
				#rooms_with_already_pc = []
				a = Occupant(id_occupant, self, n_type_occupants, '')
				self.agents.append(a)
				id_occupant = 1 + id_occupant
					
				self.schedule.add(a)
				self.grid.place_agent(a, self.outBuilding.pos)
				self.pushAgentRoom(a, self.outBuilding.pos)
				self.num_occupants = self.num_occupants + 1

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

	def thereIsClosedDoor(self, beforePos, nextPos):
		oldRoom = False
		newRoom = False
		for room in rooms:
			if room.pos == beforePos:
				oldRoom = room
			if room.pos == nextPos:
				newRoom = room
		for door in self.doors:
			if (door.room1.name == oldRoom.name and door.room2.name == newRoom.name) or (door.room2.name == oldRoom.name and door.room1.name == newRoom.name):
				if door.state == False:
					return True
		return False

	def thereIsOccupant(self,pos):
		possible_occupant = self.grid.get_cell_list_contents([pos])
		if (len(possible_occupant) > 0):
			for occupant in possible_occupant:
				if isinstance(occupant,Occupant):
					return True
		return False

	def ThereIsOtherOccupantInRoom(self, room, agent):
		for roomAux in self.rooms:
			possible_occupant = []
			if roomAux.name.split(r".")[0] == room.name.split(r".")[0]:
				possible_occupant = self.grid.get_cell_list_contents(roomAux.pos)
			for occupant in possible_occupant:
				if isinstance(occupant, Occupant) and occupant != agent:
					return True
		return False

	def ThereIsSomeOccupantInRoom(self, room):
		for roomAux in self.rooms:
			possible_occupant = []
			if roomAux.name.split(r".")[0] == room.name.split(r".")[0]:
				possible_occupant = self.grid.get_cell_list_contents(roomAux.pos)
			for occupant in possible_occupant:
				if isinstance(occupant, Occupant):
					return True
		return False

	def thereIsOccupantInRoom(self, room, agent):
		for roomAux in self.rooms:
			possible_occupant = []
			if roomAux.name.split(r".")[0] == room.name.split(r".")[0]:
				possible_occupant = self.grid.get_cell_list_contents(roomAux.pos)
			for occupant in possible_occupant:
				if isinstance(occupant, Occupant) and occupant == agent:
					return True
		return False

	def getRoom(self, pos):
		for room in self.rooms:
			if room.pos == pos:
				return room
		return False

	def pushAgentRoom(self, agent, pos):
		room = self.getRoom(pos)
		room.agentsInRoom.append(agent)

	def popAgentRoom(self, agent, pos):
		room = self.getRoom(pos)
		room.agentsInRoom.remove(agent)

	def crossDoor(self, agent, room1, room2):
		numb = random.randint(0, 10)
		for door in self.doors:
			if ((door.room1 == room1 and door.room2 == room2) or (door.room1 == room2 and door.room2 == room1)):
				if  agent.leftClosedDoor >= numb:
					door.state = False
				else:
					door.state = True

	def getMatrix(self,agent):
		new_matrix = configuration.defineOccupancy.returnMatrix(agent, self.clock.clock)
		agent.markov_matrix = new_matrix
	
	def getTimeInState(self, agent):
		matrix_time_in_state = configuration.defineOccupancy.getTimeInState(agent, self.clock.clock)
		return matrix_time_in_state

	def step(self):
		if (self.running == False):
			PID = os.system('$!')
			os.system('kill ' + str(PID))
				
		#Rooms occupancy
		time = self.clock.clock
		day = self.clock.day
		for room in self.rooms:
			if len(room.agentsInRoom) > 0 and room.typeRoom != 'out' and room.typeRoom != 'restRoom':
				self.roomsSchedule.append([room.name, day, time])

		if (self.clock.day > self.day):
			self.day = self.day + 1
		self.NStep = self.NStep + 1