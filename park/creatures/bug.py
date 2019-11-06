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
        super().__init__(state, starting_position, scaler, fertility, speed)
        self.x_offset = 0
        self.y_offset = 0

    def _random_walk(self):
        if random.random() < 0.25:
            self.x_offset = random.choice([self.speed, 0, -self.speed])
            self.y_offset = random.choice([self.speed, 0, -self.speed])

        offset = math.hypot(self.x_offset, self.y_offset)
        if offset:
            angle = math.atan2(-self.y_offset, self.x_offset)  # negative y_offset to account for reversed y axis
        else:
            angle = 0

        return offset, angle

    def update(self):
        self.dirty = 1
        self.movesBehavior.move(self._random_walk)
