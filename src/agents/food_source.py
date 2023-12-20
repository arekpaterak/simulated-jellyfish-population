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

    def __init__(self, unique_id, position, model, density=0, moore=True):
        super().__init__(unique_id, position, model, moore)
        self.density = density
        self.time_to_grow = self.model.plankton_time_to_grow
        self.grow_probability = self.model.plankton_grow_probability

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def step(self):
        """
        Plankton density grows at each step, when it reaches 1, new plankton agent appears at random neighbour grid cell
        """
        self.time_to_grow -= 1
        if self.time_to_grow <= 0 and self.grow_probability < self.random.random():
            self.grow()

    def grow(self):
        """
        Creates new plankton agent
        """
        plankton = Plankton(self.model.next_id(), self.position, self.model)
        new_position = (
            max(min(self.position[0] + self.random.choice([-1, 0, 1]), self.model.width - 1), 0),
            max(min(self.position[1] + self.random.choice([-1, 0, 1]), self.model.height - 1), 0)
        )
        self.model.grid.place_agent(plankton, new_position)
        self.model.schedule.add(plankton)

