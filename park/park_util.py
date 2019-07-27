import time
import warnings

import numpy as np
import pygame
from pygame.compat import geterror
from pygame.locals import *

images = {}

# images are expected to be 20x20 pixels
CREATURE_IMAGE_SIZE = 20


def load_image(name, scaler=1, colorkey=None):
    if (name, scaler) in images:
        image = images[(name, scaler)]
    else:
        print("didnt triggered cache")
        try:
            image = pygame.image.load(name)
        except pygame.error:
            print('Cannot load image:', name)
            raise SystemExit(str(geterror()))
        image = image.convert_alpha()

        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        image = pygame.transform.scale(image, (int(image.get_size()[0] * scaler),
                                               int(image.get_size()[1] * scaler)))
    images[(name, scaler)] = image
    return image, image.get_rect()


def time_and_log(func, message):
    """
    Executes the given func and prints the message along with the time it ran in milliseconds.
    """
    start = time.time()
    res = func()
    end = time.time()
    print(message, (end - start) * 1000, "ms")
    return res


def convert_to_np(arr, size):
    """
    Converts a `sharedctypes.Array` into a 2d numpy array.
    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', RuntimeWarning)
        np_arr = np.reshape(np.ctypeslib.as_array(arr), (size, size))
    return np_arr
