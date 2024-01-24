import math
from random import Random

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

    def __init__(self, config_filepath, **kwargs) -> None:
        super().__init__()

        with open(config_filepath) as file:
            config = json.load(file)

        self.width = config["width"]
        self.height = config["height"]

        self.jellyfish_larva_time_to_grow = config["jellyfish_larva"]["time_to_grow"]

        self.jellyfish_polyp_time_to_grow = config["jellyfish_polyp"]["time_to_grow"]
        self.jellyfish_polyp_gain_from_food = config["jellyfish_polyp"][
            "gain_from_food"
        ]

        self.jellyfish_medusa_time_to_grow = config["jellyfish_medusa"]["time_to_grow"]
        self.jellyfish_medusa_reproduce_probability = config["jellyfish_medusa"][
            "reproduce_probability"
        ]
        self.jellyfish_medusa_reproduce_rate = config["jellyfish_medusa"][
            "reproduce_rate"
        ]
        self.jellyfish_medusa_gain_from_food = config["jellyfish_medusa"][
            "gain_from_food"
        ]
        self.jellyfish_empty_cells_to_reproduce = config["jellyfish_medusa"][
            "max_non_empty_neighbour_cells_to_reproduce"
        ]

        self.plankton_time_to_grow = config["plankton"]["time_to_grow"]
        self.plankton_grow_probability = config["plankton"]["grow_probability"]
        self.plankton_empty_cells_to_reproduce = config["plankton"][
            "max_non_empty_neighbour_cells_to_reproduce"
        ]

        self.fish_time_to_grow = config["fish"]["time_to_grow"]
        self.fish_gain_from_food = config["fish"]["gain_from_food"]
        self.fish_reproduce_probability = config["fish"]["reproduction_probability"]

        self.max_allowed_temperature = config[
            "max_allowed_temperature"
        ]  # max value of slider
        self.min_allowed_temperature = config[
            "min_allowed_temperature"
        ]  # min value of slider

        self.max_used_temperature = config["max_used_temperature"]  # slider
        self.min_used_temperature = config["min_used_temperature"]  # slider
        self.temperature = None

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)
        self.current_step = 0

        self.datacollector = mesa.datacollection.DataCollector(
            {
                "Jellyfish Medusae": lambda m: m.schedule.get_type_count(
                    JellyfishMedusa
                ),
                "Jellyfish Polyps": lambda m: m.schedule.get_type_count(JellyfishPolyp),
                "Jellyfish Larvae": lambda m: m.schedule.get_type_count(JellyfishLarva),
                "Sea Turtles": lambda m: m.schedule.get_type_count(SeaTurtle),
                "Fish": lambda m: m.schedule.get_type_count(Fish),
                "Plankton": lambda m: m.schedule.get_type_count(Plankton),
            }
        )

        # for agent in config["initial_population"]:
        #     self._init_population(globals()[agent], config["initial_population"][agent])

        self._init_population(
            JellyfishMedusa, kwargs["initial_population_jellyfish_medusa"]
        )
        self._init_population(
            JellyfishPolyp, kwargs["initial_population_jellyfish_polyp"]
        )
        self._init_population(
            JellyfishLarva, kwargs["initial_population_jellyfish_larva"]
        )
        self._init_population(SeaTurtle, kwargs["initial_population_sea_turtle"])
        self._init_population(Fish, kwargs["initial_population_fish"])
        self._init_population(Plankton, kwargs["initial_population_plankton"])

        self.running = True

    def _init_population(self, agent_type, size):
        """
        Create a new population of agents of a given type.
        """
        for _ in range(size):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            agent = agent_type(self.next_id(), (x, y), self)

            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

    def step(self):
        """
        Advance the model by one timestep.
        """

        self.current_step += 1
        self.schedule.step()
        self.datacollector.collect(self)

        self.temperature = (
            float(self.max_used_temperature - self.min_used_temperature) / 2
        )
        self.temperature = self.temperature * math.sin(
            2 * math.pi * self.current_step / 365
        )
        self.temperature = (
            self.temperature
            + float(self.max_used_temperature + self.min_used_temperature) / 2
        )

        for _ in range(5):
            if self.plankton_reproduction_probability() > 0.0:
                x = self.random.randrange(self.width)
                y = self.random.randrange(self.height)
                plankton = Plankton(self.next_id(), (x, y), self)
                self.grid.place_agent(plankton, (x, y))
                self.schedule.add(plankton)

    def plankton_reproduction_probability(self):
        return math.sin(
            math.pi
            / 2
            * self.temperature
            / (self.max_allowed_temperature - self.min_allowed_temperature)
        )
