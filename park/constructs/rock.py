import random

from park.constructs.multisprite import Multisprite
from park.park_util import CREATURE_IMAGE_SIZE


def square(starting_position, size, scaler=1):
    pixel_size = CREATURE_IMAGE_SIZE * scaler
    return [(starting_position[0] + pixel_size * x,
             starting_position[1] + pixel_size * y) for y in range(size) for x in range(size)]


def horizontal_u_shaped(starting_position, size, scaler=1):
    pixel_size = CREATURE_IMAGE_SIZE * scaler
    rectangle = [(starting_position[0] + pixel_size * x,
                  starting_position[1] + pixel_size * y) for y in range(2) for x in range(size + 2)]
    for i in range(1, size + 1):
        rectangle.remove((starting_position[0] + pixel_size * i, starting_position[1] + pixel_size))
    return rectangle


def vertical_u_shaped(starting_position, size, scaler=1):
    pixel_size = CREATURE_IMAGE_SIZE * scaler
    rectangle = [(starting_position[0] + pixel_size * x,
                  starting_position[1] + pixel_size * y) for y in range(size + 2) for x in range(2)]
    for i in range(1, size + 1):
        rectangle.remove((starting_position[0] + pixel_size, starting_position[1] + pixel_size * i))
    return rectangle


rock_types = [square, horizontal_u_shaped, vertical_u_shaped]


def create_rock(screen, state, starting_position, size, scaler=1):
    rock_type = random.choice(rock_types)
    return Multisprite(screen, state, rock_type(starting_position, size, scaler))
