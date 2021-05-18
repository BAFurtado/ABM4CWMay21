
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from .model import Simulation

# Products: Name: productivity, size
full_size = 10
products = {'Dairy': {'productivity': 300, 'size': 2/10, 'color': 'Red', 'transport': 1},
            'Crops': {'productivity': 200,
                      'size': 3/10, 'color': 'Blue', 'transport': 2},
            'Grazing': {'productivity': 150, 'size': 1 - 5/10, 'color': 'Green', 'transport': 3}}


def farm_draw(agent):
    return {"Shape": "rect", 'w': 1, 'h': 1, 'Layer': 0,
            "Filled": "true",
            "Color": agent.color, 'x': agent.pos[0], 'y': agent.pos[1]}


town_canvas = CanvasGrid(farm_draw, 20, 20, 500, 500)
model_params = {
    "population": 100,
    "width": 20,
    "height": 20,
    'vision': 4,
    'products': products}

server = ModularServer(Simulation, [town_canvas], "Farmers", model_params)
