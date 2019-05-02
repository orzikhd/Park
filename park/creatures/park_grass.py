import random
import typing

import pygame

from park.creatures import park_creature
from park.park_state import State


class Grass(park_creature.Creature):
    image = 'park\\pictures\\grass-{}.png'

    def __init__(self,
                 screen: pygame.Surface,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 fertility: float):
        self.image = self._get_image_from_fertility(fertility)
        park_creature.Creature.__init__(self, screen, state, starting_position, fertility)
        self.spread_options = self._generate_spread_options()

    def _generate_spread_options(self):
        return [self.rect.topright,  # right
                self.rect.bottomleft,  # down
                (self.rect.left - self.rect.width, self.rect.top),  # left
                (self.rect.left, self.rect.top - self.rect.height)  # up
                ]

    def _get_image_from_fertility(self, fertility):
        if fertility < 0.01:
            return self.image.format("1")
        elif fertility < 0.05:
            return self.image.format("2")
        elif fertility < 0.1:
            return self.image.format("3")
        else:
            return self.image.format("4")

    def update(self):
        if not self.spread_options:
            # print("current active group len: ", len(group.sprites()))
            self.groups()[0].remove(self)  # remove self from active group
            # park_util.global_tree = KDTree([sprite.rect.center for sprite in group])
            # print("removed self")
            return

        if self._spread():
            chosen_spot = random.choice(self.spread_options)
            self.spread_options.remove(chosen_spot)
            if chosen_spot[0] < 0 \
                    or chosen_spot[0] > self.screen.get_rect().right \
                    or chosen_spot[1] < 0 \
                    or chosen_spot[1] > self.screen.get_rect().bottom:
                # print("hit border")
                return

            new_grass = Grass(self.screen, self.state, chosen_spot, random.choice([0.009, 0.04, 0.09, 0.5]))
            if not new_grass._check_spawning_collision():
                new_grass.add(self.groups())
                self.state.add_sprite_to_park(new_grass)
