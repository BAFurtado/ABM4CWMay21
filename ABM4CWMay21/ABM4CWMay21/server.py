from mesa.visualization.ModularVisualization import ModularServer

from .model import Simulation
from .SimpleContinuousModule import SimpleCanvas

# Products: Name: productivity, size
full_size = 10
products = {'Dairy': {'productivity': 300, 'size': 2/10, 'color': 'Red', 'transport': 1},
            'Crops': {'productivity': 200, 'size': 3/10, 'color': 'Blue', 'transport': 2},
            'Grazing': {'productivity': 150, 'size': 1 - 5/10, 'color': 'Green', 'transport': 3}}


def farm_draw(agent):
    return {"Shape": "circle", 'r': 2, "Filled": "true", "Color": agent.color}


town_canvas = SimpleCanvas(farm_draw, 500, 500)
model_params = {
    "population": 2000,
    "width": 70,
    "height": 70,
    'vision': 7,
    'products': products}

server = ModularServer(Simulation, [town_canvas], "Farmers", model_params)
