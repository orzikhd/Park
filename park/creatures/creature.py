import typing

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
        ParkEntity.__init__(self, state, starting_position, scaler, fertility)

        self.movesBehavior = Moves(self)
        self.speed = speed

        self.original_image = self.image

    # default behavior is to do nothing, should be overwritten
    def update(self):
        pass
