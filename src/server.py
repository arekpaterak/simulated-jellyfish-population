from mesa.visualization.modules import CanvasGrid
from portrayals import agent_portrayal
from mesa.visualization.ModularVisualization import ModularServer
from model import MarineEcosystem


grid = CanvasGrid(agent_portrayal, 100, 100, canvas_width=800, canvas_height=800)

server = ModularServer(
    MarineEcosystem,
    [grid],
    "Jellyfish population simulation",
)

server.port = 8521
server.launch()
