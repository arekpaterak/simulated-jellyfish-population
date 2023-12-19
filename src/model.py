import mesa
import json
from agents import *
from scheduler import RandomActivationByTypeFiltered


class MarineEcosystem(mesa.Model):
    """
    A model of a whole environment in the simulation.
    """

    def __init__(self) -> None:
        super().__init__()

        with open('config.json') as file:
            config = json.load(file)

        try:
            width = config['width']
            height = config['height']
        except ValueError:
            raise ValueError('Incorrect or missing grid size parameters')

        self.jellyfish_larva_time_to_grow = config['jellyfish_larva']['time_to_grow']
        self.jellyfish_polyp_time_to_grow = config['jellyfish_polyp']['time_to_grow']

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(width, height, torus=True)

        self.datacollector = mesa.datacollection.DataCollector(
            {
                "Jellyfish Medusae": lambda m: m.schedule.get_type_count(JellyfishMedusa),
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
        for i in range(size):
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
