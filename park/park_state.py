import statistics
import time

import numpy as np
import pygame
from rtree import index

import park.diamond_square


class State:
    grid_depth = 6
    pixel_size = 10
    width = pixel_size * (2 ** grid_depth + 1)
    height = pixel_size * (2 ** grid_depth + 1)

    def __init__(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.global_sprites = {}
        self.global_sprite_tree = index.Index()
        self.global_sprite_counter = -1

        # self.background_group = self._create_background()
        # self.background_list = self.background_group.sprites()
        # self.background_tree = spatial.KDTree([b.rect.center for b in self.background_list])
        self.background_grid = self._create_background()

    def add_sprite_to_park(self, sprite):
        self.global_sprite_counter += 1
        self.global_sprites[self.global_sprite_counter] = sprite
        self.global_sprite_tree.insert(self.global_sprite_counter, sprite.get_bounding_box())
        return self.global_sprite_counter  # return the index given to this sprite just in case

    def _create_background(self):
        import park.constructs.park_background as pb

        start = time.time()
        noise_grid = park.diamond_square.DiamondSquare().create_diamond_square_map(2 ** self.grid_depth + 1)
        end = time.time()
        print("time to generate noise grid: ", (end - start) * 1000, "ms")

        # convert noise grid into color grid
        colors = np.zeros((noise_grid.shape[0], noise_grid.shape[1], 3))
        print(colors.shape)
        for x in range(noise_grid.shape[0]):
            for y in range(noise_grid.shape[1]):
                colors[x, y] = pb.get_color_from_fertility(noise_grid[x, y])

        # scale color grid into pixel grid, distributing the colors into the correct scale
        scaled = np.kron(colors, np.ones((self.pixel_size, self.pixel_size, 1), dtype=float))
        assert scaled.shape[0] == self.width and scaled.shape[1] == self.height

        ferts = park.constructs.park_background.get_ferts()
        print("ferts: ", len(ferts))
        print("max", max(ferts))
        print("min", min(ferts))
        print("median", statistics.median(ferts))
        return scaled
