import math

import pygame


class Moves:
    """
    A creature that moves has its rect move around the Park and its image rotate.

    creature: the creature doing the moving
    """
    def __init__(self, creature):
        from park.creatures.creature import Creature
        self.creature: Creature = creature
        self.original_image = self.creature.image

    def move(self, deciding_function):
        """
        Moves the creature once.
        :param deciding_function: a function that should return a offset,angle tuple
        :return: True if the creature has moved, False otherwise
        """
        old_move = self.creature.rect.move(0, 0)
        offset, angle = deciding_function()
        x_offset = offset * math.cos(angle)
        y_offset = -offset * math.sin(angle)  # negative y_offset to account for reversed y axis
        new_move = self.creature.rect.move(x_offset, y_offset)

        if new_move.left < 0 or new_move.right > self.creature.state.WIDTH:
            new_move = self.creature.rect.move(-x_offset, y_offset)

        if new_move.top < 0 or new_move.bottom > self.creature.state.HEIGHT:
            new_move = self.creature.rect.move(x_offset, -y_offset)

        if (x_offset == 0 and y_offset == 0) or \
                not self.creature.state.creature_tree.check_moving_collision(self.creature, new_move):
            self.creature.rect = new_move
            rendering_angle = Moves.round_angle(math.degrees(angle))
            self.creature.image = pygame.transform.rotate(self.original_image, rendering_angle)

            # print("updating location from ", self.get_bounding_box(old_move), "to", self.get_bounding_box())
            self.creature.state.update_entity_in_park(self.creature,
                                                      self.creature.sprite_id,
                                                      self.creature.get_bounding_box(old_move))
            return True

        return False

    @staticmethod
    def round_angle(angle):
        return round(angle / 90.0) * 90
