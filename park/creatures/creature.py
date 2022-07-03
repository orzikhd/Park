import math
import typing
import random

from park.behaviors.moves import Moves
from park.creatures.park_entity import ParkEntity
from park.park_state import State


class Creature(ParkEntity):
    """
    A basic creature of the park.
    state: the Park State object representing this park
    starting_position: where the creature should spawn
    scaler: how much to scale the creature's image
        for example, a 20px image with scaler .5 will be rendered as a 10px shape in the park
        defaults to 1
    fertility: the creature's fertility, between 0 and 1
    speed: how many pixels per tick the creature can move
    """
    IMAGE_LOCATION = 'park\\pictures\\creature.png'

    def __init__(self,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float,
                 fertility: float,
                 speed: float):
        super().__init__(state, starting_position, scaler, fertility)

        self.movesBehavior = Moves(self)
        self.speed = speed

        self.original_image = self.image

        self.rand_x_offset = 0
        self.rand_y_offset = 0

    def _add_self_to_park(self, new_id):
        self.state.creature_tree.tree.insert(new_id, self.get_bounding_box())

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

    # default behavior is to do nothing, should be overwritten
    def update(self):
        pass
