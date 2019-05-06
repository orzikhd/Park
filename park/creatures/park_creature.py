import random
import typing

import pygame

from park.park_util import load_image
from park.park_state import State


class Creature(pygame.sprite.Sprite):
    """
    A base creature of the park.
    Creature inherits from Sprite and uses that for all PyGame logic.
    screen: a pygame surface that the creature will be drawn on
    state: the Park State object representing this park
    starting_position: where the creature should spawn
    fertility: the creature's fertility, between 0 and 1
    """

    # override this to get a different image for your creature
    # images are expected to be 20x20 pixels
    image = 'park\\pictures\\default-1.png'
    # how much to scale the creature's image
    # for example, a 20px image with scaler .5 will be rendered as a 10px shape in the park
    scaler = 1

    def __init__(self,
                 screen: pygame.Surface,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 fertility: float = 0):
        pygame.sprite.Sprite.__init__(self)
        self.screen: pygame.Surface = screen
        self.state: State = state
        self.fertility = fertility
        self._load_image_and_rect(starting_position)

    # helper function to return the 4 corners of the creature as a tuple
    def get_bounding_box(self):
        return (self.rect.left,
                self.rect.top,
                self.rect.right,
                self.rect.bottom)

    # update function is inherited from Sprite and is called with every tick
    # default behavior is to do nothing, should be overwritten
    def update(self):
        pass

    def _load_image_and_rect(self, starting_position: typing.Tuple[int, int]):
        self.image, self.rect = load_image(self.image, self.scaler)
        self.rect: pygame.Rect = self.rect.move(starting_position)

    def _spread(self):
        return random.random() < self.fertility

    def _generate_spread_options(self):
        return []

    def _check_spawning_collision(self):
        collisions = list(self.state.global_sprite_tree.intersection(
                    (self.rect.left,
                     self.rect.top,
                     self.rect.right,
                     self.rect.bottom)))

        for collision in collisions:
            # print("collision: ", collision)
            if self.state.global_sprites[collision].rect.colliderect(self.rect):
                # print("collided!")
                return True

        # print("all good")
        return False

