import math
import random
from multiprocessing import Pool, sharedctypes
from statistics import mean

import numpy as np

from park import park_util as pu


def mp_init(shared_array):
    global grid_array
    grid_array = shared_array


class DiamondSquare:
    """
    Does the DiamondSquare algorithm to procedurally generate a 2d grid of values.
    Totally based on code I found on the internet.

    :param size: size of the resulting square grid defined by the length of one side
    """
    def __init__(self, size):
        self.size = size

    def _diamond_square(self, left, top, right, bottom, rand_mag, pre_share=None):
        # expects the global grid_array to be initialized so the processes can share it
        # otherwise the pre_share should be set to use that instead
        if pre_share:
            # print("p")
            grid = pu.convert_to_np(pre_share, self.size)
        else:
            # print("e")
            grid = pu.convert_to_np(grid_array, self.size)

        x_center = math.floor((left + right) / 2)
        y_center = math.floor((top + bottom) / 2)

        center = (x_center, y_center)
        north = (x_center, top)
        south = (x_center, bottom)
        west = (left, y_center)
        east = (right, y_center)
        northwest = (left, top)
        northeast = (right, top)
        southwest = (left, bottom)
        southeast = (right, bottom)

        # * The **diamond** step populates the centre point by averaging the
        # values at the four corners and adding or subtracting a random amount
        # of noise.
        if grid[center] == 0:
            grid[center] = DiamondSquare.create_value([grid[northwest], grid[northeast],
                                                       grid[southwest], grid[southeast]], rand_mag)

        # * The **square** step populates the North, South, East and West points
        # by averaging the North West and North East values, the South East and
        # South East values, etc.
        if grid[north] == 0:
            grid[north] = DiamondSquare.create_value([grid[northwest], grid[northeast], grid[center]], rand_mag)

        if grid[south] == 0:
            grid[south] = DiamondSquare.create_value([grid[southwest], grid[southeast], grid[center]], rand_mag)

        if grid[west] == 0:
            grid[west] = DiamondSquare.create_value([grid[northwest], grid[southwest], grid[center]], rand_mag)

        if grid[east] == 0:
            grid[east] = DiamondSquare.create_value([grid[northeast], grid[southeast], grid[center]], rand_mag)

    def _ds_recurse(self, args):
        # Yes, recursion is technically a bad way to do this because memory overflow blah blah blah

        left, top, right, bottom, rand_mag = args

        x_center = math.floor((left + right) / 2)
        y_center = math.floor((top + bottom) / 2)

        self._diamond_square(left, top, right, bottom, rand_mag)

        # Once the centre point and the four side points are populated then,
        # provided there are no smaller regions left, split the current region
        # into four smaller regions and perform the diamond square algorithm
        # on them.
        if (right - left) > 2:
            rand_mag = math.floor(rand_mag * 2 ** -0.75)

            self._ds_recurse((left, top, x_center, y_center, rand_mag))
            self._ds_recurse((left, y_center, x_center, bottom, rand_mag))
            self._ds_recurse((x_center, top, right, y_center, rand_mag))
            self._ds_recurse((x_center, y_center, right, bottom, rand_mag))

    def create_diamond_square_map(self, low_val=0, high_val=100):
        """
        Runs DiamondSquare algorithm to get a 2d grid of values.
        Because of the algorithm's inherent bias towards the initial values,
        expect to see each grid biasing towards the values in the corners.

        :param low_val: minimum value that should appear in the resulting grid
        :param high_val: maximum value that should appear in the resulting grid
        :return: 2d grid of procedurally generated values
        """
        mid_value = math.floor((low_val + high_val) / 2)
        quarter_value = mid_value / 2
        three_quart_value = mid_value + mid_value / 2
        seed_options = [mid_value, mid_value, quarter_value, three_quart_value, three_quart_value, three_quart_value]

        # initialize grid with corners
        left = top = 0
        right = bottom = self.size - 1
        x_center = math.floor((left + right) / 2)
        y_center = math.floor((top + bottom) / 2)

        init_grid = np.zeros((self.size, self.size))
        init_grid[top, left] = random.choice(seed_options)
        init_grid[top, right] = random.choice(seed_options)
        init_grid[bottom, left] = random.choice(seed_options)
        init_grid[bottom, right] = random.choice(seed_options)

        tmp = np.ctypeslib.as_ctypes(init_grid.ravel())
        shared_array = sharedctypes.Array(tmp._type_, tmp, lock=False)

        # I found that there's a nice speed boost if you split the first recursion between four processes
        # but anything more than that gave diminishing returns.
        with Pool(processes=4, initializer=mp_init, initargs=(shared_array,)) as pool:
            # do first step
            self._diamond_square(left, top, right, bottom, mid_value, shared_array)

            pool.map(self._ds_recurse, [
                (left, top, x_center, y_center, mid_value),
                (left, y_center, x_center, bottom, mid_value),
                (x_center, top, right, y_center, mid_value),
                (x_center, y_center, right, bottom, mid_value)
            ])

        grid = pu.convert_to_np(shared_array, self.size)
        return grid

    @staticmethod
    def create_value(source_values, rand_mag):
        return mean(source_values) - (random.random() - 0.5) * rand_mag
