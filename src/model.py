import mesa

from .agents import *
from .scheduler import RandomActivationByTypeFiltered


class MarineEcosystem(mesa.Model):
    """
    A model of a whole environment in the simulation.
    """

    def __init__(
        self,
        width=20,
        height=20,
        initial_jellyfish_medusae=100,
        initial_jellyfish_polyps=50,
        initial_jellyfish_larvae=50,
        initial_sea_turtles=50,
        initial_fish=50,
        jellyfish_medusae_reproduce=0.04,
        jellyfish_polyps_reproduce=0.04,
        fish_reproduce=0.05,
        sea_turtles_gain_from_food=20,
        jellyfish_medusae_gain_from_food=20,
        jellyfish_polyps_gain_from_food=20,
        jellyfish_larvae_gain_from_food=20,
        fish_gain_from_food=20,
        # TODO: add parameters
    ) -> None:
        super().__init__()

        # TODO: assign parameters

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

        # TODO: initialise populations of agents

        self.running = True

    def _init_population(self, agent_type, size):
        """
        Create a new population of agents of a given type.
        """
        for i in range(size):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            energy = None  # TODO: assign energy

            agent = agent_type()  # TODO: pass parameters to agent constructor

            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

    def step(self):
        """
        Advance the model by one timestep.
        """
        self.schedule.step()
        self.datacollector.collect(self)
