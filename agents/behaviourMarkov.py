import random
from transitions import *

class Markov(object):

	def __init__(self, agent_aux):
		self.agent = agent_aux

	def runStep(self, markov_matrix):
		currentState = self.agent.state
		numberCurrentState = False
		self.n = 0
		for state in self.agent.machine.states:
			if state == currentState:
				break
			self.n = self.n + 1 
		numberCurrentState = self.n
		numberNextState = self.getNextState(numberCurrentState)
		if (numberNextState != 0) and (numberNextState == False):
			return
		listKeyStates = list(self.agent.machine.states.keys())
		nextState = self.agent.machine.states[listKeyStates[numberNextState]]
		for n in self.agent.triggers.keys():
			if n == nextState.name:
				trigger = self.agent.triggers[n]
				cast = 'self.agent.'+ trigger
				eval(cast)

	def getNextState(self, NumberCurrentState):
		vector = self.agent.markov_matrix[NumberCurrentState]
		randomNumber = random.randrange(0, 101)
		self.n = -1
		value_aux = 0
		for pos in vector: 
			self.n = self.n + 1
			value_aux = value_aux + pos
			if value_aux > randomNumber:
				return self.n
		return False