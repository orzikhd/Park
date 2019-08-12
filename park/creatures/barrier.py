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
        park_entity.ParkEntity.__init__(self, state, starting_position, scaler)
