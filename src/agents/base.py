import mesa


# TODO: think generally about energy

Position = tuple[int, int]


class BaseSeaAgent(mesa.Agent):
    """
    Base class for all agents in the simulation.
    """

    def __init__(
        self, unique_id: int, position: Position, model: mesa.Model, moore: bool = True
    ) -> None:
        super().__init__(unique_id, model)
        self.position = position
        self.moore = moore

    def is_food_source(self):
        return False
