from typing import List, Tuple

import pygame

from park.park_state import State
from park.creatures.barrier import Barrier


class Multisprite:
    """
    A wrapper for a group of sprites created all at once to be one entity.
    """
    def __init__(self,
                 state: State,
                 positions: List[Tuple[int, int]],
                 scaler: float = 1):
        """
        Create the Multisprite.
        :param state: state of the park
        :param positions: list of positions to place sprites into to create the multisprite
        :param scaler: how much to scale the sprite's image for each sprite
        """
        self.group = pygame.sprite.RenderUpdates()
        self.scaler = scaler

        for position in positions:
            creature = Barrier(state=state,
                               starting_position=position,
                               scaler=scaler)
            self.group.add(creature)
