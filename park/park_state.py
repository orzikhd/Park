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
    tick_speed: How many ticks per second the park will run for
    """

    SIDE_SCREEN_WIDTH = 50
    BORDER = 2

    def __init__(self, grid_depth: int, pixel_size: int, tick_speed=60, sea_level=50):
        import park.park_util as pu
        from park.creatures.park_entity import ParkEntity

        # set all the boundary and scaling numbers
        self.grid_depth = grid_depth
        self.pixel_size = pixel_size
        self.tick_speed = tick_speed
        self.sea_level = sea_level
        self.grid_size = 2 ** grid_depth + 1  # Non-scaled length of one side of the park grid
        self.park_width = pixel_size * self.grid_size  # width of the park grid scaled by pixel size
        self.park_height = pixel_size * self.grid_size  # height of the park grid scaled by pixel size
        print("creating", self.park_width, "x", self.park_height, "park")

        self.side_screen_width = pixel_size * self.SIDE_SCREEN_WIDTH
        self.border = pixel_size * self.BORDER

        # init all the pygame objects
        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.park_width + self.side_screen_width + self.border,
             self.park_height))
        pygame.display.set_caption('P A R K')
        self.screen.fill(pu.PINK)

        self.park_screen: pygame.Surface = pygame.Surface((self.park_width, self.park_height))

        self.side_screen: pygame.Surface = pygame.Surface((self.side_screen_width, self.park_height))

        self.terrain_screen: pygame.Surface = pygame.Surface(self.park_screen.get_size())

        self.clock = pygame.time.Clock()

        # init all the state and tracking
        self.global_entities: Dict[int, ParkEntity] = {}
        self.global_sprite_counter = -1

        self.creature_tree = SpriteTree(self.global_entities)
        self.background_tree = SpriteTree(self.global_entities)

        # init the terrain
        self.terrain_grid, self.fertility_grid, self.topography = self._create_terrain()
        pygame.surfarray.blit_array(self.terrain_screen, self.terrain_grid)

    def init_screen(self):
        # init the screen
        self.park_screen.blit(self.terrain_screen, (0, 0))
        self.screen.blit(self.park_screen, (0, 0))
        self.update_screen([])

    def add_entity_to_park(self, entity, adding_function):
        """
        Creates a new entity in the park.

        :param entity - a ParkEntity to add to the park
        :param adding_function - a callback to trigger with the entity's new ID, for any custom logic
        :return unique ID for this entity
        """
        self.global_sprite_counter += 1
        self.global_entities[self.global_sprite_counter] = entity

        adding_function(self.global_sprite_counter)

        return self.global_sprite_counter  # return as a unique index given to this sprite just in case

    def remove_entity_from_park(self, entity, sprite_id):
        """
        Removes the given entity from the park.
        :param entity: entity to remove
        :param sprite_id: sprite ID for this entity as returned by the add function
        """
        if sprite_id in self.global_entities:
            del self.global_entities[sprite_id]

            self.creature_tree.tree.delete(sprite_id, entity.get_bounding_box())
            self.background_tree.tree.delete(sprite_id, entity.get_bounding_box())

    def update_entity_in_park(self, entity, sprite_id, old_box):
        """
        Updates an entity's location in the park.

        :param entity: entity to update
        :param sprite_id: sprite ID for this entity as returned by the add function
        :param old_box: the entity's old location
        """

        # the operation of deleting and inserting *looks* expensive, but timing it I found that
        # each call of this method is almost instant
        from park.creatures.creature import Creature

        if isinstance(entity, Creature):
            self.creature_tree.tree.delete(sprite_id, old_box)
            self.creature_tree.tree.insert(sprite_id, entity.get_bounding_box())
        else:
            # TODO some other sort of check
            self.background_tree.tree.delete(sprite_id, old_box)
            self.background_tree.tree.insert(sprite_id, entity.get_bounding_box())

    def _update_border(self):
        import park.park_util as pu
        border_box = pygame.draw.rect(self.screen, pu.PINK, (self.park_width, 0, self.border, self.park_height))
        return [border_box]

    def _update_side_screen(self):
        import park.park_util as pu

        self.side_screen.fill(pu.WHITE)
        font = pygame.font.Font(None, pu.TITLE_FONT_SIZE)
        text = font.render("HELLO, PARK", 1, pu.BLACK)
        self.side_screen.blit(text, text.get_rect(centerx=self.side_screen.get_width() / 2))

        font = pygame.font.Font(None, pu.INFO_FONT_SIZE)
        text_lines = [
            "Run Stats",
            f"Current FPS: {self.clock.get_fps():.2f}",
            f"Current Time: {pygame.time.get_ticks()}",
        ]
        label = [font.render(line, 1, pu.BLACK) for line in text_lines]
        label_margin = 10
        # each text line is rendered on the screen with its Y varying on its position in the list plus a margin
        for line in range(len(label)):
            self.side_screen.blit(label[line],
                                  label[line].get_rect(centerx=self.side_screen.get_width() / 2,
                                                       centery=self.side_screen.get_height() / 6
                                                       + line * pu.INFO_FONT_SIZE
                                                       + line * label_margin))

        # returning dirty rects of side screen to flip later
        return [self.screen.blit(self.side_screen, (self.border + self.park_width, 0))]

    def update_screen(self, dirty_rects):
        """
        Wrapper over pygame.display.update to update any passed in "dirty rects" or stale areas of the screen.
        Also updates any other areas of the screen that are related to the state but not part of the park.
        """
        # pygame.display.update(dirty_rects + self._update_side_screen() + self._update_border())
        self._update_side_screen() + self._update_border()
        pygame.display.flip()  # seems like its faster to just update the whole screen than to do it by rects

    def _create_terrain(self):
        import park.constructs.terrain as pt
        import park.park_util as pu

        noise_grid = pu.time_and_log(
            lambda: park.diamond_square.DiamondSquare(self.grid_size)
            .create_diamond_square_map(low_val=0, high_val=100),
            "Time to generate noise grid:")

        # scale noise grid into fertility grid
        scaled_fertility = np.kron(noise_grid, np.ones((self.pixel_size, self.pixel_size), dtype=float))
        assert scaled_fertility.shape[0] == self.park_width and scaled_fertility.shape[1] == self.park_height

        # convert noise grid into color grid
        colors = np.zeros((noise_grid.shape[0], noise_grid.shape[1], 3))

        for x in range(noise_grid.shape[0]):
            for y in range(noise_grid.shape[1]):
                colors[x, y] = pt.get_color_from_fertility(noise_grid[x, y])

        # scale color grid into pixel grid, distributing the colors into the correct scale
        scaled_colors = np.kron(colors, np.ones((self.pixel_size, self.pixel_size, 1), dtype=float))
        assert scaled_colors.shape[0] == self.park_width and scaled_colors.shape[1] == self.park_height

        # import statistics
        # ferts = park.constructs.terrain.get_ferts()
        # print("ferts: ", len(ferts))
        # print("max", max(ferts))
        # print("min", min(ferts))
        # print("median", statistics.median(ferts))

        # add water
        height_grid = pu.time_and_log(
            lambda: park.diamond_square.DiamondSquare(self.grid_size)
            .create_diamond_square_map(low_val=0, high_val=100),
            "Time to generate height grid:")
        # relax height to smooth it out
        self._relax_grid(height_grid, times=3)

        scaled_height = np.kron(height_grid, np.ones((self.pixel_size, self.pixel_size), dtype=float))
        assert scaled_height.shape[0] == self.park_width and scaled_height.shape[1] == self.park_height

        for x in range(self.park_width):
            for y in range(self.park_height):
                if scaled_height[x, y] < self.sea_level:
                    # print(scaled_height[x, y])
                    scaled_colors[x, y] = pt.put_color_underwater(scaled_colors[x, y])

        return scaled_colors, scaled_fertility, scaled_height

    @staticmethod
    def _relax_grid(grid, times=1):
        """
        Relaxes the values in a grid.

        This is basically making each value to be the average of values around it.
        :param grid: grid to relax
        :param times: how many times to relax it
        :return:
        """
        for time in range(times):
            for x in range(grid.shape[0] - 1):
                for y in range(grid.shape[1] - 1):
                    grid[x, y] = (grid[x, y]
                                  + grid[x - 1, y]
                                  + grid[x + 1, y]
                                  + grid[x, y - 1]
                                  + grid[x, y + 1]) / 5
