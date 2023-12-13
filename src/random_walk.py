"""
Generalized behavior for random walking, one grid cell at a time.
"""

import mesa


class RandomWalker(mesa.Agent):
    """
    Class implementing random walker methods in a generalized manner.

    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    def __init__(self, unique_id, position, model, moore=True):
        super().__init__(unique_id, model)
        self.position = position
        self.moore = moore

    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.position, self.moore, True)
        next_move = self.random.choice(next_moves)

        self.model.grid.move_agent(self, next_move)
