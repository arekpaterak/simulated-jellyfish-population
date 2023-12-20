import mesa

from agents.food_source import *
from agents.animals import *
import json
from scheduler import RandomActivationByTypeFiltered
import time

class MarineEcosystem(mesa.Model):
    """
    A model of a whole environment in the simulation.
    """

    def __init__(self) -> None:
        super().__init__()

        with open("config.json") as file:
            config = json.load(file)

        self.width = config["width"]
        self.height = config["height"]

        self.jellyfish_larva_time_to_grow = config["jellyfish_larva"]["time_to_grow"]

        self.jellyfish_polyp_time_to_grow = config["jellyfish_polyp"]["time_to_grow"]
        self.jellyfish_polyp_gain_from_food = config['jellyfish_polyp']['gain_from_food']

        self.jellyfish_medusa_time_to_grow = config["jellyfish_medusa"]["time_to_grow"]
        self.jellyfish_medusa_reproduce_probability = config['jellyfish_medusa']['reproduce_probability']
        self.jellyfish_medusa_reproduce_rate = config['jellyfish_medusa']['reproduce_rate']
        self.jellyfish_medusa_gain_from_food = config['jellyfish_medusa']['gain_from_food']

        self.plankton_time_to_grow = config["plankton"]["time_to_grow"]
        self.plankton_grow_probability = config['plankton']["grow_probability"]

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)

        self.datacollector = mesa.datacollection.DataCollector(
            {
                "Jellyfish Medusa": lambda m: m.schedule.get_type_count(JellyfishMedusa),
                "Jellyfish Polyps": lambda m: m.schedule.get_type_count(JellyfishPolyp),
                "Jellyfish Larvae": lambda m: m.schedule.get_type_count(JellyfishLarva),
                "Sea Turtles": lambda m: m.schedule.get_type_count(SeaTurtle),
                "Fish": lambda m: m.schedule.get_type_count(Fish),
            }
        )

        for agent in config["initial_population"]:
            self._init_population(globals()[agent], config["initial_population"][agent])

        self.running = True

    def _init_population(self, agent_type, size):
        """
        Create a new population of agents of a given type.
        """
        for i in range(size):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            agent = agent_type(self.next_id(), (x, y), self)

            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

    def step(self):
        """
        Advance the model by one timestep.
        """
        self.schedule.step()
        self.datacollector.collect(self)
        self.remove_redundant_agents()

    def remove_redundant_agents(self, max_agents_per_cell=2):
        for cell_content in self.grid.coord_iter():
            cell_agents, cords = cell_content
            if len(cell_agents) > max_agents_per_cell:
                for agent in cell_agents[max_agents_per_cell:]:
                    self.grid.remove_agent(agent)
                    self.schedule.remove(agent)
