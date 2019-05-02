import pygame

from pygame.compat import geterror
from pygame.locals import *

images = {}


def load_image(name, scaler=1, colorkey=None):
    if name in images:
        image = images[name]
    else:
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
    return image, image.get_rect()
