import typing

import pygame

from park.park_state import State
from park.creatures.creature import Creature


class Multisprite:
    def __init__(self,
                 screen: pygame.Surface,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float = 1):
        # create a 2x2 multisprite
        self.group = pygame.sprite.RenderUpdates()
        self.scaler = scaler

        for x in range(2):
            for y in range(2):
                creature = Creature(screen,
                                    state,
                                    (starting_position[0] + 20 * x, starting_position[1] + 20 * y),
                                    scaler)
                self.group.add(creature)
