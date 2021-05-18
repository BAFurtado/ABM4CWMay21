"""
A simple example of von Thünen's Isolated State idea
=============================================================
Based on a Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""

import numpy as np

from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation

from .farmers import Farmer


class Simulation(Model):
    """
    The simulation model itself. Handles agent creation, placement and scheduling.
    """

    def __init__(self, population, width, height, vision, products):
        """
        Create a new model.

        Args:
            population: Number of available land
            width, height: Size of the space.
        """
        super().__init__(self)
        self.population = population
        self.vision = vision
        self.products = products
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, False)
        self.center = int(width/2), int(height/2)
        self.ids = 0
        self.make_agents()
        self.running = True
        self.market = list()

    def make_agents(self, n=None):
        """
        Create self.population agents, with random positions and starting headings.
        """
        if not n:
            n = self.population
        types = np.random.choice(list(self.products), size=n, p=[self.products[k]['size'] for k in self.products])
        for i in range(n):
            farmer = Farmer(self.ids, self, None, self.products[types[i]],
                            self.products[types[i]]['productivity'],
                            self.products[types[i]]['transport'],
                            self.products[types[i]]['color'])
            self.grid.position_agent(farmer, 'random')
            self.schedule.add(farmer)
            self.ids += 1

    def center(self):
        return int(self.grid.width/2), int(self.grid.height/2)

    def get_distance(self, pos_1: (int, int), pos_2: (int, int)) -> float:
        """ Get the distance between two point, accounting for toroidal space.

        Args:
            pos_1, pos_2: Coordinate tuples for both points.

        """
        x1, y1 = pos_1
        x2, y2 = pos_2

        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        if self.grid.torus:
            dx = min(dx, self.grid.width - dx)
            dy = min(dy, self.grid.height - dy)
        return np.sqrt(dx * dx + dy * dy)

    def step(self):
        # Agents steps
        self.schedule.step()

        # Bidding for empty places. Model step
        on_the_market_land = list(set(x[1] for x in self.market))
        on_the_market_land.sort(key=lambda l: self.get_distance(l, self.center))

        for empty in on_the_market_land:
            bidders = [b for b in self.market if b[1] == empty]
            if bidders:
                winner = max(bidders, key=lambda b: b[2])
                self.grid.move_agent(winner[0], winner[1])
                # self.market.remove((winner[0], winner[1], winner[2]))
        self.market = list()
