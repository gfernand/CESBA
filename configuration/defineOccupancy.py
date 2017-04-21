import random

def init():

	global occupancy_json
	#Store the occupancy
	occupancy_json = []


		#Professors
	#Number of Occupants
	NProfessors = 40 #40

	#Define states: name (str), position: str or ditc
	statesProfessors = [
		{'name':'leave', 'position': 'outBuilding'}, #initial state (the first)
		{'name':'working in my office', 'position': {'Office1': 2, 'Office2': 3, 'Office3': 3, 'Office4': 4, 'Office5': 3, 'Office6': 1, 'Office7': 3, 'Office8': 5, 'Office9': 2, 'Office10': 4, 'Office11': 3, 'Office12': 3, 'Office13': 2, 'Office14': 2}},
		{'name':'having a break', 'position': {'Hall': 16}}, #The others will rest in their own workPlace
		{'name':'at restroom', 'position':'Restroom'},
		{'name':'in a meeting', 'position': {'Class4':10 ,'Lab10':10,'Lab12':10,'Lab16':10}},
		{'name':'lunch', 'position': 'outBuilding'},
		{'name':'giving class', 'position':{'outBuilding': 24, 'Class1': 4, 'Class2': 4, 'Class3': 4, 'Class4': 4}}
	]

	states_use_PCs_Professors = ['working in my office', 'giving class']

	#Define initial markov matrix
	markov_matrixProfessors = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

	controlBehaviourProfessors = {'arriveTime': 8.55, 'meetingTime': 10.25, 'lunchTime': 12.55, 'backLunchTime': 14.00, 'classTime': 16.0, 'leaveWorkTime': 18.0, 'leaveWorkTimeMaximun': 20}

	# %Occupants with behaviour: Perfect, good, bad. For "traditional case" only, in other case will be ignored.
	behaviourEnvironmentProfessors = [25, 60, 15] #25/60/15
	TconfortProfessors = [19, 27]
	#TconfortWinter = [19, 25]
	leftClosedDoorProfessors = [7, 10]

	agentProfessor = {'type':'professor' , 'N':NProfessors, 'states': statesProfessors, 'PCs': states_use_PCs_Professors ,'matrix': markov_matrixProfessors, 'lifeWay': controlBehaviourProfessors, 'environment':behaviourEnvironmentProfessors, 'Tconfort':TconfortProfessors, 'leftClosedDoor': leftClosedDoorProfessors}
	
	occupancy_json.append(agentProfessor)


		#Researchers
	#Number of Occupants
	NResearches = 40 #40

	#Define states: name (str), position: str or ditc
	statesResearchers = [
		{'name':'leave', 'position': 'outBuilding'}, #initial state (the first)
		{'name':'working in my laboratory', 'position': {'Lab1': 1, 'Lab2': 1, 'Lab3': 1, 'Lab4': 1, 'Lab5': 1, 'Lab6': 3, 'Lab7': 2, 'Lab8': 2, 'Lab9': 2, 'Lab11': 3, 'Lab13': 3, 'Lab14': 3, 'Lab15': 5, 'Lab17': 4, 'Lab18': 2, 'Lab19': 3, 'Lab20': 3}},
		{'name':'having a break', 'position': {'Hall': 26}},
		{'name':'at restroom', 'position':'Restroom'},
		{'name':'lunch', 'position': 'outBuilding'}
	]

	states_use_PCsResearchers = ['working in my laboratory']

	#Define initial markov matrix
	markov_matrixResearchers = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

	controlBehaviourResearchers = {'arriveTime': 9.00, 'lunchTime': 13.20, 'backLunchTime': 14.30, 'leaveWorkTime': 17.30, 'leaveWorkTimeMaximun': 20}

	# %Occupants with behaviour: Perfect, good, bad. For "traditional case" only, in other case will be ignored.
	behaviourEnvironmentResearchers = [35, 60, 5] #35/60/5
	TconfortResearchers = [19, 27]
	#TconfortWinter = [20, 26]
	leftClosedDoorResearchers = [7, 10]

	agentResearchers = {'type':'researchers' , 'N':NResearches, 'states': statesResearchers, 'PCs': states_use_PCsResearchers ,'matrix': markov_matrixResearchers, 'lifeWay': controlBehaviourResearchers, 'environment':behaviourEnvironmentResearchers, 'Tconfort':TconfortResearchers, 'leftClosedDoor': leftClosedDoorResearchers}
	
	occupancy_json.append(agentResearchers)


		#Studients
	#Number of Occupants
	NStudients = 125 # 4 classes, Class1: 40, Class2: 35, Class3: 30, Class4: 20  Total: 125

	#Define states: name (str), position: str or ditc
	statesStudients = [
		{'name':'leave', 'position': 'outBuilding'}, #initial state (the first)
		{'name':'in class', 'position': {'Class1': 40, 'Class2': 35, 'Class3': 30, 'Class4': 20}},
	]

	states_use_PCsStudients = []

	#Define initial markov matrix
	markov_matrixStudients = [[0, 0], [0, 0]]

	controlBehaviourStudients = {'arriveTime': 15.55, 'leaveWorkTime': 18.05}

	# %Occupants with behaviour: Perfect, good, bad. For "traditional case" only, in other case will be ignored.
	behaviourEnvironmentStudients = [10, 60, 30] #10/60/30
	TconfortStudients = [19, 27]
	#TconfortWinter = [20, 26]
	leftClosedDoorStudients = [4, 7]

	occupancytudients = {'type':'studients' , 'N':NStudients, 'states': statesStudients, 'PCs': states_use_PCsStudients, 'matrix': markov_matrixStudients, 'lifeWay': controlBehaviourStudients, 'environment':behaviourEnvironmentStudients, 'Tconfort':TconfortStudients, 'leftClosedDoor': leftClosedDoorStudients}
	
	occupancy_json.append(occupancytudients)

def returnMatrix(agent, time):
	new_matrix = False
	behaviour = agent.behaviour

	if agent.type == 'professor':
		if time < behaviour['arriveTime']:
			new_matrix = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
		elif behaviour['meetingTime'] >= time >= behaviour['arriveTime']:
			if agent.model.occupantsValues == False:
				new_matrix = [[45, 55, 0, 0, 0, 0, 0], [0, 50, 25, 25, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0], 
				[0, 0, 0, 0, 0, 0, 0 ], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
			else:
				new_matrix = [[70, 30, 0, 0, 0, 0, 0], [0, 50, 25, 25, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0], 
				[0, 0, 0, 0, 0, 0, 0 ], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
		elif (behaviour['meetingTime']+0.9) >= time >= behaviour['meetingTime']:
			new_matrix = [[0, 100, 0, 0, 0, 0, 0], [0, 30, 10, 10, 50, 0, 0], [0, 50, 0, 0, 50, 0, 0], [0, 50, 0, 0, 50, 0, 0], 
			[0, 0, 0, 0, 100, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
		elif behaviour['lunchTime'] >= time >= (behaviour['meetingTime']+0.9):
			new_matrix = [[0, 0, 0, 0, 0, 0, 0], [0, 50, 25, 25, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0], 
			[0, 100, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
		elif behaviour['backLunchTime']  >= time >= behaviour['lunchTime']:
			new_matrix = [[0, 0, 0, 0, 0, 0, 0], [0, 55, 0, 0, 0, 45, 0], [0, 55, 0, 0, 0, 45, 0], [0, 55, 0, 0, 0, 45, 0],
			[0, 55, 0, 0, 0, 45, 0], [0, 55, 0, 0, 0, 45, 0], [0, 55, 0, 0, 0, 45, 0]]
		elif behaviour['classTime'] >= time >= behaviour['backLunchTime']:
			new_matrix = [[0, 0, 0, 0, 0, 0, 0], [0, 74, 13, 13, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0], [0, 55, 0, 0, 0, 45, 0], [0, 0, 0, 0, 0, 0, 0]]
		elif (behaviour['classTime']+0.05) >= time >= behaviour['classTime']:
			new_matrix = [[0, 0, 0, 0, 0, 0, 0], [0, 60, 0, 0, 0, 0, 40], [0, 60, 0, 0, 0, 0, 40], [0, 60, 0, 0, 0, 0, 40],
			[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 100]]
		elif behaviour['leaveWorkTime'] >= time >= (behaviour['classTime']+0.05):
			new_matrix = [[0, 0, 0, 0, 0, 0, 0], [0, 74, 13, 13, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0], 
			[0, 0, 0, 0, 0, 0, 0], [0, 30, 0, 0, 0, 0, 70], [50, 50, 0, 0, 0, 0, 0]]
		elif (behaviour['leaveWorkTimeMaximun']) >time >= behaviour['leaveWorkTime']:
			if agent.model.occupantsValues == False:
				new_matrix = [[100, 0, 0, 0, 0, 0, 0], [60, 40, 0, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
				[0, 100, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0]]
			else:
				new_matrix = [[100, 0, 0, 0, 0, 0, 0], [30, 70, 0, 0, 0, 0, 0], [0, 100, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
				[0, 100, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0]]
		elif time >= (behaviour['leaveWorkTimeMaximun']):
			new_matrix = [[100, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0],
			[100, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0], [100, 0, 0, 0, 0, 0, 0]]
		return new_matrix

	elif agent.type == 'researchers':
		if time < behaviour['arriveTime']:
			new_matrix = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
		elif behaviour['arriveTime']+1.3 >= time >= behaviour['arriveTime']:
			if agent.model.occupantsValues == False:
				new_matrix = [[55, 35, 0, 0, 0], [0, 50, 25, 25, 0], [0, 100, 0, 0, 0],
				[0, 100, 0, 0, 0], [0, 0, 0, 0, 0]]
			else:
				new_matrix = [[70, 30, 0, 0, 0], [0, 50, 25, 25, 0], [0, 100, 0, 0, 0],
				[0, 100, 0, 0, 0], [0, 0, 0, 0, 0]]
		elif behaviour['lunchTime'] >= time >= (behaviour['arriveTime']+1.3):
			new_matrix = [[0, 100, 0, 0, 0], [0, 50, 25, 25, 0], [0, 100, 0, 0, 0],
			[0, 100, 0, 0, 0], [0, 0, 0, 0, 0]]
		elif behaviour['backLunchTime']  >= time >= behaviour['lunchTime']:
			new_matrix = [[0, 0, 0, 0, 0], [0, 70, 0, 0, 30], [0, 0, 0, 0, 100],
			[0, 0, 0, 0, 100], [0, 0, 0, 0, 100]]
		elif behaviour['leaveWorkTime'] >= time >= behaviour['backLunchTime']:
			new_matrix = [[0, 0, 0, 0, 0], [0, 50, 25, 25, 0], [0, 100, 0, 0, 0],
			[0, 100, 0, 0, 0], [0, 30, 0, 0, 70]]
		elif (behaviour['leaveWorkTimeMaximun']) >time >= behaviour['leaveWorkTime']:
			if agent.model.occupantsValues == False:
				new_matrix = [[100, 0, 0, 0, 0], [60, 40, 0, 0, 0], [0, 100, 0, 0, 0],
				[0, 100, 0, 0, 0], [0, 0, 0, 0, 0]]
			else:
				new_matrix = [[100, 0, 0, 0, 0], [30, 70, 0, 0, 0], [0, 100, 0, 0, 0],
				[0, 100, 0, 0, 0], [0, 0, 0, 0, 0]]
		elif time >= (behaviour['leaveWorkTimeMaximun']):
			new_matrix = [[100, 0, 0, 0, 0], [100, 0, 0, 0, 0], [100, 0, 0, 0, 0],
			[100, 0, 0, 0, 0], [100, 0, 0, 0, 0]]
		return new_matrix 

	elif agent.type == 'studients':
		if time < behaviour['arriveTime']:
			new_matrix = [[0, 0], [0, 0]]
		elif (behaviour['leaveWorkTime']) >= time >= behaviour['arriveTime']:
			new_matrix =[[30, 70], [0, 100]]
		elif time >= (behaviour['leaveWorkTime']):
			new_matrix = [[100, 0], [70, 30]]
		return new_matrix

	else:
		return new_matrix

def getTimeInState(agent, time): #Hours.Minutes
	timeActivity_matrix = False
	behaviour = agent.behaviour

	if agent.type == 'professor':
		if time < behaviour['arriveTime']:
			timeActivity_matrix = [8.0, 0, 0, 0, 0, 0, 0]
		elif behaviour['meetingTime'] >= time >= behaviour['arriveTime']:
			if agent.model.occupantsValues == False:
				timeActivity_matrix = [0.30, 1.00, 0.10, 0.10, 0, 0, 0]
			else:
				timeActivity_matrix = [0.02, 1.00, 0.10, 0.10, 0, 0, 0]
		elif (behaviour['meetingTime']+0.9) >= time >= behaviour['meetingTime']:
			timeActivity_matrix = [0, 1.00, 0.10, 0.10, 0.10, 0, 0]
		elif behaviour['lunchTime'] >= time >= (behaviour['meetingTime']+0.9):
			timeActivity_matrix = [0, 1.00, 0.10, 0.10, 0, 0, 0]
		elif behaviour['backLunchTime']  >= time >= behaviour['lunchTime']:
			timeActivity_matrix = [0, 0.10, 0, 0, 0.05, 1.0, 0]
		elif behaviour['classTime'] >= time >= behaviour['backLunchTime']:
			timeActivity_matrix = [0, 0.30, 0.10, 0.10, 0, 0.1, 0]
		elif (behaviour['classTime']+0.05) >= time >= behaviour['classTime']:
			timeActivity_matrix = [0, 1, 0.10, 0.10, 0, 0.1, 2.0]
		elif behaviour['leaveWorkTime'] >= time >= (behaviour['classTime']+0.05):
			timeActivity_matrix = [0, 0.3, 0.10, 0.10, 0, 0, 0]
		elif time >= behaviour['leaveWorkTime']:
			if agent.model.occupantsValues == False:
				timeActivity_matrix = [5, 0.3, 0.10, 0.10, 0, 0, 0]
			else:
				timeActivity_matrix = [5, 0.02, 0.10, 0.10, 0, 0, 0]
		return timeActivity_matrix

	elif agent.type == 'researchers':
		if time < behaviour['arriveTime']:
			timeActivity_matrix = [8.0, 0, 0, 0, 0]
		elif behaviour['lunchTime'] >= time >= behaviour['arriveTime']:
			if agent.model.occupantsValues == False:
				timeActivity_matrix = [0.30, 1.00, 0.10, 0.10, 0]
			else:
				timeActivity_matrix = [0.02, 1.00, 0.10, 0.10, 0]
		elif behaviour['backLunchTime']  >= time >= behaviour['lunchTime']:
			timeActivity_matrix = [0, 0.05, 0, 0, 1.0]
		elif behaviour['leaveWorkTime'] >= time >= behaviour['backLunchTime']:
			timeActivity_matrix = [0, 1.00, 0.10, 0.10, 0.1]
		elif time >= behaviour['leaveWorkTime']:
			if agent.model.occupantsValues == False:
				timeActivity_matrix = [5, 0.30, 0.10, 0.10, 0]
			else:
				timeActivity_matrix = [5, 0.02, 0.10, 0.10, 0]
		return timeActivity_matrix

	elif agent.type == 'studients':
		if time < behaviour['arriveTime']:
			timeActivity_matrix = [13.0, 0]
		elif (behaviour['leaveWorkTime']) >= time >= behaviour['arriveTime']:
			timeActivity_matrix = [0.01, 2]
		elif time >= behaviour['leaveWorkTime']:
			timeActivity_matrix = [10, 0.01]
		return timeActivity_matrix

	else:
		return timeActivity_matrix

