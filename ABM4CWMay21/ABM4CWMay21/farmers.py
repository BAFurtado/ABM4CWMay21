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

    def __init__(self, unique_id, model, pos, productivity=1):
        """
        Create a new farmer.
        Args:
            unique_id: Unique agent identifyer.
            pos: Starting position
            model: Simulation object
        """
        super().__init__(unique_id, model)
        self.model = model
        self.pos = np.array(pos)
        # Productivity is price at the market minus cost of production (positive)
        self.productivity = productivity

    def get_empties(self, neighbors):
        occupied_pos = [(n.pos[0], n.pos[1]) for n in neighbors]
        empties = list()
        for x in range(self.pos[0] - self.model.vision, self.pos[0] + self.model.vision):
            for y in range(self.pos[1] - self.model.vision, self.pos[1] + self.model.vision):
                if (x != self.pos[0]) and (y != self.pos[1]):
                    pos = self.model.space.torus_adj((x, y))
                    if pos not in occupied_pos:
                        empties.append(pos)
        return empties

    def current_income(self):
        return self.productivity - self.model.space.get_distance(self.pos, self.model.space.center)

    def step(self):
        """
        Make decisions
        """
        # Get closest available position
        neighbors = self.model.space.get_neighbors(self.pos, self.model.vision, False)
        # Calculating neighborhood based on integers for positions, radius=2
        empties = self.get_empties(neighbors)
        current = self.current_income()
        # If more profitable move
        if empties:
            new_pos = max(empties, key=lambda f: self.productivity - self.model.space.get_distance(f, self.pos))
            new_income = self.productivity - self.model.space.get_distance(new_pos, self.pos)
            if new_income > current:
                self.model.space.move_agent(self, new_pos)
                return
        if current > 0:
            return
        self.model.space.remove_agent(self)
        self.model.schedule.remove(self)
        self.model.make_agents(n=1)

