import typing

import pygame
from park.park_state import State
from park.creatures import park_creature

ferts = []


def get_ferts():
    return ferts


class Background(park_creature.Creature):
    image = 'park\\pictures\\dirt-{}.png'

    def __init__(self,
                 screen: pygame.Surface,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler,
                 fertility: float):
        self.image = self._get_image_from_fertility(fertility)
        self.scaler = scaler
        park_creature.Creature.__init__(self, screen, state, starting_position, fertility)

    def _get_image_from_fertility(self, fertility):
        transformed_fert = fertility * 10 + 1
        ferts.append(transformed_fert)
        return self.image.format(int(transformed_fert))
