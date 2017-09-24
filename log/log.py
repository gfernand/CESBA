import csv
import json

class Log():

	def collectLog(self, agentsWorkingByStep, occupantsInRoomByStep, timeByStep):
		with open('results/example/agentsWorkingByTime.csv', 'w', newline='') as f:
			outPut = []
			outPut.append(['time', 'numberAgents'])
			for n in range(0, len(agentsWorkingByStep)):
				outPut.append([n*timeByStep, agentsWorkingByStep[n]])
			writer = csv.writer(f)
			writer.writerows(outPut)

		for k, v in occupantsInRoomByStep.items():
			with open('results/example/occupantsIn' + k + 'ByTime.csv', 'w', newline='') as f:
				outPut = []
				outPut.append(['time', 'numberAgents'])
				for n in range(0, len(agentsWorkingByStep)):
					outPut.append([n*timeByStep, v[n]])
				writer = csv.writer(f)
				writer.writerows(outPut)
