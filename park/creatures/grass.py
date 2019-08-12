import random
import statistics as st
import typing

import pygame

from park.behaviors.spreads import Spreads
from park.creatures import park_entity
from park.park_state import State
from park.park_util import CREATURE_IMAGE_SIZE


class Grass(park_entity.ParkEntity):
    IMAGE_LOCATION = 'park\\pictures\\grass-{}.png'

    def __init__(self,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float,
                 fertility: float,
                 active_grass_group):
        self.IMAGE_LOCATION = self._get_image_from_fertility(fertility)
        park_entity.ParkEntity.__init__(self, state, starting_position, scaler, fertility)

        self.spreads = Spreads(self.screen, self.rect, fertility)
        self.spread_options = self.spreads.get_neighboring_squares()

        self.active_grass_group = active_grass_group

    def _get_image_from_fertility(self, fertility):
        if fertility < 0.02:
            return self.IMAGE_LOCATION.format("1")
        elif fertility < 0.04:
            return self.IMAGE_LOCATION.format("2")
        elif fertility < 0.06:
            return self.IMAGE_LOCATION.format("3")
        elif fertility < 0.08:
            return self.IMAGE_LOCATION.format("4")
        else:
            return self.IMAGE_LOCATION.format("5")

    def update(self):
        if not self.spread_options:
            # self.groups()[0].remove(self)  # remove self from active group
            self.remove(self.active_grass_group)
            return

        if self.spreads.should_spread():
            chosen_spot = random.choice(self.spread_options)
            self.spread_options.remove(chosen_spot)
            if chosen_spot[0] < 0 \
                    or chosen_spot[0] >= self.state.WIDTH \
                    or chosen_spot[1] < 0 \
                    or chosen_spot[1] >= self.state.HEIGHT:
                print("hit border")
                return

            if self.state.background_tree.check_spawning_collision(
                    creature=self,
                    proposed_rect=pygame.Rect(chosen_spot[0],
                                              chosen_spot[1],
                                              int(CREATURE_IMAGE_SIZE * self.scaler),
                                              int(CREATURE_IMAGE_SIZE * self.scaler))):
                return

            env_fertility = self.state.fertility_grid[chosen_spot] / 1000
            random_noise = (random.random() - .5) / 100

            new_fertility = env_fertility + random_noise
            new_fertility = st.mean([new_fertility, self.fertility])

            new_grass = Grass(self.state,
                              starting_position=chosen_spot,
                              scaler=self.scaler,
                              fertility=new_fertility,
                              active_grass_group=self.active_grass_group)

            new_grass.add(self.groups())
