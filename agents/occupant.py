from mesa import Agent, Model
from transitions import Machine
from transitions import State
import random
from collections import OrderedDict
import operator
from agents.behaviourMarkov import Markov
import space.aStar
import configuration.settings

class Occupant(Agent):

    def __init__(self, unique_id, model, json, environmentBehaviour):
        super().__init__(unique_id, model)
        self.comfort = 0
        self.modelWay = self.model.modelWay

        # Agents' life way 
        self.type = json['type']
        self.behaviour = {}
        for k, v in json['lifeWay'].items():
            if self.model.occupantsValues != False:
                if k == 'arriveTime':
                    self.behaviour['arriveTime'] = self.model.occupantsValues[str(self.unique_id)]['schedule']['day0']['arrive']
                elif k == 'leaveWorkTime':
                    self.behaviour['leaveWorkTime'] = self.model.occupantsValues[str(self.unique_id)]['schedule']['day0']['leave']
                else:
                    self.behaviour[k] = v
            else:
                self.behaviour[k] = v

        self.environment = environmentBehaviour #type 1, 2, 3
        self.positionByState = OrderedDict()
        self.TComfort = random.randint(json['Tconfort'][0], json['Tconfort'][1])
        if self.model.occupantsValues != False:
            self.TComfort = self.model.occupantsValues[str(self.unique_id)]['TComfort']
        self.leftClosedDoor = random.randint(json['leftClosedDoor'][0], json['leftClosedDoor'][1]+1)

        #State machine
        states = []
        for state in json['states']:
            name = state['name']
            if self.model.occupantsValues == False:
                pos = self.model.getPosState(name, self.type)
            else:
                pos = self.model.occupantsValues[str(self.unique_id)]['posByState'][name]
            on_enter = 'start_activity'
            on_exit = 'finish_activity'
            self.positionByState[name] = pos
            states.append(State(name=name, on_enter=[on_enter], on_exit=[on_exit]))
        self.machine = Machine(model=self, states=states, initial=states[0].name)

        self.triggers = {}
        n_state = 0
        for state in json['states']:
            name = state['name']
            self.machine.add_transition('setState'+str(n_state), '*', name)
            self.triggers[name] = 'setState'+str(n_state)+'()'
            n_state = n_state + 1

        self.markov_matrix = json['matrix']
        self.markov_machine = Markov(self)


        #control
        self.markov = True
        self.in_room = False
        self.time_activity = 0
        self.place_to_go = self.model.outBuilding.pos
        self.movements = []
        self.N = 0
        self.opened_door1 = False
        self.opened_door2 = False
        self.lastState = False
        self.onMyWay1 = False
        self.onMyWay2 = False
        self.costMovementToNewRoom = 0
        self.costMovementInNewRoom = 0
        self.lastSchedule = 0.0
        self.scheduleLog = []
        self.arrive = False
        self.leave = False

    # Methods when entering/exit states
    def start_activity(self):
        if self.modelWay == 0:
            self.lastState = self.state
            self.markov = False
            self.place_to_go = self.getPlaceToGo()
        if self.model.occupantsValues == False:
            if self.arrive == False:
                if self.pos != self.place_to_go:
                    self.arrive = self.model.clock.clock
            else:
                if self.leave == False and self.state == 'leave':
                    self.leave = self.model.clock.clock
        if self.pos != self.place_to_go:
            self.movements = space.aStar.getPath(self.model, self.pos, self.place_to_go)
        else:
            self.movements = [self.pos]
        time_in_state = self.model.getTimeInState(self)[list(self.positionByState.keys()).index(self.state)]
        self.time_activity = int(self.model.clock.getMinuteFromHours(time_in_state)*60 / configuration.settings.time_by_step)
        self.N = 0

    #Control models
    def changeSchedule(self):
        beh = sorted(self.behaviour.items(), key=operator.itemgetter(1))
        nextSchedule = False
        for i in beh:
            a, b = i
            if b < self.model.clock.clock:
                nextSchedule = a
        if nextSchedule != self.lastSchedule:
            self.lastSchedule = nextSchedule
            return True
        else:
            return False

        #space.aStar
    def occupantMovePos(self, new_position):
        ux, uy = self.pos
        nx, ny = new_position
        for room in self.model.rooms:
            rx, ry = room.pos
            if room.pos == self.pos:
            #Cost as steps
                if (rx == nx):
                    self.costMovemenToNewRoom = room.dy/2 * (1/configuration.settings.speed) * (1/configuration.settings.time_by_step)# m * seg/m * step/seg
                if (ry == ny):
                    self.costMovemenToNewRoom = room.dx/2 * (1/configuration.settings.speed) * (1/configuration.settings.time_by_step)
            if room.pos == new_position:
                if (rx == ux):
                    self.costMovementInNewRoom = room.dy/2 * (1/configuration.settings.speed) * (1/configuration.settings.time_by_step)
                if (ry == uy):
                    self.costMovementInNewRoom = room.dx/2 * (1/configuration.settings.speed) * (1/configuration.settings.time_by_step)

    def getPlaceToGo(self):
        place_to_go = self.pos
        possible_rooms = []
        for room in self.model.rooms:
            if room.name.split(r".")[0] == self.positionByState[self.state]:
                possible_rooms.append(room.pos)
        if place_to_go in possible_rooms:
            return place_to_go
        if len(possible_rooms) > 1:
            place_to_go = random.choice(possible_rooms)
        elif len(possible_rooms) > 0:
            place_to_go = possible_rooms[0]
        return place_to_go

    # Step from mesa
    def step(self):
        #print('state: ', self.state, ' - cambiar estado: ', self.markov, ' - TA: ', self.time_activity, self.comfort, self.TComfort)
        #print(self.unique_id, self.behaviour, self.TComfort)
        self.model.getMatrix(self)
        if self.markov == True or self.changeSchedule():
            self.markov_machine.runStep(self.markov_matrix)
            #if self.markov == False:
                #self.step()
        elif self.onMyWay1 == True:
            if self.costMovemenToNewRoom > 0:
                self.costMovemenToNewRoom = self.costMovemenToNewRoom - 1
            else:
                room1 = self.model.getRoom(self.pos)
                room2 = self.model.getRoom(self.movements[self.N])
                if room1.name.split(r".")[0] != room2.name.split(r".")[0]:
                    self.model.crossDoor(self, room1, room2)
                    if self.modelWay == 0:
                        self.model.switchLights(self, room1, room2)
                self.model.popAgentRoom(self, self.pos)
                self.model.grid.move_agent(self, self.movements[self.N])
                self.model.pushAgentRoom(self, self.pos)
                self.N = self.N + 1
                self.onMyWay1 = False
                self.onMyWay2 = True
                self.step()
        elif self.onMyWay2 == True:
            if self.costMovementInNewRoom > 0:
                self.costMovementInNewRoom = self.costMovementInNewRoom - 1
            else:
                self.onMyWay2 = False
                if self.modelWay == 0 and len(self.movements) == (self.N + 1):
                    usingPC = self.PCs.get(self.state)
                    if usingPC != None:
                        usingPC.turn_on()
                self.step()
        elif self.pos != self.place_to_go:
            self.occupantMovePos(self.movements[self.N])
            self.onMyWay1 = True
            self.step()
        else:
            self.N = 0
            if self.time_activity > 0:
                self.time_activity = self.time_activity - 1
            else:
                self.markov = True