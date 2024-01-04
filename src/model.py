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

    def __init__(self, config_filepath) -> None:
        super().__init__()

        with open(config_filepath) as file:
            config = json.load(file)

        self.width = config["width"]
        self.height = config["height"]

        self.max_agents_per_cell = config["max_agents_per_cell"]

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

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)

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

        for agent in config["initial_population"]:
            self._init_population(globals()[agent], config["initial_population"][agent])

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
        self.schedule.step()
        self.datacollector.collect(self)

    #     self.remove_redundant_agents(self.max_agents_per_cell)

    # def remove_redundant_agents(self, max_agents_per_cell):
    #     for cell_content in self.grid.coord_iter():
    #         cell_agents, cords = cell_content
    #         if len(cell_agents) > max_agents_per_cell:
    #             for agent in cell_agents[max_agents_per_cell:]:
    #                 if isinstance(agent, SeaTurtle):
    #                     continue
    #                 self.grid.remove_agent(agent)
    #                 self.schedule.remove(agent)
