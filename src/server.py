import json
from mesa.visualization.modules import CanvasGrid
from portrayals import agent_portrayal
from mesa.visualization.ModularVisualization import ModularServer
from model import MarineEcosystem


with open('config.json') as file:
    config = json.load(file)

grid = CanvasGrid(agent_portrayal, config['width'], config['height'], canvas_width=config['width'] * 8, canvas_height=config['height'] * 8)

server = ModularServer(
    MarineEcosystem,
    [grid],
    "Jellyfish population simulation",
)

server.port = 8522

server.launch()
