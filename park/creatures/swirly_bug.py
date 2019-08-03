import math
import random
import typing

import pygame

from park.behaviors.moves import Moves
from park.creatures import creature
from park.park_state import State


class SwirlyBug(creature.Creature):
    IMAGE_LOCATION = 'park\\pictures\\swirly-bug.png'

    ROTATION_CONSTANT = 28  # dividing the radians into 14 sections, I think

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
        self.speed = speed
        self.angle = 0

    def _circle_walk(self):
        self.angle += 1
        return self.speed, (self.angle / self.ROTATION_CONSTANT) * math.pi

    def update(self):
        self.movesBehavior.move(self._circle_walk)
