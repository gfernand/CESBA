from mesa.visualization.ModularVisualization import ModularServer
from model.model import SOBAModel
from visualization.drawModelBack import MapVisualization
from visualization.drawModelBack import GraphVisualization

def occupancyVisualization(agent):
    
    json = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.5}

    return json


mapVisualization = MapVisualization(occupancyVisualization, 18, 6, 1200, 600)

graphVisualization = GraphVisualization()

server = ModularServer(SOBAModel,
                       [mapVisualization, graphVisualization],
                       "GreenSOBA Model",
                       22, 22, None)

server.port = 8882
server.launch()