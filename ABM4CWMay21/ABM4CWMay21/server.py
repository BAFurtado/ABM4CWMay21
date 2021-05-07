from mesa.visualization.ModularVisualization import ModularServer

from .model import Simulation
from .SimpleContinuousModule import SimpleCanvas

# Products: Name: productivity, size
full_size = 10
products = {'Dairy': {'productivity': 400, 'size': 1/10, 'color': 'Red'},
            'Crops': {'productivity': 150, 'size': 2/10, 'color': 'Blue'},
            'Grazing': {'productivity': 100, 'size': 1 - 3/10, 'color': 'Green'}}


def farm_draw(agent):
    return {"Shape": "circle", 'r': 2, "Filled": "true", "Color": agent.color}


town_canvas = SimpleCanvas(farm_draw, 500, 500)
model_params = {
    "population": 8000,
    "width": 100,
    "height": 100,
    'vision': 2,
    'products': products}

server = ModularServer(Simulation, [town_canvas], "Farmers", model_params)
