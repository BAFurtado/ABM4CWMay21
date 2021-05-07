"""
A simple example of von Thünen's Isolated State idea
=============================================================
Based on a Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""

import numpy as np

from mesa import Model
from mesa.space import ContinuousSpace
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
        self.space = ContinuousSpace(width, height, True)
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
        # Get some positions on the grid
        pos = np.array([(x, y) for x in range(0, self.space.width) for y in range(0, self.space.height)])
        # Choose population from the grid
        new_pos = pos[np.random.choice(pos.shape[0], n, replace=False), :]
        types = np.random.choice(list(self.products), size=n, p=[self.products[k]['size'] for k in self.products])
        for i in range(n):
            farmer = Farmer(self.ids, self, new_pos[i], self.products[types[i]],
                            self.products[types[i]]['productivity'],
                            self.products[types[i]]['color'])
            self.space.place_agent(farmer, new_pos[i])
            self.schedule.add(farmer)
            self.ids += 1

    def step(self):
        # Agents steps
        self.schedule.step()
        # Bidding for empty places
        on_the_market_land = list(set(x[1] for x in self.market))
        on_the_market_land.sort(key=lambda l: self.space.get_distance(l, self.space.center))
        for empty in on_the_market_land:
            bidders = [b for b in self.market if b[1] == empty]
            if bidders:
                winner = max(bidders, key=lambda b: b[2])
                self.space.move_agent(winner[0], winner[1])
                self.market.remove((winner[0], winner[1], winner[2]))
        self.market = list()
