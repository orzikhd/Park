import random


class Spreads:
    """
    A creature that spreads is stationary
    and concerned only with its surrounding squares
    and what other spreaders are in them

    screen: a pygame surface that the spreader is drawn on
    fertility: the spreader's fertility, between 0 and 1
    rect: the spreader's rect, which doesn't move
    """
    def __init__(self, screen, fertility, rect):
        self.screen = screen
        self.fertility = fertility
        self.rect = rect

    def should_spread(self):
        return random.random() < self.fertility

    def get_neighboring_squares(self):
        possible_squares = \
            {self.rect.topright,  # right
                self.rect.bottomleft,  # down
                (self.rect.left - self.rect.width, self.rect.top),  # left
                (self.rect.left, self.rect.top - self.rect.height)  # up
             }

        for square in list(possible_squares):
            if square[0] < 0 \
                    or square[0] >= self.screen.get_rect().right \
                    or square[1] < 0 \
                    or square[1] >= self.screen.get_rect().bottom:
                possible_squares.remove(square)
        # print(possible_squares)
        return list(possible_squares)
