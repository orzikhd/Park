import math
import typing

from park.creatures.creature import Creature
from park.park_state import State


class SwirlyBug(Creature):
    """
    SwirlyBugs exist as a tech demo of manipulating movement behavior across ticks.
    """
    IMAGE_LOCATION = 'park\\pictures\\swirly-bug.png'

    ROTATION_CONSTANT = 28  # dividing the radians into 14 sections, I think

    def __init__(self,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float,
                 fertility: float,
                 speed: float):
        super().__init__(state, starting_position, scaler, fertility, speed)
        self.angle = 0

    def _circle_walk(self):
        self.angle += 1
        return self.speed, (self.angle / self.ROTATION_CONSTANT) * math.pi

    def update(self):
        if not self.current_location_is_valid():
            self.die()

        self.dirty = 1
        self.movesBehavior.move(self._circle_walk)
