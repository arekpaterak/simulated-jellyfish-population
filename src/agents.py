import random

import mesa

from random_walk import RandomWalker


# TODO: think generally about energy


class JellyfishMedusa(RandomWalker):
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

        cell = self.model.grid.get_cell_list_contents([self.position])

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
        potential_food = [
            agent for agent in neighbors if isinstance(agent, Plankton)
        ]
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


class JellyfishLarva(RandomWalker):
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
        potential_food = [
            agent for agent in neighbors if isinstance(agent, Plankton)
        ]
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


class JellyfishPolyp(mesa.Agent):
    """
    An agent representing a jellyfish polyp.

    It can reproduce asexually via strobilation. It doesn't move. It isn't eaten by anything.
    """

    def __init__(self, unique_id, position, model, moore=True):
        super().__init__(unique_id, model)
        self.position = position
        self.time_to_grow = self.model.jellyfish_polyp_time_to_grow
        self.moore = moore

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
        potential_food = [
            agent for agent in neighbors if isinstance(agent, Plankton)
        ]
        if potential_food:
            plankton: Plankton = self.random.choice(potential_food)
            energy_gain = self.model.fish_gain_from_food * plankton.density
            plankton.die()
            self.energy += energy_gain

    def _strobilate(self):
        raise NotImplementedError()


class SeaTurtle(RandomWalker):
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


class Fish(RandomWalker):
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

        potential_food = [
            agent for agent in neighbors if isinstance(agent, Plankton)
        ]
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
        fish_num = random.choices(
            [1, 2, 3, 4, 5],
            weights=[0.5, 0.25, 0.125, 0.07, 0.055],
            k=1
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


class Plankton(mesa.Agent):
    """
    An agent representing a plankton. Main food source for jellyfish and fish.
    Args:
        density (float): Plankton density, determines energy gain for agent which eats him
    """
    def __init__(self, unique_id, position, model, density=0.5, moore=True):
        super().__init__(unique_id, model)
        self.position = position
        self.moore = moore
        self.density = density
        self.time_to_grow = self.model.plankton_time_to_grow

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def step(self):
        """
        Plankton density grows at each step, when it reaches 1,
         new plankton agent appears at random neighbour grid cell
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
