import numpy as np
import random
from statistics import mean
import math
from multiprocessing import Pool, sharedctypes
import warnings


def create_value(source_values, rand_mag):
    return mean(source_values) - (random.random() - 0.5) * rand_mag


def mp_init(shared_array):
    global grid_array
    grid_array = shared_array


def convert_to_np(arr, size):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', RuntimeWarning)
        np_arr = np.reshape(np.ctypeslib.as_array(arr), (size, size))
    return np_arr


class DiamondSquare:
    def __init__(self, size):
        print("hello world")
        self.size = size

    def diamond_square(self, left, top, right, bottom, rand_mag, pre_share=None):
        # expects the global grid to be initialized
        if pre_share:
            # print("p")
            grid = convert_to_np(pre_share, self.size)
        else:
            # print("e")
            grid = convert_to_np(grid_array, self.size)

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
            grid[center] = create_value([grid[northwest], grid[northeast],
                                         grid[southwest], grid[southeast]], rand_mag)

        # * The **square** step populates the North, South, East and West points
        # by averaging the North West and North East values, the South East and
        # South East values, etc.
        if grid[north] == 0:
            grid[north] = create_value([grid[northwest], grid[northeast], grid[center]], rand_mag)

        if grid[south] == 0:
            grid[south] = create_value([grid[southwest], grid[southeast], grid[center]], rand_mag)

        if grid[west] == 0:
            grid[west] = create_value([grid[northwest], grid[southwest], grid[center]], rand_mag)

        if grid[east] == 0:
            grid[east] = create_value([grid[northeast], grid[southeast], grid[center]], rand_mag)

    def ds_recurse(self, args):
        left, top, right, bottom, rand_mag = args
        # print("called")
        x_center = math.floor((left + right) / 2)
        y_center = math.floor((top + bottom) / 2)

        self.diamond_square(left, top, right, bottom, rand_mag)

        # Once the centre point and the four side points are populated then,
        # provided there are no smaller regions left, split the current region
        # into four smaller regions and perform the diamond square algorithm
        # on them.
        if (right - left) > 2:
            rand_mag = math.floor(rand_mag * 2 ** -0.75)

            self.ds_recurse((left, top, x_center, y_center, rand_mag))
            self.ds_recurse((left, y_center, x_center, bottom, rand_mag))
            self.ds_recurse((x_center, top, right, y_center, rand_mag))
            self.ds_recurse((x_center, y_center, right, bottom, rand_mag))

    def create_diamond_square_map(self, low_val=0, high_val=100):
        mid_value = math.floor((low_val + high_val) / 2)
        quarter_value = mid_value / 2
        three_quart_value = mid_value + mid_value / 2
        seed_options = [mid_value, mid_value, quarter_value, three_quart_value, three_quart_value]
        # seed_options = [mid_value]
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

        with Pool(processes=4, initializer=mp_init, initargs=(shared_array,)) as pool:
            # do first step
            self.diamond_square(left, top, right, bottom, mid_value, shared_array)

            res = pool.map(self.ds_recurse, [
                (left, top, x_center, y_center, mid_value),
                (left, y_center, x_center, bottom, mid_value),
                (x_center, top, right, y_center, mid_value),
                (x_center, y_center, right, bottom, mid_value)
            ])
            print("map res: ", res)
        # pool.join()

        grid = convert_to_np(shared_array, self.size)
        print(grid)
        return grid


'''
if __name__ == "__main__":
    all_mins = []
    all_maxs = []
    for i in range(40):
        minv, maxv = create_diamond_square_map(2 ** 5 + 1)
        all_mins.append(minv)
        all_maxs.append(maxv)

    print("f max: ", max(all_maxs))
    print("f min: ", min(all_mins))
'''
