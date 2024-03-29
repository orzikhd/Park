import math
from typing import Tuple, List

from park.behaviors.chomps import Chomps
from park.behaviors.remembers import Remembers
from park.behaviors.sees import SeenEntity
from park.behaviors.sees import Sees
from park.creatures.creature import Creature
from park.creatures.grass import Grass
from park.park_state import State


class Grazer(Creature):
    """
    Grazers are creatures that eat grass.
    """
    IMAGE_LOCATION = 'park\\pictures\\grazer.png'
    CHOMP_REACH = 2
    MEMORY_SIZE = 8
    HUNGRY_INTERVAL = 1

    def __init__(self,
                 state: State,
                 starting_position: Tuple[int, int],
                 scaler: float,
                 fertility: float,
                 speed: float,
                 viewing_distance: float):
        super().__init__(state, starting_position, scaler, fertility, speed)

        self.seesBehavior = Sees(self, viewing_distance)
        self.chompsBehavior = Chomps(self,
                                     self.HUNGRY_INTERVAL,
                                     self.CHOMP_REACH * self.state.pixel_size)
        self.remembersBehavior = Remembers(self.MEMORY_SIZE)

    def update(self):
        """
        A grazer looks for grass to eat when its hungry.
        It's lazy so if it sees grass, it'll walk to it without seeing if the grass moved. Why would grass move, right?
        If it's not hungry, it'll wander aimlessly. Maybe some day it shouldn't.
        """
        if not self.current_location_is_valid():
            self.die()

        if not self.is_alive():
            # might have been killed by another entity in the same tick and not know it yet
            return

        self.dirty = 1

        # stop at the first (closest) creature that's a grass
        def searching_behavior(seen_sprites: List[SeenEntity]):
            for seen_sprite in seen_sprites:
                if isinstance(seen_sprite.entity, Grass) \
                        and seen_sprite.entity not in self.remembersBehavior.memory:
                    return seen_sprite
            return None

        if not self.chompsBehavior.hungry():
            # not hungry yet!
            self.movesBehavior.move(self._random_walk)
            return

        # determine the target if one exists
        target = self.remembersBehavior.target
        if target:
            old_offset = target.offset
            self.seesBehavior.update_seen_entity(target)
            if old_offset != target.offset:
                picked_sprite = target
            else:
                # in the case the offset hasn't changed, we can't make progress towards our target so lets give up
                self.remembersBehavior.memory.append(target.entity)
                self.remembersBehavior.target = None
                picked_sprite = None
        else:
            picked_sprite = self.seesBehavior.see(searching_behavior)

        # determine what to do with the target if one exists
        if picked_sprite:
            if self.chompsBehavior.chomp(picked_sprite.entity):
                self.remembersBehavior.target = None
            else:
                # didn't chomp yet, pursue target
                self.remembersBehavior.target = picked_sprite
                self.movesBehavior.move(self._directed_walk(self.remembersBehavior.target.offset))
        else:
            # didn't find any grass!
            self.movesBehavior.move(self._random_walk)
