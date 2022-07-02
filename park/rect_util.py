def get_rect_offset(rect1, rect2):
    """
    Determine the offset between rects.
    """
    return rect2.center[0] - rect1.center[0], \
        rect2.center[1] - rect1.center[1]


def offset_to_l1_distance(offset):
    return abs(offset[0]) + abs(offset[1])
