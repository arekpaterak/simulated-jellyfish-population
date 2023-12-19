import mesa

from .base import BaseSeaAgent


class FoodSource(BaseSeaAgent):
    """
    Base class for all food sources in the simulation.
    """

    def __init__(self, unique_id, position, model, moore=True) -> None:
        super().__init__(unique_id, position, model, moore)

    def is_food_source(self):
        return True


class Plankton(FoodSource):
    """
    An agent representing a plankton. Main food source for jellyfish and fish.
    Args:
        density (float): Plankton density, determines energy gain for agent which eats him
    """

    def __init__(self, unique_id, position, model, density=0.5, moore=True):
        super().__init__(unique_id, position, model, moore)
        self.density = density
        self.time_to_grow = self.model.plankton_time_to_grow

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def step(self):
        """
        Plankton density grows at each step, when it reaches 1, new plankton agent appears at random neighbour grid cell
        """
        self.time_to_grow -= 1
        self.density += 0.02
        if self.density > 1:
            self.grow()

    def grow(self):
        """
        Creates new plankton agent
        """
        raise NotImplementedError()
