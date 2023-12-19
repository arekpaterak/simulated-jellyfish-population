import mesa

from agents import *
from scheduler import RandomActivationByTypeFiltered


class MarineEcosystem(mesa.Model):
    """
    A model of a whole environment in the simulation.
    """

    def __init__(
        self,
        width: int = 20,
        height: int = 20,
        initial_jellyfish_medusa_population_size: int = 1000,
        initial_jellyfish_polyp_population_size: int = 100,
        initial_jellyfish_larva_population_size: int = 100,
        initial_sea_turtle_population_size: int = 100,
        initial_fish_population_size: int = 1000,
        jellyfish_medusa_time_to_grow: int = 15,
        jellyfish_medusa_gain_from_food: int = 20,
        jellyfish_medusa_reproduction_probability: float = 0.05,
        jellyfish_medusa_reproduction_rate: int = 5,  # larvae per day
        jellyfish_polyp_time_to_grow: int = 30,
        jellyfish_polyp_gain_from_food: int = 20,
        jellyfish_polyp_strobilation_rate: int = 1,  # medusae per day
        jellyfish_larva_time_to_grow: int = 5,
        jellyfish_larva_gain_from_food: int = 20,
        fish_time_to_grow: int = 90,  # days
        fish_gain_from_food: int = 20,
        fish_reproduction_probability: float = 0.05,
        sea_turtle_gain_from_food: int = 20,
        plantkton_time_to_grow: int = 50
        # TODO: add parameters
    ) -> None:
        super().__init__()

        # TODO: assign parameters

        self.jellyfish_larva_time_to_grow = jellyfish_larva_time_to_grow

        self.jellyfish_polyp_time_to_grow = jellyfish_polyp_time_to_grow

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(width, height, torus=True)

        self.datacollector = mesa.datacollection.DataCollector(
            {
                "Jellyfish Medusae": lambda m: m.schedule.get_type_count(
                    JellyfishMedusa
                ),
                "Jellyfish Polyps": lambda m: m.schedule.get_type_count(JellyfishPolyp),
                "Jellyfish Larvae": lambda m: m.schedule.get_type_count(JellyfishLarva),
                "Sea Turtles": lambda m: m.schedule.get_type_count(SeaTurtle),
                "Fish": lambda m: m.schedule.get_type_count(Fish),
            }
        )

        self._init_population(JellyfishLarva, 10)

        self.running = True

    def _init_population(self, agent_type, size):
        """
        Create a new population of agents of a given type.
        """
        for _ in range(size):
            x = self.random.randrange(100)
            y = self.random.randrange(100)

            energy = None  # TODO: assign energy

            agent = agent_type(self.next_id(), (x, y), self)

            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

    def step(self):
        """
        Advance the model by one timestep.
        """
        self.schedule.step()
        self.datacollector.collect(self)
