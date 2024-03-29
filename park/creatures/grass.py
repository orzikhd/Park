import random
import statistics as st
import typing

import pygame

from park.behaviors.spreads import Spreads
from park.creatures.park_entity import ParkEntity
from park.park_state import State
from park.park_util import CREATURE_IMAGE_SIZE


class Grass(ParkEntity):
    """
    Grass is a background entity that spreads across the map.
    """
    IMAGE_LOCATION = 'park\\pictures\\grass-{}.png'

    def __init__(self,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float,
                 fertility: float,
                 active_grass_group):
        self.IMAGE_LOCATION = self._get_image_from_fertility(fertility)
        super().__init__(state, starting_position, scaler, fertility)

        self.spreads = Spreads(self.screen, self.rect, fertility)
        self.spread_options = self.spreads.get_neighboring_squares()

        self.active_grass_group = active_grass_group

    def _add_self_to_park(self, new_id):
        self.state.background_tree.tree.insert(new_id, self.get_bounding_box())

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

    def activate(self):
        self.add(self.active_grass_group)
        self.spread_options = self.spreads.get_neighboring_squares()

    def die(self):
        # warn nearby grasses to become active
        nearby_creatures = self.state.background_tree.get_nearest_creatures(creature=self, num_creatures=1)
        for creature in nearby_creatures:
            if isinstance(creature, Grass):
                creature.activate()

        ParkEntity.die(self)

    def update(self):
        """
        Grass spreads randomly to empty space around it.
        """
        if not self.current_location_is_valid():
            self.die()

        if not self.spread_options:
            self.remove(self.active_grass_group)  # remove self from active group
            return

        if self.spreads.should_spread():
            chosen_spot = random.choice(self.spread_options)
            self.spread_options.remove(chosen_spot)

            # ignore invalid spots
            if chosen_spot[0] < 0 \
                    or chosen_spot[0] >= self.state.park_width \
                    or chosen_spot[1] < 0 \
                    or chosen_spot[1] >= self.state.park_height:
                return

            if self.state.topography[chosen_spot] < self.state.sea_level:
                return

            if self.state.background_tree.check_spawning_collision(
                    creature=self,
                    proposed_rect=pygame.Rect(chosen_spot[0],
                                              chosen_spot[1],
                                              int(CREATURE_IMAGE_SIZE * self.scaler),
                                              int(CREATURE_IMAGE_SIZE * self.scaler))):
                return

            # new fertility is based on the env fertility with some small noise
            # we assume that the park's fertility is between 0 and 100 TODO read variable
            env_fertility = self.state.fertility_grid[chosen_spot] / 1000  # 0 to .1
            random_noise = (random.random() - .7) / 100  # 0.003

            new_fertility = env_fertility + random_noise
            new_fertility = st.mean([new_fertility, self.fertility])

            new_grass = Grass(self.state,
                              starting_position=chosen_spot,
                              scaler=self.scaler,
                              fertility=new_fertility,
                              active_grass_group=self.active_grass_group)

            new_grass.add(self.groups())
