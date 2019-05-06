import numpy as np
import random
from statistics import mean
import math
import threading
import concurrent.futures


def create_value(source_values, rand_mag):
    return mean(source_values) - (random.random() - 0.5) * rand_mag


class DiamondSquare:
    def __init__(self):
        print("hello world")

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def diamond_square(self, executor, grid, left, top, right, bottom, rand_mag):
        # print("called")
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

        # Once the centre point and the four side points are populated then,
        # provided there are no smaller regions left, split the current region
        # into four smaller regions and perform the diamond square algorithm
        # on them.
        if (right - left) > 2:
            rand_mag = math.floor(rand_mag * 2 ** -0.75)

            '''
            if executor:
                print("parallelizing")
                res1 = executor.submit(self.diamond_square, None, grid, left, top, x_center, y_center, rand_mag)
                res2 = executor.submit(self.diamond_square, None, grid, left, y_center, x_center, bottom, rand_mag)
                res3 = executor.submit(self.diamond_square, None, grid, x_center, top, right, y_center, rand_mag)
                res4 = executor.submit(self.diamond_square, None, grid, x_center, y_center, right, bottom, rand_mag)
                res1.result()
                res2.result()
                res3.result()
                res4.result()
            else:
            '''
            self.diamond_square(None, grid, left, top, x_center, y_center, rand_mag)
            self.diamond_square(None, grid, left, y_center, x_center, bottom, rand_mag)
            self.diamond_square(None, grid, x_center, top, right, y_center, rand_mag)
            self.diamond_square(None, grid, x_center, y_center, right, bottom, rand_mag)
            '''
            '''
            '''
            res1 = self.pool.apply_async(self.diamond_square, [grid, left, top, x_center, y_center, rand_mag])
            res2 = self.pool.apply_async(self.diamond_square, [grid, left, y_center, x_center, bottom, rand_mag])
            res3 = self.pool.apply_async(self.diamond_square, [grid, x_center, top, right, y_center, rand_mag])
            res4 = self.pool.apply_async(self.diamond_square, [grid, x_center, y_center, right, bottom, rand_mag])
            res1.get()
            res2.get()
            res3.get()
            res4.get()
            '''
            # print(grid)

    def create_diamond_square_map(self, size, low_val=0, high_val=100):
        mid_value = math.floor((low_val + high_val) / 2)
        quarter_value = mid_value / 2
        three_quart_value = mid_value + mid_value / 2
        seed_options = [mid_value, mid_value, quarter_value, three_quart_value, three_quart_value]
        # seed_options = [mid_value]
        # initialize grid with corners
        grid = np.zeros((size, size), dtype=float)

        grid[0, 0] = random.choice(seed_options)
        grid[0, size - 1] = random.choice(seed_options)
        grid[size - 1, 0] = random.choice(seed_options)
        grid[size - 1, size - 1] = random.choice(seed_options)

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        self.diamond_square(None, grid, 0, 0, size - 1, size - 1, mid_value)

        print("generated diamond-square map of shape", grid.shape)
        print("max: ", np.amax(grid))
        print("min: ", np.amin(grid))
        # return np.amin(grid), np.amax(grid)
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
