import math

from pygame.rect import Rect


def get_rect_offset(rect1: Rect, rect2: Rect):
    """
    Determine the offset between rects.
    """
    return rect2.center[0] - rect1.center[0], \
        rect2.center[1] - rect1.center[1]


def rect_distance(rect1: Rect, rect2: Rect):
    """
    https://stackoverflow.com/questions/51807787/how-to-find-the-distance-between-sprites
    """
    x1, y1 = rect1.topleft
    x1b, y1b = rect1.bottomright
    x2, y2 = rect2.topleft
    x2b, y2b = rect2.bottomright
    left = x2b < x1
    right = x1b < x2
    top = y2b < y1
    bottom = y1b < y2
    if bottom and left:
        # print('bottom left')
        return math.hypot(x2b-x1, y2-y1b)
    elif left and top:
        # print('top left')
        return math.hypot(x2b-x1, y2b-y1)
    elif top and right:
        # print('top right')
        return math.hypot(x2-x1b, y2b-y1)
    elif right and bottom:
        # print('bottom right')
        return math.hypot(x2-x1b, y2-y1b)
    elif left:
        # print('left')
        return x1 - x2b
    elif right:
        # print('right')
        return x2 - x1b
    elif top:
        # print('top')
        return y1 - y2b
    elif bottom:
        # print('bottom')
        return y2 - y1b
    else:  # rectangles intersect
        # print('intersection')
        return 0.


def offset_to_l1_distance(offset):
    return abs(offset[0]) + abs(offset[1])

