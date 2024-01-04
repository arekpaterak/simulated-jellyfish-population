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

        case JellyfishPolyp() as polyp:
            # https://icons8.com/icon/JrrHSGz7NmRU/coral
            portrayal = {
                "Shape": "src/resources/polyp1.png" if polyp.random.random() < 0.5 else "src/resources/polyp2.png",
                "scale": 2.5,
                "Layer": 1,
            }

        case JellyfishMedusa() as medusa:
            # https://icons8.com/icon/NU0xLnU5q3q8/jellyfish
            portrayal = {
                "Shape": "src/resources/jelly1.png" if medusa.random.random() < 0.5 else "src/resources/jelly2.png",
                "scale": 3,
                "Layer": 1,
            }

        case Plankton():
            portrayal = {
                "Shape": "circle",
                "Color": "green",
                "Layer": 0,
                "r": 0.5,
            }

        case SeaTurtle() as turtle:
            # https://icons8.com/icon/GZZxLoYInRiK/turtle
            portrayal = {
                "Shape": "src/resources/turtle1.png" if turtle.random.random() < 0.5 else "src/resources/turtle2.png",
                "scale": 7,
                "Layer": 5,
            }

        case Fish() as fish:
            # https://icons8.com/icon/u6IuaW242HuR/fish
            portrayal = {
                'Shape': "src/resources/fish1.png" if fish.random.random() < 0.5 else "src/resources/fish2.png",
                "scale": 3 if fish.is_mature() else 1,
                'Layer': 4,
            }

        case _:
            portrayal = {}

    return portrayal
