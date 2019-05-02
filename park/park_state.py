import pygame
import random
import time
import numpy as np
import statistics
import park.diamond_square
from rtree import index
from scipy import spatial


class State:
    size = 6
    scaling = 5
    width = scaling * (2 ** size + 1)
    height = scaling * (2 ** size + 1)

    def __init__(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.global_sprites = {}
        self.global_sprite_tree = index.Index()
        self.global_sprite_counter = -1

        self.background_group = self._create_background()
        self.background_list = self.background_group.sprites()
        self.background_tree = spatial.KDTree([b.rect.center for b in self.background_list])

    def add_sprite_to_park(self, sprite):
        self.global_sprite_counter += 1
        self.global_sprites[self.global_sprite_counter] = sprite
        self.global_sprite_tree.insert(self.global_sprite_counter, sprite.get_bounding_box())
        return self.global_sprite_counter  # return the index given to this sprite just in case

    def _create_background(self):
        print(self.scaling / 20.0)
        from park.creatures.park_background import Background
        background_group = pygame.sprite.RenderPlain()
        matrix_width = int(self.width/self.scaling)
        matrix_height = int(self.height/self.scaling)

        start = time.time()
        noise_grid = park.diamond_square.DiamondSquare().create_diamond_square_map(2 ** self.size + 1)
        end = time.time()
        print("time to generate noise grid: ", (end - start) * 1000, "ms")
        # background_matrix = [[0 for y in range(matrix_height)] for x in range(matrix_width)]
        for x in range(matrix_width):
            for y in range(matrix_height):
                # fert = min(0.9, 0.4 + noise_grid[x, y])
                # fert = noise_grid[x, y]
                fert = noise_grid[x, y] / 100
                background_pixel = Background(self.screen,
                                              self,
                                              (x * self.scaling, y * self.scaling),
                                              self.scaling / 20.0,
                                              fert)
                # print("l: ", background_pixel.rect.left)
                # print("r: ", background_pixel.rect.right)
                # print("---")
                # print(y)
                # background_matrix[x][y] = background_pixel
                background_group.add(background_pixel)

        ferts = park.creatures.park_background.get_ferts()
        print("ferts: ", len(ferts))
        print("max", max(ferts))
        print("min", min(ferts))
        print("median", statistics.median(ferts))
        return background_group
