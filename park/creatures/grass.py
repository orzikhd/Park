import random
import typing
import statistics as st

import pygame

from park.behaviors.spreads import Spreads
from park.creatures import creature
from park.park_state import State


class Grass(creature.Creature):
    IMAGE_LOCATION = 'park\\pictures\\grass-{}.png'

    def __init__(self,
                 screen: pygame.Surface,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float,
                 fertility: float):
        self.IMAGE_LOCATION = self._get_image_from_fertility(fertility)
        creature.Creature.__init__(self, screen, state, starting_position, scaler, fertility)
        self.spreads = Spreads(screen, fertility, self.rect)
        self.spread_options = self._generate_spread_options()

    def _generate_spread_options(self):
        return self.spreads.get_neighboring_squares()

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
            self.groups()[0].remove(self)  # remove self from active group
            return

        if self.spreads.should_spread():
            chosen_spot = random.choice(self.spread_options)
            self.spread_options.remove(chosen_spot)
            if chosen_spot[0] < 0 \
                    or chosen_spot[0] >= self.state.WIDTH \
                    or chosen_spot[1] < 0 \
                    or chosen_spot[1] >= self.state.HEIGHT:
                # print("hit border")
                return

            if self._check_spawning_collision(pygame.Rect(chosen_spot[0],
                                                          chosen_spot[1],
                                                          int(20 * self.scaler),
                                                          int(20 * self.scaler))):
                return

            env_fertility = self.state.fertility_grid[chosen_spot] / 1000
            random_noise = (random.random() - .5) / 100

            new_fertility = env_fertility + random_noise
            new_fertility = st.mean([new_fertility, self.fertility])

            new_grass = Grass(self.screen,
                              self.state,
                              chosen_spot,
                              self.scaler,
                              new_fertility)

            new_grass.add(self.groups())
