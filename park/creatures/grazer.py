import math
import random
from typing import Tuple, Optional, List

from park.behaviors.sees import SeenSprite
from park.behaviors.sees import Sees
from park.creatures.creature import Creature
from park.creatures.grass import Grass
from park.park_state import State

from collections import deque


class Grazer(Creature):
    IMAGE_LOCATION = 'park\\pictures\\grazer.png'
    CHOMP_REACH = 10
    MEMORY_SIZE = 8

    def __init__(self,
                 state: State,
                 starting_position: Tuple[int, int],
                 scaler: float,
                 fertility: float,
                 speed: float,
                 viewing_distance: float):
        super().__init__(state, starting_position, scaler, fertility, speed)

        self.seesBehavior = Sees(self, viewing_distance)
        self.target: Optional[SeenSprite] = None
        self.badTargets = deque(maxlen=self.MEMORY_SIZE)

        self.rand_x_offset = 0
        self.rand_y_offset = 0
        self.hunger = 10

    def _random_walk(self):
        if random.random() < 0.25:
            self.rand_x_offset = random.choice([self.speed, 0, -self.speed])
            self.rand_y_offset = random.choice([self.speed, 0, -self.speed])

        offset = math.hypot(self.rand_x_offset, self.rand_y_offset)
        if offset:
            # negative y_offset to account for reversed y axis
            angle = math.atan2(-self.rand_y_offset, self.rand_x_offset)
        else:
            angle = 0

        return offset, angle

    def _directed_walk(self, offset):
        x_offset: float = math.copysign(min(abs(offset[0]), self.speed), offset[0])
        y_offset: float = math.copysign(min(abs(offset[1]), self.speed), offset[1])

        angle = math.atan2(-y_offset, x_offset)  # negative y_offset to account for reversed y axis

        return lambda: (math.hypot(x_offset, y_offset), angle)

    def _graze(self, creature):
        if creature.is_alive():
            # print("Ate grass")
            creature.die()
            self.hunger = 0
        else:
            print("Tried to eat something that was already dead :(")
        self.target = None

    def update(self):
        """
        A grazer looks for grass to eat when its hungry.
        It's lazy so if it sees grass, it'll walk to it without seeing if the grass moved. Why would grass move, right?
        If it's not hungry, it'll wander aimlessly. Maybe some day it shouldn't.
        """
        self.dirty = 1

        # print(f"Target: {self.target}")

        # stop at the first (closest) creature that's a grass
        def searching_behavior(seen_sprites: List[SeenSprite]):
            for seen_sprite in seen_sprites:
                # if seen_sprite.sprite in self.badTargets:
                #     print(f"skipped bad target from {len(self.badTargets)} -- {self.badTargets}")
                if isinstance(seen_sprite.sprite, Grass) and seen_sprite.sprite not in self.badTargets:
                    return seen_sprite
            return None

        if self.hunger < 2:
            self.movesBehavior.move(self._random_walk)
            self.hunger += 1
            return

        # determine the target if one exists
        if self.target:
            old_offset = self.target.offset
            self.seesBehavior.update_seen_sprite(self.target)
            if old_offset != self.target.offset:
                picked_sprite = self.target
            else:
                # in the case the offset hasn't changed, we can't make progress towards our target so lets give up
                self.badTargets.append(self.target.sprite)
                self.target = None
                picked_sprite = None
        else:
            picked_sprite = self.seesBehavior.see(searching_behavior)

        # determine what to do with the target if one exists
        if picked_sprite:
            if picked_sprite.l1_distance <= self.CHOMP_REACH:
                self._graze(picked_sprite.sprite)
            else:
                self.target = picked_sprite
                self.movesBehavior.move(self._directed_walk(self.target.offset))
        else:
            self.movesBehavior.move(self._random_walk)
