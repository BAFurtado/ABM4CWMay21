from mesa.visualization.ModularVisualization import ModularServer

from .model import Simulation
from .SimpleContinuousModule import SimpleCanvas


def farm_draw(agent):
    return {"Shape": "circle", 'r': 2, "Filled": "true", "Color": "Red"}


town_canvas = SimpleCanvas(farm_draw, 500, 500)
model_params = {
    "population": 8000,
    "width": 100,
    "height": 100}

server = ModularServer(Simulation, [town_canvas], "Farmers", model_params)
