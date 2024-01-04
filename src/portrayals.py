from agents.food_source import (
    Plankton,
)

from agents.animals import (
    JellyfishLarva,
    JellyfishMedusa,
    JellyfishPolyp,
    Fish,
    SeaTurtle,
)


def agent_portrayal(agent):
    match agent:
        case JellyfishLarva():
            portrayal = {
                "Shape": "circle",
                "Color": "#f76fa3",
                "Filled": "true",
                "Layer": 1,
                "r": 0.3,
            }

        case JellyfishPolyp():
            portrayal = {
                "Shape": "circle",
                "Color": "#f76fa3",
                "Layer": 1,
                "r": 0.6,
            }

        case JellyfishMedusa():
            portrayal = {
                "Shape": "circle",
                "Color": "#f76fa3",
                "Filled": "true",
                "Layer": 1,
                "r": 0.9,
            }

        case Plankton():
            portrayal = {
                "Shape": "circle",
                "Color": "green",
                "Layer": 0,
                "r": 0.5,
            }

        case SeaTurtle():
            portrayal = {
                "Shape": "circle",
                "Color": "green",
                "Filled": "true",
                "Layer": 5,
                "r": 5,
            }

        case Fish() as fish:
            portrayal = {
                "Shape": "circle",
                "Color": "gray",
                "Filled": "true",
                "Layer": 4,
                "r": 2 if fish.is_mature() else 1,
            }

        case _:
            portrayal = {}

    return portrayal
