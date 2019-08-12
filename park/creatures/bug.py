import math
import random
import typing

from park.creatures.creature import Creature
from park.park_state import State


class Bug(Creature):
    IMAGE_LOCATION = 'park\\pictures\\bug.png'

    def __init__(self,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float,
                 fertility: float,
                 speed: float):
        Creature.__init__(self, state, starting_position, scaler, fertility, speed)

    def _random_walk(self):
        x_offset = random.choice([self.speed, 0, -self.speed])
        y_offset = random.choice([self.speed, 0, -self.speed])

        offset = math.sqrt(x_offset**2 + y_offset**2)
        if offset:
            angle = math.atan2(-y_offset, x_offset)  # negative y_offset to account for reversed y axis
        else:
            angle = 0

        return offset, angle

    def update(self):
        self.movesBehavior.move(self._random_walk)
