import json
import mesa
from portrayals import agent_portrayal
from model import MarineEcosystem

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIGS_DIR = "configs"
CONFIG_FILE = "config.json"
CONFIG_FILE_PATH = f"{ROOT_DIR}/{CONFIGS_DIR}/{CONFIG_FILE}"

with open(CONFIG_FILE_PATH) as file:
    config = json.load(file)

grid = mesa.visualization.CanvasGrid(
    agent_portrayal,
    config["width"],
    config["height"],
    canvas_width=config["width"] * 8,
    canvas_height=config["height"] * 8,
)

chart = mesa.visualization.ChartModule(
    [
        {"Label": "Jellyfish Medusae", "Color": "#F999B7"},
        {"Label": "Jellyfish Larvae", "Color": "#F9C5D5"},
        {"Label": "Jellyfish Polyps", "Color": "#F2789F"},
        {"Label": "Sea Turtles", "Color": "green"},
        {"Label": "Fish", "Color": "gray"},
        {"Label": "Plankton", "Color": "yellowgreen"},
    ]
)

model_params = {
    "title": mesa.visualization.StaticText("Parameters:"),
    "initial_population_jellyfish_medusa": mesa.visualization.Slider(
        "Initial Jellyfish Medusae Population",
        config["initial_population"]["JellyfishMedusa"],
        0,
        500,
        10,
        description="xd",
    ),
    "initial_population_jellyfish_polyp": mesa.visualization.Slider(
        "Initial Jellyfish Polyps Population",
        config["initial_population"]["JellyfishPolyp"],
        0,
        100,
        10,
    ),
    "initial_population_jellyfish_larva": mesa.visualization.Slider(
        "Initial Jellyfish Larvae Population",
        config["initial_population"]["JellyfishLarva"],
        0,
        500,
        10,
    ),
    "initial_population_fish": mesa.visualization.Slider(
        "Initial Fish Population", config["initial_population"]["Fish"], 0, 500, 10
    ),
    "initial_population_plankton": mesa.visualization.Slider(
        "Initial Plankton Population",
        config["initial_population"]["Plankton"],
        0,
        1000,
        100,
    ),
    "initial_population_sea_turtle": mesa.visualization.Slider(
        "Initial Sea Turtles Population",
        config["initial_population"]["SeaTurtle"],
        0,
        10,
        1,
    ),
    "config_filepath": CONFIG_FILE_PATH,
}

server = mesa.visualization.ModularServer(
    model_cls=MarineEcosystem,
    model_params=model_params,
    visualization_elements=[grid, chart],
    name="Simulated Jellyfish Population",
)

server.port = 8521
