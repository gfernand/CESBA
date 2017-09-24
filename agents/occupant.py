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

    def __init__(self, unique_id, model, json):
        super().__init__(unique_id, model)

        # Agents' life way 
        self.behaviour = json['lifeWay']
        self.type = json['type']
        
        #State machine
        self.positionByState = OrderedDict()
        states = []
        for state in json['states']:
            name = state['name']
            pos = self.model.getPosState(name, self.type)
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
        self.time_activity = 0
        self.place_to_go = self.model.outBuilding
        self.movements = []
        self.distance = 0
        self.N = 0
        self.onMyWay = False
        self.onMyWay1 = False
        self.onMyWay2 = False
        self.costMovementToNewRoom = 0
        self.costMovementInNewRoom = 0
        self.lastSchedule = 0.0
        self.room1 = False
        self.room2 = False
        self.dead = False
        self.oldMan = False #random.choice([True, False])
        self.NoldMan = 0
        self.block = 0
        self.family = 0#random.choice([1, 2])
        self.child = False
        self.parent = False
        self.together = False
        
    # Methods when entering/exit states
    def start_activity(self):
        self.markov = False
        ## Dependiendo del tipo de politica a elegir, comentaremos y descomentaremos
        ## la parte del código necesaria para su correcto funcionamiento.

        ## Politica de salida más cercana.
        # if (self.state == 'emergency'):
        #     self.movements, self.place_to_go = space.aStar.getNearOut(self.model, self.pos)
        # else:


        ## Politica de salida más segura(más lejana al fuego sin pasar por él en el momento de elegir el camino.
        # if (self.state == 'emergency'):
        #     self.movements, self.place_to_go = space.aStar.getSafestOut(self.model, self.pos)
        # else:

        ## Politica de salida más cercana pero con modelo de afiliación.
        if (self.state == 'emergency'):
            if self.family == 1:
                if self.parent:
                    if self.pos != self.model.posChild1 and self.pos != (14,2):
                        self.movements, self.distance = space.aStar.getPath(self.model, self.pos, self.model.posChild1)
                        self.place_to_go = self.model.posChild1
                        print("soy padre y voy a por mi hijo", self.place_to_go)
                        for member in self.model.family1:
                            if member.child:
                                member.place_to_go = member.pos
                elif self.child:
                    self.place_to_go = self.pos
                else:
                    self.place_to_go = self.getPlaceToGo()
                    if self.pos != self.place_to_go:
                        self.movements, self.distance = space.aStar.getPath(self.model, self.pos, self.place_to_go)
                    else:
                        self.movements = [self.pos]
                    time_in_state = self.model.getTimeInState(self)[list(self.positionByState.keys()).index(self.state)]
                    self.time_activity = int(self.model.clock.getMinuteFromHours(time_in_state)*60 / configuration.settings.time_by_step)
                    self.N = 0
            elif self.family == 2:
                if self.parent:
                    if self.pos != self.model.posChild1 and self.pos != (14,2):
                        self.movements, self.distance = space.aStar.getPath(self.model, self.pos, self.model.posChild2)
                        self.place_to_go = self.model.posChild2
                        print("soy padre y voy a por mi hijo", self.place_to_go)
                        for member in self.model.family2:
                            if member.child:
                                member.place_to_go = member.pos
                elif self.child:
                    self.place_to_go = self.pos
                else:
                    self.place_to_go = self.getPlaceToGo()
                    if self.pos != self.place_to_go:
                        self.movements, self.distance = space.aStar.getPath(self.model, self.pos, self.place_to_go)
                    else:
                        self.movements = [self.pos]
                    time_in_state = self.model.getTimeInState(self)[list(self.positionByState.keys()).index(self.state)]
                    self.time_activity = int(self.model.clock.getMinuteFromHours(time_in_state)*60 / configuration.settings.time_by_step)
                    self.N = 0
            else:
                self.place_to_go = self.getPlaceToGo()
                if self.pos != self.place_to_go:
                    self.movements, self.distance = space.aStar.getPath(self.model, self.pos, self.place_to_go)
                else:
                    self.movements = [self.pos]
                time_in_state = self.model.getTimeInState(self)[list(self.positionByState.keys()).index(self.state)]
                self.time_activity = int(self.model.clock.getMinuteFromHours(time_in_state)*60 / configuration.settings.time_by_step)
                self.N = 0                
        else:
            ## Parte común a los tres casos que debe ir a continuación del 'else' correspondiente de cada caso.
            self.place_to_go = self.getPlaceToGo()
            if self.pos != self.place_to_go:
                self.movements, self.distance = space.aStar.getPath(self.model, self.pos, self.place_to_go)
            else:
                self.movements = [self.pos]
            time_in_state = self.model.getTimeInState(self)[list(self.positionByState.keys()).index(self.state)]
            self.time_activity = int(self.model.clock.getMinuteFromHours(time_in_state)*60 / configuration.settings.time_by_step)
            self.N = 0

    def finish_activity(self):
        pass

    #Movement
    def occupantMovePos(self, pos):
        possible_steps = self.model.grid.get_neighborhood(
        pos,
        moore=False,
        include_center=False)
        for is_wall in self.model.Walls:
            w = (is_wall.x, is_wall.y)
            for cell in possible_steps:
                if w == cell or self.model.thereIsOccupant(cell):
                    possible_steps.remove(cell)
        if len(possible_steps) != 0:
            unBlockPos = random.choice(possible_steps)
            #print("unBlockPos:", unBlockPos, "Pos block:", self.pos)
            self.model.grid.move_agent(self, unBlockPos)
            self.movements, self.distance = space.aStar.getPath(self.model, self.pos, self.place_to_go)
            self.N = 0
            self.NoldMan = 0        

    def getPlaceToGo(self):
        place_to_go = self.pos
        #print("Posicion:", self.pos)
        possible_cells = []
        for room in self.model.rooms:
            if room.name.split(r".")[0] == self.positionByState[self.state]:
                for x in room.x:
                    for y in room.y:
                        cell = (x,y)
                        if self.positionByState[self.state] == 'outBuilding' or self.positionByState[self.state] == 'BuildingC':
                            possible_cells.append(cell)
                        elif self.model.thereIsOccupant(cell) == False:
                            possible_cells.append(cell)
        #print("possible_cells:", possible_cells)
        if place_to_go in possible_cells:
            return place_to_go
        if len(possible_cells) > 1:
            place_to_go = random.choice(possible_cells)
        elif len(possible_cells) > 0:
            place_to_go = possible_cells[0]
        #print("place_to_go", place_to_go)
        return place_to_go

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

    #Step from mesa
    def step(self):
        self.model.getMatrix(self)
        if (self.markov == True or self.changeSchedule()) and (self.state != 'emergency'):
            self.markov_machine.runStep(self.markov_matrix)
        elif self.pos != self.place_to_go:
            if self.model.fire:
                self.model.isBurned(self, self.pos)
            if self.oldMan == True:
                if self.NoldMan == 1:
                    if self.N < len(self.movements):
                        if self.model.thereIsOccupant(self.movements[self.N]) == False:
                            #self.occupantMovePos(self.movements[self.N])
                            #self.model.popAgentRoom(self, self.pos)
                            self.model.grid.move_agent(self, self.movements[self.N])
                            #self.model.pushAgentRoom(self, self.pos)
                            self.N = self.N + 1
                            self.NoldMan = 0
                        elif self.model.occupant_going_to_my_pos(self.movements[self.N],self.pos) == True:
                            self.occupantMovePos(self.pos)
                        else:
                            if self.pos != (14,2):
                                self.block = self.block + 1
                                if self.block == 3:
                                    self.occupantMovePos(self.pos)
                                    self.block = 0
                    else:
                        if self.pos != (14,2):
                            self.block = self.block + 1
                            if self.block == 3:
                                self.occupantMovePos(self.pos)
                                self.block = 0
                else:
                    self.NoldMan = self.NoldMan + 1
            else:
                if self.N < len(self.movements):
                    if self.model.thereIsOccupant(self.movements[self.N]) == False:
                        #self.occupantMovePos(self.movements[self.N])
                        #self.model.popAgentRoom(self, self.pos)
                        self.model.grid.move_agent(self, self.movements[self.N])
                        #self.model.pushAgentRoom(self, self.pos)
                        self.N = self.N + 1
                        if self.state == 'emergency':
                            if self.parent and self.family == 1 and self.together == False:
                                if self.movements[self.N] == self.model.posChild1:
                                    # self.movements, self.place_to_go = space.aStar.getNearOut(self.model, self.pos) #para nearest
                                    self.place_to_go = self.getPlaceToGo()
                                    self.movements, self.distance = space.aStar.getPath(self.model, self.pos, self.place_to_go)
                                    self.N = 0
                                    for member in self.model.family1:
                                        if member.child:
                                            # member.movements, member.place_to_go = space.aStar.getNearOut(self.model, member.pos)
                                            member.place_to_go = member.getPlaceToGo()
                                            member.movements, member.distance = space.aStar.getPath(self.model, member.pos, member.place_to_go)
                                            member.N = 0
                                            self.together = True
                            elif self.parent and self.family == 2 and self.together == False:
                                if self.movements[self.N] == self.model.posChild2:
                                    # self.movements, self.place_to_go = space.aStar.getNearOut(self.model, self.pos) #para nearest
                                    self.place_to_go = self.getPlaceToGo()
                                    self.movements, self.distance = space.aStar.getPath(self.model, self.pos, self.place_to_go)
                                    self.N = 0
                                    for member in self.model.family2:
                                        if member.child:
                                            # member.movements, member.place_to_go = space.aStar.getNearOut(self.model, member.pos)
                                            member.place_to_go = member.getPlaceToGo()
                                            member.movements, member.distance = space.aStar.getPath(self.model, member.pos, member.place_to_go)
                                            member.N = 0
                                            self.together = True
                    elif self.model.occupant_going_to_my_pos(self.movements[self.N],self.pos) == True:
                        self.occupantMovePos(self.pos)
                    else:
                        if self.pos != (14,2):
                            self.block = self.block + 1
                            if self.block == 3:
                                self.occupantMovePos(self.pos)
                                self.block = 0
                else:
                    if self.pos != (14,2):
                        self.block = self.block + 1
                        if self.block == 3:
                            self.occupantMovePos(self.pos)
                            self.block = 0
        else:
            self.N = 0
            if self.time_activity > 0:
                self.time_activity = self.time_activity - 1
            else:
                self.markov = True