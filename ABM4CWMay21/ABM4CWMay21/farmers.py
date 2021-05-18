import numpy as np

from mesa import Agent


class Farmer(Agent):
    """
    A farm agent.

    To the spirit of the simplest agent possible, farmers try only to survive.
    Agent (producer)'s Rule:
        At all times

        Income = Price - Cost - (transport * distance_to_market(x,y))

        if income above 0
            if available location higher income
                move
            stay
        leave town

    """

    def __init__(self, unique_id, model, pos, types, productivity, transport, color):
        """
        Create a new farmer.
        Args:
            unique_id: Unique agent identifyer.
            pos: Starting position
            model: Simulation object
        """
        super().__init__(unique_id, model)
        self.model = model
        self.pos = pos
        # Productivity is price at the market minus cost of production (positive)
        self.types = types
        self.productivity = productivity
        self.transport = transport
        self.color = color

    def current_income(self):
        return self.productivity - self.model.get_distance(self.pos, self.model.center) * self.transport

    def step(self):
        """
        Make decisions
        """
        # Get closest available position
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True,
                                                        include_center=False, radius=self.model.vision)
        # Calculating neighborhood based on integers for positions, radius=2
        empties = self.model.grid.empties
        current = self.current_income()
        # If more profitable move
        if empties:
            new_pos = min(empties, key=lambda f: self.model.get_distance(f, self.model.center))
            new_income = self.productivity - self.model.get_distance(new_pos, self.model.center) * self.transport
            if new_income > current:
                self.model.market.append((self, new_pos, new_income))
                return
        if current > 0:
            return
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
        self.model.make_agents(n=1)

