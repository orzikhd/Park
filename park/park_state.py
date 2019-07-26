import time

import numpy as np
import pygame
from rtree import index

import park.diamond_square


class State:
    """
    A State does all the bookkeeping for the state of the Park.
    """

    GRID_DEPTH = 6  # This is the depth to run the symmetric dirt procedural generation
    PIXEL_SIZE = 10  # Scales the park, so a higher pixel size makes it more "zoomed in"
    GRID_SIZE = 2 ** GRID_DEPTH + 1  # Non-scaled length of one side of the park grid
    WIDTH = PIXEL_SIZE * GRID_SIZE  # width of the park grid scaled by pixel size
    HEIGHT = PIXEL_SIZE * GRID_SIZE  # height of the park grid scaled by pixel size

    def __init__(self):
        self.screen: pygame.Surface = pygame.display.set_mode((State.WIDTH, State.HEIGHT))
        self.terrain_screen: pygame.Surface = pygame.Surface(self.screen.get_size())
        self.clock = pygame.time.Clock()
        self.global_sprites = {}
        self.global_sprite_tree = index.Index()
        self.global_sprite_counter = -1

        # self.background_group = self._create_background()
        # self.background_list = self.background_group.sprites()
        # self.background_tree = spatial.KDTree([b.rect.center for b in self.background_list])
        self.terrain_grid, self.fertility_grid = self._create_terrain()

        pygame.surfarray.blit_array(self.terrain_screen, self.terrain_grid)
        self.screen.blit(self.terrain_screen, (0, 0))
        pygame.display.update()

    def add_sprite_to_park(self, sprite):
        self.global_sprite_counter += 1
        self.global_sprites[self.global_sprite_counter] = sprite
        self.global_sprite_tree.insert(self.global_sprite_counter, sprite.get_bounding_box())
        return self.global_sprite_counter  # return as a unique index given to this sprite just in case

    def remove_sprite_from_park(self, sprite, sprite_id):
        del self.global_sprites[sprite_id]
        self.global_sprite_tree.delete(sprite_id, sprite.get_bounding_box())

    def update_sprite_in_park(self, sprite, sprite_id, old_box):
        self.global_sprite_tree.delete(sprite_id, old_box)
        self.global_sprite_tree.insert(sprite_id, sprite.get_bounding_box())

    @staticmethod
    def _create_terrain():
        import park.constructs.terrain as pt
        import park.park_util as pu

        noise_grid = pu.time_and_log(
            lambda: park.diamond_square.DiamondSquare(State.GRID_SIZE).create_diamond_square_map(),
            "Time to generate noise grid:")

        # scale noise grid into fertility grid
        scaled_fertility = np.kron(noise_grid, np.ones((State.PIXEL_SIZE, State.PIXEL_SIZE), dtype=float))
        assert scaled_fertility.shape[0] == State.WIDTH and scaled_fertility.shape[1] == State.HEIGHT

        # convert noise grid into color grid
        colors = np.zeros((noise_grid.shape[0], noise_grid.shape[1], 3))

        for x in range(noise_grid.shape[0]):
            for y in range(noise_grid.shape[1]):
                colors[x, y] = pt.get_color_from_fertility(noise_grid[x, y])

        # scale color grid into pixel grid, distributing the colors into the correct scale
        scaled_colors = np.kron(colors, np.ones((State.PIXEL_SIZE, State.PIXEL_SIZE, 1), dtype=float))
        assert scaled_colors.shape[0] == State.WIDTH and scaled_colors.shape[1] == State.HEIGHT

        # ferts = park.constructs.park_background.get_ferts()
        # print("ferts: ", len(ferts))
        # print("max", max(ferts))
        # print("min", min(ferts))
        # print("median", statistics.median(ferts))
        return scaled_colors, scaled_fertility
