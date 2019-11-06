import typing

from park.creatures import park_entity
from park.park_state import State


class Barrier(park_entity.ParkEntity):
    """
    A barrier entity exists both as a background and a creature.
    """
    def __init__(self,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float):
        super().__init__(state, starting_position, scaler)

    def _add_self_to_park(self, new_id):
        self.state.creature_tree.tree.insert(new_id, self.get_bounding_box())
        self.state.background_tree.tree.insert(new_id, self.get_bounding_box())
