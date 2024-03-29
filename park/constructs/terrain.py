ferts = []


# debug functionality
def get_ferts():
    return ferts


# expects a raw value between 0 and 100 and transforms it into a fertility RGB color tuple
def get_color_from_fertility(fertility):
    transformed_fert = fertility/10
    ferts.append(transformed_fert)
    return Terrain.dirt_colors[min(int(transformed_fert), 9)]


def put_color_underwater(color_tuple):
    r, g, b = color_tuple
    return r * .4, g * .9, b * 1.3


class Terrain:
    # in order of increasing fertility
    dirt_colors = [(164, 158, 150),
                   (162, 148, 125),
                   (160, 138, 100),
                   (145, 120, 85),
                   (134, 110, 70),
                   (120, 92, 48),
                   (96, 70, 26),
                   (72, 54, 22),
                   (60, 42, 12),
                   (38, 26, 6)]
