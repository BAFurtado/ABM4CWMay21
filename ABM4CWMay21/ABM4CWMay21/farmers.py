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

    def __init__(self, unique_id, model, pos, product=None):
        """
        Create a new farmer.
        Args:
            unique_id: Unique agent identifyer.
            pos: Starting position
            model: Simulation object
        """
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.product = product

    def step(self):
        """
        Make decisions
        """

        # Get closest available position
        # If more profitable move
        # else if positive stay
        # else leave model

        # new_pos =
        # self.model.space.move_agent(self, new_pos)
        pass
