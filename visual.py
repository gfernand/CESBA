from mesa.visualization.ModularVisualization import ModularServer
from model.model import CESBAModel
from visualization.drawModelBack import MapVisualization
from visualization.drawModelBack import GraphVisualization

def occupancyVisualization(agent):
    
    json = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.5}

    if agent.unique_id >2999:
    	json = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    if agent.unique_id <2999:             
        if agent.dead == True:
            json = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "black",
                     "r": 0.8}
        elif agent.oldMan == True:
            json = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "pink",
                     "r": 0.5}
        elif agent.family == 1:
            if agent.child == True:
                json = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "pink",
                     "r": 0.5}
            elif agent.parent == True:
                json = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "brown",
                     "r": 0.5}
            else:
                json = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "yellow",
                     "r": 0.5}
        elif agent.family == 2:
            if agent.child == True:
                json = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "pink",
                     "r": 0.8}
            elif agent.parent == True:
                json = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "brown",
                     "r": 0.8}
            else:
                json = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "purple",
                     "r": 0.8}

    return json


mapVisualization = MapVisualization(occupancyVisualization, 100, 25, 1200, 600)

graphVisualization = GraphVisualization()

server = ModularServer(CESBAModel,
                       [mapVisualization, graphVisualization],
                       "CESBA Model",
                       99, 24, None)

server.port = 8882
server.launch()