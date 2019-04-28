import random
import typing

import pygame

from park_util import load_image
from park_state import State


class Creature(pygame.sprite.Sprite):
    image = 'pictures\\default.png'

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

    def get_bounding_box(self):
        return (self.rect.left,
                self.rect.top,
                self.rect.right,
                self.rect.bottom)

    def update(self):
        pass

    def _load_image_and_rect(self, starting_position: typing.Tuple[int, int]):
        self.image, self.rect = load_image(self.image)
        self.rect: pygame.Rect = self.rect.move(starting_position)

    def _spread(self):
        return random.random() < self.fertility

    def _generate_spread_options(self):
        return []

    def _check_spawning_collision(self):
        collisions = list(self.state.global_tree.intersection(
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

