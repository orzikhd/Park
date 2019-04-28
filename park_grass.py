import random
import typing

import pygame

import park_creature
import park_util
from park_util import global_tree
from park_util import load_image


class Grass(park_creature.Creature):
    default_image = 'pictures\\grass.png'

    def __init__(self,
                 screen: pygame.Surface,
                 starting_position: typing.Tuple[int, int],
                 fertility: float):
        park_creature.Creature.__init__(self, screen, starting_position, fertility)
        self.screen: pygame.Surface = screen
        self.image, self.rect = load_image('pictures\\grass.png')
        self.fertility = fertility
        self.rect: pygame.Rect = self.rect.move(starting_position)
        self.spread_options = [self.rect.topright,  # right
                               self.rect.bottomleft,  # down
                               (self.rect.left - self.rect.width, self.rect.top),  # left
                               (self.rect.left, self.rect.top - self.rect.height)  # up
                               ]
        # print(self.spread_options)

    def update(self):
        if not self.spread_options:
            # print("current active group len: ", len(group.sprites()))
            self.groups()[0].remove(self)  # remove self from active group
            # park_util.global_tree = KDTree([sprite.rect.center for sprite in group])
            # print("removed self")
            return

        if self._spread():
            chosen_spot = random.choice(self.spread_options)
            self.spread_options.remove(chosen_spot)
            if chosen_spot[0] < 0 \
                    or chosen_spot[0] > self.screen.get_rect().right \
                    or chosen_spot[1] < 0 \
                    or chosen_spot[1] > self.screen.get_rect().bottom:
                # print("hit border")
                return

            new_grass = Grass(self.screen, chosen_spot, 0.5)
            if not new_grass._check_spawning_collision():
                new_grass.add(self.groups())

                park_util.global_sprite_counter += 1
                global_tree.insert(park_util.global_sprite_counter,
                                   (new_grass.rect.left,
                                    new_grass.rect.top,
                                    new_grass.rect.right,
                                    new_grass.rect.bottom)
                                   )
                park_util.global_sprites[park_util.global_sprite_counter] = new_grass


