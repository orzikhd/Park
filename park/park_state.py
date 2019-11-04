from typing import Dict

import numpy as np
import pygame

import park.diamond_square
from park.sprite_tree import SpriteTree


class State:
    """
    A State does all the bookkeeping for the state of the Park.
    grid_depth: This is the depth to run the symmetric dirt procedural generation
    pixel_size: Scales the park, so a higher pixel size makes it more "zoomed in"
    """

    def __init__(self, grid_depth: int, pixel_size: int):
        from park.creatures.park_entity import ParkEntity

        # set all the boundary and scaling numbers
        self.grid_depth = grid_depth
        self.pixel_size = pixel_size
        self.grid_size = 2 ** grid_depth + 1  # Non-scaled length of one side of the park grid
        self.width = pixel_size * self.grid_size  # width of the park grid scaled by pixel size
        self.height = pixel_size * self.grid_size  # height of the park grid scaled by pixel size
        print("creating", self.width, "x", self.height, "park")

        # init all the pygame objects
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        self.terrain_screen: pygame.Surface = pygame.Surface(self.screen.get_size())
        self.clock = pygame.time.Clock()

        # init all the state and tracking
        self.global_sprites: Dict[int, ParkEntity] = {}
        self.global_sprite_counter = -1

        self.creature_tree = SpriteTree(self.global_sprites)
        self.background_tree = SpriteTree(self.global_sprites)

        # init the terrain
        self.terrain_grid, self.fertility_grid = self._create_terrain()
        pygame.surfarray.blit_array(self.terrain_screen, self.terrain_grid)
        self.screen.blit(self.terrain_screen, (0, 0))
        pygame.display.update()

    def add_entity_to_park(self, entity, adding_function):
        self.global_sprite_counter += 1
        self.global_sprites[self.global_sprite_counter] = entity

        adding_function(self.global_sprite_counter)

        return self.global_sprite_counter  # return as a unique index given to this sprite just in case

    def remove_entity_from_park(self, entity, sprite_id):
        del self.global_sprites[sprite_id]

        self.creature_tree.tree.delete(sprite_id, entity.get_bounding_box())
        self.background_tree.tree.delete(sprite_id, entity.get_bounding_box())

    def update_entity_in_park(self, entity, sprite_id, old_box):
        from park.creatures.creature import Creature

        if isinstance(entity, Creature):
            self.creature_tree.tree.delete(sprite_id, old_box)
            self.creature_tree.tree.insert(sprite_id, entity.get_bounding_box())
        else:
            # TODO some other sort of check
            self.background_tree.tree.delete(sprite_id, old_box)
            self.background_tree.tree.insert(sprite_id, entity.get_bounding_box())

    def _create_terrain(self):
        import park.constructs.terrain as pt
        import park.park_util as pu

        noise_grid = pu.time_and_log(
            lambda: park.diamond_square.DiamondSquare(self.grid_size).create_diamond_square_map(),
            "Time to generate noise grid:")

        # scale noise grid into fertility grid
        scaled_fertility = np.kron(noise_grid, np.ones((self.pixel_size, self.pixel_size), dtype=float))
        assert scaled_fertility.shape[0] == self.width and scaled_fertility.shape[1] == self.height

        # convert noise grid into color grid
        colors = np.zeros((noise_grid.shape[0], noise_grid.shape[1], 3))

        for x in range(noise_grid.shape[0]):
            for y in range(noise_grid.shape[1]):
                colors[x, y] = pt.get_color_from_fertility(noise_grid[x, y])

        # scale color grid into pixel grid, distributing the colors into the correct scale
        scaled_colors = np.kron(colors, np.ones((self.pixel_size, self.pixel_size, 1), dtype=float))
        assert scaled_colors.shape[0] == self.width and scaled_colors.shape[1] == self.height

        # ferts = park.constructs.park_background.get_ferts()
        # print("ferts: ", len(ferts))
        # print("max", max(ferts))
        # print("min", min(ferts))
        # print("median", statistics.median(ferts))
        return scaled_colors, scaled_fertility
