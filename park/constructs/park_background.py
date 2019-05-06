ferts = []


def get_ferts():
    return ferts


def get_color_from_fertility(fertility):
    transformed_fert = fertility/100 * 10
    ferts.append(transformed_fert)
    return Background.dirt_colors[int(transformed_fert)]


class Background:
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

