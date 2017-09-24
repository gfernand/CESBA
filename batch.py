from mesa.visualization.ModularVisualization import ModularServer
from mesa.batchrunner import BatchRunner
from model.model import CESBAModel
from model.time import Time
from mesa.datacollection import DataCollector

parameters = {"width": 99,
              "height": 24}

batch = BatchRunner(CESBAModel,
                        parameters,
                        iterations= 1,
                        max_steps = 10,
                        model_reporters={"Step": lambda m: m.NStep},
                        agent_reporters={"Pos": lambda a: a.pos if not isinstance(a, Time) else -1,})
batch.run_all()

model_step = batch.get_model_vars_dataframe()
print(model_step)
print("===============================================")
agent_pos = batch.get_agent_vars_dataframe()
print(agent_pos)
model_step.to_json('/home/guillermo/Escritorio/model.json')
agent_pos.to_json('/home/guillermo/Escritorio/dataframe.json')