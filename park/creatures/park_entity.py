import typing

import pygame

import park.park_util as pu
from park.park_state import State


class ParkEntity(pygame.sprite.DirtySprite):
    """
    A basic entity of the park.
    ParkEntity inherits from Sprite and uses that for all PyGame logic.
    state: the Park State object representing this park
    starting_position: where the creature should spawn
    scaler: how much to scale the creature's image
        for example, a 20px image with scaler .5 will be rendered as a 10px shape in the park
        defaults to 1
    fertility: the creature's fertility, between 0 and 1
    """

    # override this to get a different image for your creature
    IMAGE_LOCATION = 'park\\pictures\\default-1.png'

    def __init__(self,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float = 1,
                 fertility: float = 0):
        super().__init__()
        self.state: State = state
        self.screen = self.state.screen
        self.scaler: float = scaler
        self.fertility: float = fertility
        self.dirty = 1
        self.image, self.rect = self._load_image_and_rect(starting_position)
        self.sprite_id: int = self.state.add_entity_to_park(self, self._add_self_to_park)
        self.alive = True

    def _add_self_to_park(self, new_id):
        pass

    def get_bounding_box(self, rect=None):
        """
        Helper function to return the 4 corners of a rect as a tuple.
        If the rect isn't provided, returns the corners of the rect of self
        """
        # print(self, rect)
        rect = rect if rect else self.rect  # I'm sorry
        return (rect.left,
                rect.top,
                rect.right,
                rect.bottom)

    def is_alive(self):
        return self.alive;

    def die(self):
        """
        The entity should cease existing in the park at this point.
        """
        self.dirty = 0
        self.state.remove_entity_from_park(self, self.sprite_id)
        self.alive = False
        self.kill()

    def update(self, *args):
        """
        Update function is inherited from Sprite and is called with every tick
        default behavior is to do nothing, should be overwritten
        """
        pass

    def _load_image_and_rect(self, starting_position: typing.Tuple[int, int]):
        image, rect = pu.load_image(self.IMAGE_LOCATION, self.scaler)
        rect: pygame.Rect = rect.move(starting_position[0], starting_position[1])
        return image, rect
