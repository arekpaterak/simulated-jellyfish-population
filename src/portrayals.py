from agents import (
    JellyfishLarva,
    JellyfishPolyp,
    JellyfishMedusa
)

def agent_portrayal(agent):

    if isinstance(agent, JellyfishLarva):
        portrayal = {
            "Shape": "circle",
            "Color": "red",
            "Filled": "true",
            "Layer": 0,
            "r": 0.5
        }
        print('132')

    else:
        portrayal = {}

    return portrayal