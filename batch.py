from mesa.visualization.ModularVisualization import ModularServer
from mesa.batchrunner import BatchRunner
from model.model import SOBAModel

parameters = {"width": 22,
              "height": 22,
              "modelWay": range(0, 3)}

batch = BatchRunner(SOBAModel,
                        parameters,
                        iterations= 1,
                        max_steps = 1000000)
batch.run_all()
