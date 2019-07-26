import typing
import random
import pygame

from park.creatures import creature
from park.park_state import State


class Bug(creature.Creature):
    IMAGE_LOCATION = 'park\\pictures\\bug.png'

    def __init__(self,
                 screen: pygame.Surface,
                 state: State,
                 starting_position: typing.Tuple[int, int],
                 scaler: float,
                 fertility: float,
                 speed: float):
        creature.Creature.__init__(self, screen, state, starting_position, scaler, fertility)
        self.tick = 0
        self.speed = speed

    def update(self):
        old_move = self.rect.move(0, 0)
        has_new_valid_spot = False

        while not has_new_valid_spot:
            self.rect = old_move
            x_speed = random.choice([self.speed, 0, -self.speed])
            y_speed = random.choice([self.speed, 0, -self.speed])
            new_move = self.rect.move(x_speed, y_speed)
            if new_move.left < 0 or new_move.right > self.state.WIDTH:
                new_move = self.rect.move(-x_speed, 0)

            if new_move.top < 0 or new_move.bottom > self.state.HEIGHT:
                new_move = self.rect.move(0, -2 * y_speed)

            # print("new move", new_move)

            if (x_speed == 0 and y_speed == 0) or \
                    not self._check_moving_collision(new_move, True):
                has_new_valid_spot = True
                self.rect = new_move

        # print(self.rect)

        # print("updating location from ", self.get_bounding_box(old_move), "to", self.get_bounding_box())
        self.state.update_sprite_in_park(self, self.sprite_id, self.get_bounding_box(old_move))
