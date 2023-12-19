from agents import (
    JellyfishLarva,
    JellyfishPolyp,
    JellyfishMedusa,
    Plankton,
    SeaTurtle,
    Fish,
)


def agent_portrayal(agent):
    match agent:
        case JellyfishLarva():
            portrayal = {
                "Shape": "circle",
                "Color": "#f76fa3",
                "Filled": "true",
                "Layer": 0,
                "r": 0.5,
            }

        case JellyfishPolyp():
            portrayal = {
                "Shape": "circle",
                "Color": "#f76fa3",
                "Filled": "false",
                "Layer": 0,
                "r": 1,
            }

        # if isinstance(agent, JellyfishMedusa):
        #     portrayal = {
        #         "Shape": "circle",
        #         "Color": "blue",
        #         "Filled": "true",
        #         "Layer": 0,
        #         "r": 0.6
        #     }

        # if isinstance(agent, Plankton):
        #     portrayal = {
        #         "Shape": "rectangle",
        #         "Color": "green",
        #         "Filled": "false",
        #         "Layer": 0,
        #         "r": 0.4
        #     }

        # if isinstance(agent, SeaTurtle):
        #     portrayal = {
        #         "Shape": "circle",
        #         "Color": "yellow",
        #         "Filled": "true",
        #         "Layer": 0,
        #         "r": 0.6
        #     }

        # if isinstance(agent, Fish):
        #     portrayal = {
        #         "Shape": "circle",
        #         "Color": "purple",
        #         "Filled": "true",
        #         "Layer": 0,
        #         "r": 0.4
        #     }

        case _:
            portrayal = {}

    return portrayal
