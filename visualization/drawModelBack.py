from collections import defaultdict
from mesa.visualization.ModularVisualization import VisualizationElement
from model.model import CESBAModel
import numpy as np
from agents.occupant import Occupant

class MapVisualization(VisualizationElement):
 
    local_includes = ["drawModelFront.js"]
    package_includes = ["Chart.min.js"]

    portrayal_method = None  # Portrayal function
    canvas_width = 500
    canvas_height = 500

    def __init__(self, portrayal_method,  cellW, cellH,canvas_width=500, canvas_height=500):
        self.portrayal_method = portrayal_method
        self.grid_width = cellW
        self.grid_height = cellH
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        new_element = ("new CanvasModule({}, {}, {}, {})"
            .format(self.canvas_width, self.canvas_height,
                self.grid_width, self.grid_height ))

        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        grid_state = defaultdict(list)
        for x in range(model.grid.width):
            for y in range(model.grid.height):
                cell_objects = model.grid.get_cell_list_contents([(x, y)])
                for obj in cell_objects:
                    portrayal = self.portrayal_method(obj)
                    if portrayal:
                        portrayal["x"] = x
                        portrayal["y"] = y
                        grid_state[portrayal["Layer"]].append(portrayal)

        offSet_Walls = 30
        for wall in model.Walls:
            JSON_Wall = {"x":wall.x,
                         "y": wall.y
            }
            grid_state[offSet_Walls].append(JSON_Wall)
        return grid_state

class GraphVisualization(VisualizationElement):

    package_includes = ["Chart.min.js"]
    local_includes = ["visualization/drawModelFront.js", "lib/canvasjs.min.js"]

    def __init__(self):
        new_element = "new GraphVisualization()"
        new_element = new_element.format()
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        data = []
        clock = 0
        day = model.clock.day
        agentsBurned = 0
        if model.NStep != 0:
            clock = model.clock.clock
        for agent in model.agents:
            if agent.dead != False:
                #print(agent.unique_id, "MUERTO:", agent.dead)
                agentsBurned = agentsBurned + 1

        data.append(day)
        data.append(clock)
        data.append(agentsBurned)
        
        return data