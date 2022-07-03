import typing

from park.creatures.creature import Creature
from park.park_state import State


class Bug(Creature):
    """
    Bugs are basic creatures that walk randomly.
    """
    IMAGE_LOCATION = 'park\\pictures\\bug.png'

    def __init__(self,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float,
                 fertility: float,
                 speed: float):
        super().__init__(state, starting_position, scaler, fertility, speed)

    def update(self):
        if not self.current_location_is_valid():
            self.die()
        self.dirty = 1
        self.movesBehavior.move(self._random_walk)
