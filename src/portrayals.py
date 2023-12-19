from agents import (
    JellyfishLarva,
    JellyfishPolyp,
    JellyfishMedusa,
    Plankton,
    Fish,
    SeaTurtle
)

def agent_portrayal(agent):

    if isinstance(agent, JellyfishLarva):
        portrayal = {
            "Shape": "circle",
            "Color": "blue",
            "Filled": "true",
            "Layer": 0,
            "r": 1
        }

    # if isinstance(agent, JellyfishPolyp):
    #     portrayal = {
    #         "Shape": "circle",
    #         "Color": "blue",
    #         "Filled": "false",
    #         "Layer": 0,
    #         "r": 0.5
    #     }
    #
    # if isinstance(agent, JellyfishMedusa):
    #     portrayal = {
    #         "Shape": "circle",
    #         "Color": "blue",
    #         "Filled": "true",
    #         "Layer": 0,
    #         "r": 0.6
    #     }
    #
    # if isinstance(agent, Plankton):
    #     portrayal = {
    #         "Shape": "rectangle",
    #         "Color": "green",
    #         "Filled": "false",
    #         "Layer": 0,
    #         "r": 0.4
    #     }
    #
    # if isinstance(agent, SeaTurtle):
    #     portrayal = {
    #         "Shape": "circle",
    #         "Color": "yellow",
    #         "Filled": "true",
    #         "Layer": 0,
    #         "r": 0.6
    #     }
    #
    # if isinstance(agent, Fish):
    #     portrayal = {
    #         "Shape": "circle",
    #         "Color": "purple",
    #         "Filled": "true",
    #         "Layer": 0,
    #         "r": 0.4
    #     }

    else:
        portrayal = {}

    return portrayal