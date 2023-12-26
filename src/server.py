import json
import mesa
from portrayals import agent_portrayal
from mesa.visualization.ModularVisualization import ModularServer
from model import MarineEcosystem

import os


CONFIGS_DIR = "configs"
CONFIG_FILE = "config.json"
CONFIG_FILE_PATH = os.path.join(CONFIGS_DIR, CONFIG_FILE)

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

server = ModularServer(
    model_cls=MarineEcosystem,
    model_params={"config_filepath": CONFIG_FILE_PATH},
    visualization_elements=[grid, chart],
    name="Simulated Jellyfish Population",
)

server.port = 8521
