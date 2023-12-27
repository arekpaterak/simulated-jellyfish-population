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
    """

    def __init__(self, unique_id, position, model, density=0.5, moore=True):
        super().__init__(unique_id, position, model, moore)
        self.density = density
        self.time_to_grow = self.model.plankton_time_to_grow
        self.grow_probability = self.model.plankton_grow_probability

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

        ### Jesli wiecej niz 4 zajete pola w sasiedztwie - nie rozmnaża się
        neighborhood = list(self.model.grid.get_neighborhood(
            self.position, self.moore, include_center=False, radius=1
        ))
        num_agents = len([1 for position in neighborhood if self.model.grid.get_cell_list_contents([position])])
        if num_agents > self.model.plankton_empty_cells_to_reproduce:
            return

        new_position = self.random.choice(
            self.model.grid.get_neighborhood(self.position, self.moore, False)
        )
        if self.model.grid.is_cell_empty(new_position):
            plankton = Plankton(self.model.next_id(), new_position, self.model)
            self.model.grid.place_agent(plankton, new_position)
            self.model.schedule.add(plankton)

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
