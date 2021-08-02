import heapq
import math
from dataclasses import dataclass, field
from typing import Any, Tuple

import pygame

from park.park_util import WHITE

OCTAGON_ANGLE_DIFF = 45
OCTAGON_ANGLES = [OCTAGON_ANGLE_DIFF * i for i in range(8)]


@dataclass(order=True)
class SeenSprite:
    l1_distance: int  # sort sprites by their L1 distance from the Seeing creature
    sprite: Any = field(compare=False)
    offset: Tuple[int, int] = field(compare=False)


class Sees:
    """
    A creature that sees has a sense of what entities are within its vision in the park.
    """

    def __init__(self, creature, viewing_distance):
        from park.creatures.creature import Creature
        self.creature: Creature = creature
        self.viewing_distance = viewing_distance
        # TODO the view polygon should probably just be passed in somehow

    def see(self):
        # TODO find a way to optimize this
        center_point = self.creature.rect.center
        center_x = center_point[0]
        center_y = center_point[1]

        # construct a bounding box of size viewing_distance for querying the tree index to get rough collisions
        bounding_box = pygame.Rect(center_x - self.viewing_distance,
                                   center_y - self.viewing_distance,
                                   self.viewing_distance * 2,
                                   self.viewing_distance * 2)
        # print("made viewing intersection bounding box", bounding_box)
        # TODO remove when done debug drawing
        self.bounding_box = bounding_box

        points = [(center_x + self.viewing_distance * math.cos(math.radians(angle)),
                   center_y + self.viewing_distance * math.sin(math.radians(angle)))
                  for angle in OCTAGON_ANGLES]
        self.points = points
        # print("made octagon points", points)
        # TODO remove when done debug drawing

        # construct a view polygon with radius of viewing_distance
        # the points that make up the view polygon need to be centered such that
        # their bounding box (left,top) is (0,0) for the purposes of
        # drawing it into a mask for collision detection
        viewing_mask_offset_x = center_x - self.viewing_distance
        viewing_mask_offset_y = center_y - self.viewing_distance

        points = [(center_x + self.viewing_distance * math.cos(math.radians(angle)) - viewing_mask_offset_x,
                   center_y + self.viewing_distance * math.sin(math.radians(angle)) - viewing_mask_offset_y)
                  for angle in OCTAGON_ANGLES]

        collisions =\
            set(self.creature.state.background_tree.get_all_collisions(self.creature,
                                                                       bounding_box,
                                                                       ignore_self=True))\
            .union(set(self.creature.state.creature_tree.get_all_collisions(self.creature,
                                                                            bounding_box,
                                                                            ignore_self=True)))
        # if len(collisions) > 10: print(f"c  {len(collisions)}")
        viewing_surface = pygame.Surface((self.viewing_distance*2, self.viewing_distance*2), pygame.SRCALPHA)
        pygame.draw.polygon(viewing_surface, WHITE, points)
        viewing_mask = pygame.mask.from_surface(viewing_surface)

        seen_sprites_heap = []

        for collision in collisions:
            collided_sprite = self.creature.state.global_sprites[collision]

            # some silly logic for getting the sprites within the view polygon using pygame
            # involving a pixel by pixel mask of the collided_sprite and overlapping it with the self.creature
            collision_surface = pygame.Surface((collided_sprite.rect.width,
                                                collided_sprite.rect.height), pygame.SRCALPHA)
            collision_surface.fill(WHITE)  # the color is arbitrary, just fills 1s in the mask
            collision_mask = pygame.mask.from_surface(collision_surface)
            collision_offset = collided_sprite.rect[0] - bounding_box[0], collided_sprite.rect[1] - bounding_box[1]
            exists_intersection = viewing_mask.overlap(collision_mask, collision_offset)

            if exists_intersection:
                offset = collided_sprite.rect.center[0] - center_x, collided_sprite.rect.center[1] - center_y
                heapq.heappush(seen_sprites_heap, SeenSprite(abs(offset[0]) + abs(offset[1]), collided_sprite, offset))

        # if len(seen_sprites_heap) > 10: print(f"h  {len(seen_sprites_heap)}")
        return seen_sprites_heap
