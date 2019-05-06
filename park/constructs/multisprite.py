import typing

import pygame

from park.park_state import State
from park.creatures.park_creature import Creature


class Multisprite:
    def __init__(self,
                 screen: pygame.Surface,
                 state: State,
                 starting_position: typing.Tuple[int, int]):
        # create a 2x2 multisprite
        self.group = pygame.sprite.RenderUpdates()

        for x in range(2):
            for y in range(2):
                creature = Creature(screen,
                                    state,
                                    (starting_position[0] + 20 * x, starting_position[1] + 20 * y))
                state.add_sprite_to_park(creature)
                self.group.add(creature)
