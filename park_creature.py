import random
import typing

import pygame

import park_util
from park_util import load_image


class Creature(pygame.sprite.Sprite):
    default_image = 'pictures\\default.png'

    def __init__(self,
                 screen: pygame.Surface,
                 starting_position: typing.Tuple[int, int],
                 fertility: float = 0):
        pygame.sprite.Sprite.__init__(self)
        self.screen: pygame.Surface = screen
        self.fertility = fertility
        self._load_image_and_rect(starting_position)

    def _load_image_and_rect(self, starting_position: typing.Tuple[int, int]):
        self.image, self.rect = load_image(self.default_image)
        self.rect: pygame.Rect = self.rect.move(starting_position)

    def _spread(self):
        return random.random() < self.fertility

    def _generate_spread_options(self):
        return []

    def _check_spawning_collision(self):
        collisions = list(park_util.global_tree.intersection(
                    (self.rect.left,
                     self.rect.top,
                     self.rect.right,
                     self.rect.bottom)))
        # print("len collisions: ", len(collisions))

        for collision in collisions:
            # print("collision: ", collision)
            if park_util.global_sprites[collision].rect.colliderect(self.rect):
                # print("collided!")
                return True

        # print("all good")
        return False

