import pygame

from pygame.compat import geterror
from pygame.locals import *


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except pygame.error:
        print ('Cannot load image:', name)
        raise SystemExit(str(geterror()))
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()



