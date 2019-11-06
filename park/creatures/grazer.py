import math
import random
import typing

from park.behaviors.sees import SeenSprite
from park.behaviors.sees import Sees
from park.creatures.creature import Creature
from park.creatures.grass import Grass
from park.park_state import State


class Grazer(Creature):
    IMAGE_LOCATION = 'park\\pictures\\grazer.png'
    CHOMP_REACH = 5

    def __init__(self,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float,
                 fertility: float,
                 speed: float,
                 viewing_distance: float):
        super().__init__(state, starting_position, scaler, fertility, speed)

        self.seesBehavior = Sees(self, viewing_distance)

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
        creature.die()
        self.hunger = 0

    def update(self):
        self.dirty = 1

        if self.hunger < 10:
            self.movesBehavior.move(self._random_walk)
            self.hunger += 1
            return

        seen_sprites: typing.List[SeenSprite] = self.seesBehavior.see()

        # stop at the first (closest) creature that's a grass
        for seen_sprite in seen_sprites:
            if isinstance(seen_sprite.sprite, Grass):
                if seen_sprite.l1_distance < self.CHOMP_REACH:
                    self._graze(seen_sprite.sprite)
                    return
                else:
                    self.movesBehavior.move(self._directed_walk(seen_sprite.offset))
                    return

        self.movesBehavior.move(self._random_walk)
