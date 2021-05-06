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

    def __init__(self, population=8000, width=100, height=100):
        """
        Create a new model.

        Args:
            population: Number of available land
            width, height: Size of the space.
        """
        self.population = population
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        self.make_agents()
        self.running = True

    def make_agents(self):
        """
        Create self.population agents, with random positions and starting headings.
        """
        # Get some positions on the grid
        pos = np.array([(x, y) for x in range(0, self.space.width) for y in range(0, self.space.height)])
        # Choose population from the grid
        new_pos = pos[np.random.choice(pos.shape[0], self.population, replace=False), :]
        for i in range(self.population):
            farmer = Farmer(i, self, new_pos[i])
            self.space.place_agent(farmer, new_pos[i])
            self.schedule.add(farmer)

    def step(self):
        self.schedule.step()
