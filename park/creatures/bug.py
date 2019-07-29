import math
import random
import typing

import pygame

from park.behaviors.moves import Moves
from park.creatures import creature
from park.park_state import State


class Bug(creature.Creature):
    IMAGE_LOCATION = 'park\\pictures\\bug.png'

    def __init__(self,
                 screen: pygame.Surface,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float,
                 fertility: float,
                 speed: float):
        creature.Creature.__init__(self, screen, state, starting_position, scaler, fertility)
        self.movesBehavior = Moves(self)
        self.original_image = self.image
        self.tick = 0
        self.speed = speed

    def update(self):
        def random_walk():
            x_offset = random.choice([self.speed, 0, -self.speed])
            y_offset = random.choice([self.speed, 0, -self.speed])

            offset = math.sqrt(x_offset**2 + y_offset**2)
            if offset:
                angle = math.atan2(-y_offset, x_offset)  # negative y_offset to account for reversed y axis
            else:
                angle = 0

            return offset, angle

        self.movesBehavior.move(random_walk)
