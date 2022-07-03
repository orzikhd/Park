from typing import Tuple, List

from park.behaviors.chomps import Chomps
from park.behaviors.remembers import Remembers
from park.behaviors.sees import Sees, SeenEntity
from park.creatures.bug import Bug
from park.creatures.creature import Creature
from park.creatures.grazer import Grazer
from park.park_state import State


class Muncher(Creature):
    """
    Munchers are creatures that eat other creatures.
    """
    IMAGE_LOCATION = 'park\\pictures\\muncher.png'
    CHOMP_REACH = 1.5
    HUNGRY_INTERVAL = 1  # 5
    MEMORY_SIZE = 1

    EDIBLE_CREATURE_SPECIES = {Bug, Grazer}

    def __init__(self,
                 state: State,
                 starting_position: Tuple[int, int],
                 scaler: float,
                 fertility: float,
                 speed: float,
                 viewing_distance: float):
        super().__init__(state, starting_position, scaler, fertility, speed)

        self.seesBehavior = Sees(self, viewing_distance, see_background=False)
        self.chompsBehavior = Chomps(self,
                                     self.HUNGRY_INTERVAL,
                                     int(self.CHOMP_REACH * self.state.pixel_size))
        self.remembersBehavior = Remembers(self.MEMORY_SIZE)

    def update(self):
        """
        A muncher looks for creatures to eat but otherwise wanders aimlessly.
        """
        if not self.current_location_is_valid():
            self.die()

        self.dirty = 1

        if not self.chompsBehavior.hungry():
            # not hungry yet!
            self.movesBehavior.move(self._random_walk)
            return

        # stop at the first (closest) creature that's edible
        def searching_behavior(seen_sprites: List[SeenEntity]):
            for seen_sprite in seen_sprites:
                for species in self.EDIBLE_CREATURE_SPECIES:
                    if isinstance(seen_sprite.entity, species) \
                            and seen_sprite.entity not in self.remembersBehavior.memory:
                        # print("picked sprite", seen_sprite)
                        return seen_sprite
            return None

        # determine the target if one exists
        target = self.remembersBehavior.target
        if target:
            # print("chasing target")
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
            # print("looking for target")
            picked_sprite = self.seesBehavior.see(searching_behavior)
            self.remembersBehavior.target = picked_sprite

        # determine what to do with the target if one exists
        if picked_sprite:
            if self.chompsBehavior.chomp(picked_sprite.entity):
                # print("muncher chomped!", self, picked_sprite)
                self.remembersBehavior.target = None
            else:
                # print("moving towards target")
                # didn't chomp yet, pursue target
                self.movesBehavior.move(self._directed_walk(self.remembersBehavior.target.offset))
        else:
            # didn't find anything to eat
            self.movesBehavior.move(self._random_walk)
