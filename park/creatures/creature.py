import typing

import pygame

import park.park_util as pu
from park.park_state import State


class Creature(pygame.sprite.Sprite):
    """
    A base creature of the park.
    Creature inherits from Sprite and uses that for all PyGame logic.
    screen: a pygame surface that the creature will be drawn on
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
                 screen: pygame.Surface,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float = 1,
                 fertility: float = 0):
        pygame.sprite.Sprite.__init__(self)
        self.screen: pygame.Surface = screen
        self.state: State = state
        self.scaler: float = scaler
        self.fertility: float = fertility
        self.image: pygame.Surface
        self.rect: pygame.Rect
        self.image, self.rect = self._load_image_and_rect(starting_position)
        self.sprite_id: int = self.state.add_sprite_to_park(self)

    # helper function to return the 4 corners of a rect as a tuple
    # if the rect isn't provided, returns the corners of the rect of self
    def get_bounding_box(self, rect=None):
        # print(self, rect)
        rect = rect if rect else self.rect  # I'm sorry
        return (rect.left,
                rect.top,
                rect.right,
                rect.bottom)

    # update function is inherited from Sprite and is called with every tick
    # default behavior is to do nothing, should be overwritten
    def update(self):
        pass

    def _load_image_and_rect(self, starting_position: typing.Tuple[int, int]):
        image, rect = pu.load_image(self.IMAGE_LOCATION, self.scaler)
        rect: pygame.Rect = rect.move(starting_position)
        return image, rect