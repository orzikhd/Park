import statistics
import time

import numpy as np
import pygame
from rtree import index

import park.diamond_square


class State:
    grid_depth = 7
    pixel_size = 5
    grid_size = 2 ** grid_depth + 1
    width = pixel_size * grid_size
    height = pixel_size * grid_size

    def __init__(self):
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        self.background_screen: pygame.Surface = pygame.Surface(self.screen.get_size())
        self.clock = pygame.time.Clock()
        self.global_sprites = {}
        self.global_sprite_tree = index.Index()
        self.global_sprite_counter = -1

        # self.background_group = self._create_background()
        # self.background_list = self.background_group.sprites()
        # self.background_tree = spatial.KDTree([b.rect.center for b in self.background_list])
        self.background_grid, self.fertility_grid = self._create_background()

        pygame.surfarray.blit_array(self.background_screen, self.background_grid)
        self.screen.blit(self.background_screen, (0, 0))
        pygame.display.update()

    def add_sprite_to_park(self, sprite):
        self.global_sprite_counter += 1
        self.global_sprites[self.global_sprite_counter] = sprite
        self.global_sprite_tree.insert(self.global_sprite_counter, sprite.get_bounding_box())
        return self.global_sprite_counter  # return the index given to this sprite just in case

    def remove_sprite_from_park(self, sprite, sprite_id):
        del self.global_sprites[sprite_id]
        self.global_sprite_tree.delete(sprite_id, sprite.get_bounding_box())

    def update_sprite_in_park(self, sprite, sprite_id, old_box):
        self.global_sprite_tree.delete(sprite_id, old_box)
        self.global_sprite_tree.insert(sprite_id, sprite.get_bounding_box())

    def _create_background(self):
        import park.constructs.park_background as pb

        start = time.time()

        noise_grid = park.diamond_square.DiamondSquare(self.grid_size).create_diamond_square_map()
        end = time.time()
        print("time to generate noise grid: ", (end - start) * 1000, "ms")

        # scale noise grid into fertility grid
        scaled_fertility = np.kron(noise_grid, np.ones((self.pixel_size, self.pixel_size), dtype=float))
        assert scaled_fertility.shape[0] == self.width and scaled_fertility.shape[1] == self.height

        # convert noise grid into color grid
        colors = np.zeros((noise_grid.shape[0], noise_grid.shape[1], 3))

        for x in range(noise_grid.shape[0]):
            for y in range(noise_grid.shape[1]):
                colors[x, y] = pb.get_color_from_fertility(noise_grid[x, y])

        # scale color grid into pixel grid, distributing the colors into the correct scale
        scaled_colors = np.kron(colors, np.ones((self.pixel_size, self.pixel_size, 1), dtype=float))
        assert scaled_colors.shape[0] == self.width and scaled_colors.shape[1] == self.height

        # ferts = park.constructs.park_background.get_ferts()
        # print("ferts: ", len(ferts))
        # print("max", max(ferts))
        # print("min", min(ferts))
        # print("median", statistics.median(ferts))
        return scaled_colors, scaled_fertility
