import random
import configuration.settings

def init():

	global occupancy_json
	#Store the occupancy
	occupancy_json = []


		#Professors
	#Number of Occupants
	NProfessors = 14 #14

	#Define states: name (str), position: str or ditc
	statesProfessors = [
		{'name':'leave', 'position': 'outBuilding'}, #initial state (the first)
		{'name':'working in my office', 'position': {'Office1': 1, 'Office2': 1, 'Office3': 1, 'Office4': 1, 'Office5': 1, 'Office6': 1, 'Office7': 1, 'Office8': 1, 'Office9': 1, 'Office10': 1, 'Office11': 1, 'Office12': 1, 'Office13': 1, 'Office14': 1}},
		{'name':'having a break', 'position': {'Hall': 14}}, #The others will rest in their own workPlace
		{'name':'at restroom', 'position':'Restroom'},
		{'name':'in a meeting', 'position': {'Class4':5 ,'Lab10':3,'Lab12':3,'Lab16':3}},
		{'name':'lunch', 'position': 'outBuilding'},
		{'name':'giving class', 'position':{'outBuilding': 10, 'Class1': 1, 'Class2': 1, 'Class3': 1, 'Class4': 1}},
		{'name':'emergency', 'position':'outBuilding'}
	]

	#states_use_PCs_Professors = ['working in my office', 'giving class']

	#Define initial markov matrix
	markov_matrixProfessors = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

	controlBehaviourProfessors = {'arriveTime': 8.55, 'meetingTime': 10.25, 'lunchTime': 12.55, 'backLunchTime': 14.00, 'classTime': 16.0, 'leaveWorkTime': 18.0, 'leaveWorkTimeMaximun': 20}

	# %Occupants with behaviour: Perfect, good, bad. For "traditional case" only, in other case will be ignored.
	#behaviourEnvironmentProfessors = [25, 60, 15] #25/60/15
	#TconfortProfessors = [19, 27]
	#TconfortWinter = [19, 25]
	#leftClosedDoorProfessors = [7, 10]

	agentProfessor = {'type':'professor' , 'N':NProfessors, 'states': statesProfessors,'matrix': markov_matrixProfessors, 'lifeWay': controlBehaviourProfessors}
	
	occupancy_json.append(agentProfessor)


		#Researchers
	#Number of Occupants
	NResearches = 10 #10

	#Define states: name (str), position: str or ditc
	statesResearchers = [
		{'name':'leave', 'position': 'outBuilding'}, #initial state (the first)
		{'name':'working in my laboratory', 'position': {'Lab1': 1, 'Lab2': 1, 'Lab3': 1, 'Lab4': 1, 'Lab5': 1, 'Lab6': 1, 'Lab7': 1, 'Lab8': 1, 'Lab9': 1, 'Lab11': 0, 'Lab13': 0, 'Lab14': 0, 'Lab15': 0, 'Lab17': 0, 'Lab18': 0, 'Lab19': 0, 'Lab20': 0}},
		{'name':'having a break', 'position': {'Hall': 10}},
		{'name':'at restroom', 'position':'Restroom'},
		{'name':'lunch', 'position': 'outBuilding'},
		{'name':'emergency', 'position':'outBuilding'}
	]

	#states_use_PCsResearchers = ['working in my laboratory']

	#Define initial markov matrix
	markov_matrixResearchers = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

	controlBehaviourResearchers = {'arriveTime': 9.00, 'lunchTime': 13.20, 'backLunchTime': 14.30, 'leaveWorkTime': 17.30, 'leaveWorkTimeMaximun': 20}

	# %Occupants with behaviour: Perfect, good, bad. For "traditional case" only, in other case will be ignored.
	#behaviourEnvironmentResearchers = [35, 60, 5] #35/60/5
	#TconfortResearchers = [19, 27]
	#TconfortWinter = [20, 26]
	#leftClosedDoorResearchers = [7, 10]

	agentResearchers = {'type':'researchers' , 'N':NResearches, 'states': statesResearchers,'matrix': markov_matrixResearchers, 'lifeWay': controlBehaviourResearchers}
	
	occupancy_json.append(agentResearchers)


		#Studients
	#Number of Occupants
	# NStudients = 125 # 4 classes, Class1: 40, Class2: 35, Class3: 30, Class4: 20  Total: 125

	# #Define states: name (str), position: str or ditc
	# statesStudients = [
	# 	{'name':'leave', 'position': 'outBuilding'}, #initial state (the first)
	# 	{'name':'in class', 'position': {'Class1': 40, 'Class2': 35, 'Class3': 30, 'Class4': 20}},
	# 	{'name':'emergency', 'position':'outBuilding'}
	# ]

	# #states_use_PCsStudients = []

	# #Define initial markov matrix
	# markov_matrixStudients = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

	# controlBehaviourStudients = {'arriveTime': 15.55, 'leaveWorkTime': 18.05}

	# # %Occupants with behaviour: Perfect, good, bad. For "traditional case" only, in other case will be ignored.
	# #behaviourEnvironmentStudients = [10, 60, 30] #10/60/30
	# #TconfortStudients = [19, 27]
	# #TconfortWinter = [20, 26]
	# #leftClosedDoorStudients = [4, 7]

	# occupancytudients = {'type':'studients' , 'N':NStudients, 'states': statesStudients, 'matrix': markov_matrixStudients, 'lifeWay': controlBehaviourStudients}
	
	# occupancy_json.append(occupancytudients)

def returnMatrix(agent, time):
	new_matrix = False
	behaviour = agent.behaviour

	if agent.type == 'professor':
		if time > configuration.settings.activationFire:
			new_matrix = [[0, 0, 0, 0, 0, 0, 0, 100], [0, 0, 0, 0, 0, 0, 0, 100], [0, 0, 0, 0, 0, 0, 0, 100], [0, 0, 0, 0, 0, 0, 0, 100],
			[0, 0, 0, 0, 0, 0, 0, 100], [0, 0, 0, 0, 0, 0, 0, 100], [0, 0, 0, 0, 0, 0, 0, 100], [0, 0, 0, 0, 0, 0, 0, 100]]
		elif time < behaviour['arriveTime']:
			new_matrix = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
		elif behaviour['meetingTime'] >= time >= behaviour['arriveTime']:
			new_matrix = [[45, 55, 0, 0, 0, 0, 0, 0], [0, 50, 25, 25, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
		elif (behaviour['meetingTime']+0.9) >= time >= behaviour['meetingTime']:
			new_matrix = [[0, 100, 0, 0, 0, 0, 0, 0], [0, 30, 10, 10, 50, 0, 0, 0], [0, 50, 0, 0, 50, 0, 0, 0], [0, 50, 0, 0, 50, 0, 0, 0], 
			[0, 0, 0, 0, 100, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
		elif behaviour['lunchTime'] >= time >= (behaviour['meetingTime']+0.9):
			new_matrix = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 50, 25, 25, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0, 0], 
			[0, 100, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
		elif behaviour['backLunchTime']  >= time >= behaviour['lunchTime']:
			new_matrix = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 55, 0, 0, 0, 45, 0, 0], [0, 55, 0, 0, 0, 45, 0, 0], [0, 55, 0, 0, 0, 45, 0, 0],
			[0, 55, 0, 0, 0, 45, 0, 0], [0, 55, 0, 0, 0, 45, 0, 0], [0, 55, 0, 0, 0, 45, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
		elif behaviour['classTime'] >= time >= behaviour['backLunchTime']:
			new_matrix = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 74, 13, 13, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0], [0, 55, 0, 0, 0, 45, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
		elif (behaviour['classTime']+0.05) >= time >= behaviour['classTime']:
			new_matrix = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 60, 0, 0, 0, 0, 40, 0], [0, 60, 0, 0, 0, 0, 40, 0], [0, 60, 0, 0, 0, 0, 40, 0],
			[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 100, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
		elif behaviour['leaveWorkTime'] >= time >= (behaviour['classTime']+0.05):
			new_matrix = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 74, 13, 13, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0], [0, 30, 0, 0, 0, 0, 70, 0], [50, 50, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
		elif (behaviour['leaveWorkTimeMaximun']) >time >= behaviour['leaveWorkTime']:
			new_matrix = [[100, 0, 0, 0, 0, 0, 0, 0], [60, 40, 0, 0, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
			[0, 100, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
		elif time >= (behaviour['leaveWorkTimeMaximun']):
			new_matrix = [[100, 0, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0, 0],
			[100, 0, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
		return new_matrix

	elif agent.type == 'researchers':
		if time > configuration.settings.activationFire:
			new_matrix = [[0, 0, 0, 0, 0, 100], [0, 0, 0, 0, 0, 100], [0, 0, 0, 0, 0, 100], [0, 0, 0, 0, 0, 100],
			[0, 0, 0, 0, 0, 100], [0, 0, 0, 0, 0, 100]]
		elif time < behaviour['arriveTime']:
			new_matrix = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
		elif behaviour['arriveTime']+1.3 >= time >= behaviour['arriveTime']:
			new_matrix = [[55, 35, 0, 0, 0, 0], [0, 50, 25, 25, 0, 0], [0, 100, 0, 0, 0, 0],
			[0, 100, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
		elif behaviour['lunchTime'] >= time >= (behaviour['arriveTime']+1.3):
			new_matrix = [[0, 100, 0, 0, 0, 0], [0, 50, 25, 25, 0, 0], [0, 100, 0, 0, 0, 0],
			[0, 100, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
		elif behaviour['backLunchTime']  >= time >= behaviour['lunchTime']:
			new_matrix = [[0, 0, 0, 0, 0, 0], [0, 70, 0, 0, 30, 0], [0, 0, 0, 0, 100, 0],
			[0, 0, 0, 0, 100, 0], [0, 0, 0, 0, 100, 0], [0, 0, 0, 0, 0, 0]]
		elif behaviour['leaveWorkTime'] >= time >= behaviour['backLunchTime']:
			new_matrix = [[0, 0, 0, 0, 0, 0], [0, 50, 25, 25, 0, 0], [0, 100, 0, 0, 0, 0],
			[0, 100, 0, 0, 0, 0], [0, 30, 0, 0, 70, 0], [0, 0, 0, 0, 0, 0]]
		elif (behaviour['leaveWorkTimeMaximun']) >time >= behaviour['leaveWorkTime']:
			new_matrix = [[100, 0, 0, 0, 0, 0], [60, 40, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0],
			[0, 100, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
		elif time >= (behaviour['leaveWorkTimeMaximun']):
			new_matrix = [[100, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0],
			[100, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
		return new_matrix 

	# elif agent.type == 'studients':
	# 	if time > configuration.settings.activationFire:
	# 		new_matrix = [[0, 0, 100], [0, 0, 100], [0, 0, 100]]
	# 	elif time < behaviour['arriveTime']:
	# 		new_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
	# 	elif (behaviour['leaveWorkTime']) >= time >= behaviour['arriveTime']:
	# 		new_matrix =[[30, 70, 0], [0, 100, 0], [0, 0, 0]]
	# 	elif time >= (behaviour['leaveWorkTime']):
	# 		new_matrix = [[100, 0, 0], [70, 30, 0], [0, 0, 0]]
	# 	return new_matrix

	else:
		return new_matrix

def getTimeInState(agent, time): #Hours.Minutes
	timeActivity_matrix = False
	behaviour = agent.behaviour

	if agent.type == 'professor':
		if time > configuration.settings.activationFire:
			timeActivity_matrix = [0, 0, 0, 0, 0, 0, 0, 0]
		elif time < behaviour['arriveTime']:
			timeActivity_matrix = [8.0, 0, 0, 0, 0, 0, 0, 0]
		elif behaviour['meetingTime'] >= time >= behaviour['arriveTime']:
			timeActivity_matrix = [0.30, 1.00, 0.10, 0.10, 0, 0, 0, 0]
		elif (behaviour['meetingTime']+0.9) >= time >= behaviour['meetingTime']:
			timeActivity_matrix = [0, 1.00, 0.10, 0.10, 0.10, 0, 0, 0]
		elif behaviour['lunchTime'] >= time >= (behaviour['meetingTime']+0.9):
			timeActivity_matrix = [0, 1.00, 0.10, 0.10, 0, 0, 0, 0]
		elif behaviour['backLunchTime']  >= time >= behaviour['lunchTime']:
			timeActivity_matrix = [0, 0.10, 0, 0, 0.05, 1.0, 0, 0]
		elif behaviour['classTime'] >= time >= behaviour['backLunchTime']:
			timeActivity_matrix = [0, 0.30, 0.10, 0.10, 0, 0.1, 0, 0]
		elif (behaviour['classTime']+0.05) >= time >= behaviour['classTime']:
			timeActivity_matrix = [0, 1, 0.10, 0.10, 0, 0.1, 2.0, 0]
		elif behaviour['leaveWorkTime'] >= time >= (behaviour['classTime']+0.05):
			timeActivity_matrix = [0, 0.3, 0.10, 0.10, 0, 0, 0, 0]
		elif time >= behaviour['leaveWorkTime']:
			timeActivity_matrix = [5, 0.3, 0.10, 0.10, 0, 0, 0, 0]
		return timeActivity_matrix

	elif agent.type == 'researchers':
		if time > configuration.settings.activationFire:
			timeActivity_matrix = [0, 0, 0, 0, 0, 0]
		elif time < behaviour['arriveTime']:
			timeActivity_matrix = [8.0, 0, 0, 0, 0, 0]
		elif behaviour['lunchTime'] >= time >= behaviour['arriveTime']:
			timeActivity_matrix = [0.30, 1.00, 0.10, 0.10, 0, 0]
		elif behaviour['backLunchTime']  >= time >= behaviour['lunchTime']:
			timeActivity_matrix = [0, 0.05, 0, 0, 1.0, 0]
		elif behaviour['leaveWorkTime'] >= time >= behaviour['backLunchTime']:
			timeActivity_matrix = [0, 1.00, 0.10, 0.10, 0.1, 0]
		elif time >= behaviour['leaveWorkTime']:
			timeActivity_matrix = [5, 0.30, 0.10, 0.10, 0, 0]
		return timeActivity_matrix

	# elif agent.type == 'studients':
	# 	if time > configuration.settings.activationFire:
	# 		timeActivity_matrix = [0, 0, 0]
	# 	if time < behaviour['arriveTime']:
	# 		timeActivity_matrix = [13.0, 0, 0]
	# 	elif (behaviour['leaveWorkTime']) >= time >= behaviour['arriveTime']:
	# 		timeActivity_matrix = [0.01, 2, 0]
	# 	elif time >= behaviour['leaveWorkTime']:
	# 		timeActivity_matrix = [10, 0.01, 0]
	# 	return timeActivity_matrix

	else:
		return timeActivity_matrix