import random
import typing

import pygame

import park
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
        self.scaler = scaler
        self.fertility = fertility
        self.image, self.rect = self._load_image_and_rect(starting_position)
        self.sprite_id = self.state.add_sprite_to_park(self)

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

    def _check_spawning_collision(self, proposed_rect, ignore_grass=False):
        return self._check_collision(proposed_rect, False, ignore_grass)

    def _check_moving_collision(self, proposed_rect, ignore_grass=False):
        return self._check_collision(proposed_rect, True, ignore_grass)

    def _check_collision(self, proposed_rect, ignore_self, ignore_grass):
        collisions = list(self.state.global_sprite_tree.intersection(self.get_bounding_box(proposed_rect)))
        if ignore_self and self.sprite_id in collisions:
            collisions.remove(self.sprite_id)

        if collisions:
            # print(collisions)
            pass

        for collision in collisions:
            # print("collision: ", collision)
            collided_sprite = self.state.global_sprites[collision]
            if (ignore_grass
                    and type(collided_sprite) == park.creatures.grass.Grass):
                continue
            if collided_sprite.rect.colliderect(proposed_rect):
                # print("collided!")
                return True

        # print("all good")
        return False
