import mesa

from .base import BaseSeaAgent
from .food_source import Plankton

Position = tuple[int, int]


class Animal(BaseSeaAgent):
    """
    Base class for all animals in the simulation.
    """

    def __init__(
        self, unique_id: int, position: Position, model: mesa.Model, moore: bool = True
    ) -> None:
        super().__init__(unique_id, position, model, moore)


class MovingAnimal(BaseSeaAgent):
    """
    Class implementing random walker methods in a generalized manner.

    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    def __init__(
        self,
        unique_id: int,
        position: Position,
        model: mesa.Model,
        moore: bool = True,
    ) -> None:
        super().__init__(unique_id, position, model, moore)

    def random_move(self, radius: int = 1) -> None:
        """
        Step one cell in any allowable direction.
        """
        next_position = self._find_empty_cell_in_neighborhood(radius)

        self.model.grid.move_agent(self, next_position)

    def _find_empty_cell_in_neighborhood(self, radius: int = 1) -> Position:
        """
        Find an empty cell in the neighborhood and return its coordinates.
        """
        neighborhood = self.model.grid.get_neighborhood(
            self.position, self.moore, include_center=True, radius=radius
        )

        next_position = self.random.choice(neighborhood)
        cell_agents = self.model.grid.get_cell_list_contents([next_position])
        while (
            not (
                self.model.grid.is_cell_empty(next_position)
                or all([agent.is_food_source() for agent in cell_agents])
            )
            or next_position == self.position
        ):
            next_position = self.random.choice(neighborhood)
            cell_agents = self.model.grid.get_cell_list_contents([next_position])

        return next_position


class JellyfishMedusa(MovingAnimal):
    """
    An agent representing a swiming, mature jellyfish.

    Eats plankton and small fish. Reproduces sexually many times in the lifespan when fully grown. Can be eaten by sea turtles. Dies when it runs out of energy.

    Reproduction depends on:
    - having a mating partner in the proximity
    - a parameter that determines its probability
    - a parameter that determines the number of offspring
    """

    def __init__(self, unique_id, position, model, moore=True, energy=None):
        super().__init__(unique_id, position, model, moore)
        self.energy = energy
        self.time_to_grow = self.model.jellyfish_medusa_time_to_grow

        # TODO: think if we need males and females

        raise NotImplementedError()

    def step(self):
        self.random_move()

        self.energy -= 1
        self.time_to_grow -= 1

        # TODO: eat plankton or small fish

        if self.energy < 0:
            self.die()
            return

        if self.is_mature():
            partners = self._find_partners()

            # TODO: adjust reproduction conditions
            if (
                partners
                and self.random.random()
                < self.model.jellyfish_medusa_reproduce_probability
            ):
                self._reproduce()

    def _eat(self):
        raise NotImplementedError()

    def _eat_plankton(self):
        neighbors = self.model.grid.get_neighbors(
            self.position, self.moore, include_center=True
        )
        potential_food = [agent for agent in neighbors if isinstance(agent, Plankton)]
        if potential_food:
            plankton: Plankton = self.random.choice(potential_food)
            energy_gain = self.model.fish_gain_from_food * plankton.density
            plankton.die()
            self.energy += energy_gain

    def _eat_fish(self):
        raise NotImplementedError()

    def is_mature(self):
        return self.time_to_grow < 0

    def _find_partners(self):
        neighbors = self.model.grid.get_neighbors(
            self.position, self.moore, include_center=True
        )
        potential_partners = [
            agent
            for agent in neighbors
            if isinstance(agent, self.__class__) and agent is not self
        ]
        partners = [partner for partner in potential_partners if partner.is_mature()]
        return partners

    def _reproduce(self):
        self.energy /= 2
        # TODO: make more larvae than just one
        child = JellyfishLarva(
            self.model.next_id(), self.position, self.model, self.moore, self.energy
        )
        self.model.grid.place_agent(child, self.position)
        self.model.schedule.add(child)

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)


class JellyfishLarva(MovingAnimal):
    """
    An agent representing a jellyfish larva.

    Moves, eats plankton and transforms into a polyp after growing up enough.
    """

    def __init__(self, unique_id, position, model, moore=True):
        super().__init__(unique_id, position, model, moore)
        self.time_to_grow = self.model.jellyfish_larva_time_to_grow

    def step(self):
        self.random_move()

        self.time_to_grow -= 1
        if self.time_to_grow < 0:
            self.transform()
            return

        self._eat_plankton()

    def _eat(self):
        raise NotImplementedError()

    def _eat_plankton(self):
        neighbors = self.model.grid.get_neighbors(
            self.position, self.moore, include_center=True
        )
        potential_food = [agent for agent in neighbors if isinstance(agent, Plankton)]
        if potential_food:
            plankton: Plankton = self.random.choice(potential_food)
            energy_gain = self.model.fish_gain_from_food * plankton.density
            plankton.die()
            self.energy += energy_gain

    def transform(self):
        polyp = JellyfishPolyp(self.model.next_id(), self.position, self.model)
        self.model.grid.place_agent(polyp, self.position)
        self.model.schedule.add(polyp)

        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def die(self) -> None:
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)


class JellyfishPolyp(Animal):
    """
    An agent representing a jellyfish polyp.

    It can reproduce asexually via strobilation. It doesn't move. It isn't eaten by anything.
    """

    def __init__(self, unique_id, position, model, moore=True):
        super().__init__(unique_id, position, model, moore)
        self.time_to_grow = self.model.jellyfish_polyp_time_to_grow

    def step(self):
        self.time_to_grow -= 1

        self._eat_plankton()

        if self.time_to_grow < 0:
            self._strobilate()

    def _eat(self):
        raise NotImplementedError()

    def _eat_plankton(self):
        neighbors = self.model.grid.get_neighbors(
            self.position, self.moore, include_center=True
        )
        potential_food = [agent for agent in neighbors if isinstance(agent, Plankton)]
        if potential_food:
            plankton: Plankton = self.random.choice(potential_food)
            energy_gain = self.model.fish_gain_from_food * plankton.density
            plankton.die()
            self.energy += energy_gain

    def _strobilate(self):
        raise NotImplementedError()


class SeaTurtle(MovingAnimal):
    """
    A representative jellyfish predator in the model.

    Eats jellyfish in their medusa phase. Lives so long that it doesn't die in the model. Its reproduction is not a part of the model.
    """

    def __init__(self, unique_id, position, model, moore=True, energy=None):
        super().__init__(unique_id, position, model, moore)

        raise NotImplementedError()

    def step(self):
        self.random_move()

        self._eat()

    def _eat(self):
        neighbors = self.model.grid.get_neighbors(
            self.position, self.moore, include_center=True
        )
        potential_preys = [
            agent for agent in neighbors if isinstance(agent, JellyfishMedusa)
        ]
        if potential_preys:
            prey: JellyfishMedusa = self.random.choice(potential_preys)
            prey.die()
            self.energy += self.model.sea_turtle_gain_from_food


class Fish(MovingAnimal):
    """
    An agent representing a fish. Main competitor of jellyfish for plankton.

    Eats plankton and jellyfish larvae. Reproduces sexually when mature. Dies when it runs out of energy.
    """

    def __init__(self, unique_id, position, model, moore=True, energy=None):
        super().__init__(unique_id, position, model, moore)
        self.energy = energy
        self.time_to_grow = self.model.fish_time_to_grow

        raise NotImplementedError()

    def step(self):
        self.random_move()

        self.energy -= 1
        self.time_to_grow -= 1

        if self.energy < 0:
            self.die()
            return

        self._eat()

        if self.is_mature():
            partners = self._find_partners()

            if (
                partners
                and self.random.random() < self.model.fish_reproduce_probability
            ):
                self._reproduce()

    def is_mature(self):
        return self.time_to_grow < 0

    def _eat(self):
        neighbors = self.model.grid.get_neighbors(
            self.position, self.moore, include_center=True
        )

        if self.is_mature():
            potential_preys = [
                agent for agent in neighbors if isinstance(agent, JellyfishLarva)
            ]
            if potential_preys:
                prey: JellyfishLarva = self.random.choice(potential_preys)
                prey.die()
                self.energy += self.model.fish_gain_from_food
                return

        potential_food = [agent for agent in neighbors if isinstance(agent, Plankton)]
        if potential_food:
            plankton: Plankton = self.random.choice(potential_food)
            energy_gain = self.model.fish_gain_from_food * plankton.density
            plankton.die()
            self.energy += energy_gain
            return

    def _find_partners(self):
        neighbors = self.model.grid.get_neighbors(
            self.position, self.moore, include_center=True
        )
        potential_partners = [
            agent
            for agent in neighbors
            if isinstance(agent, self.__class__) and agent is not self
        ]
        partners = [partner for partner in potential_partners if partner.is_mature()]
        return partners

    def _reproduce(self):
        self.energy /= 2
        fish_num = self.random.choices(
            [1, 2, 3, 4, 5], weights=[0.5, 0.25, 0.125, 0.07, 0.055], k=1
        )
        for i in range(fish_num):
            child = Fish(
                self.model.next_id(), self.position, self.model, self.moore, self.energy
            )
            self.model.grid.place_agent(child, self.position)
            self.model.schedule.add(child)

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
