import heapq
import math
from dataclasses import dataclass, field
from typing import Any, Tuple

import pygame

from park.creatures.park_entity import ParkEntity
from park.park_util import WHITE

OCTAGON_ANGLE_DIFF = 45
OCTAGON_ANGLES = [OCTAGON_ANGLE_DIFF * i for i in range(8)]


@dataclass(order=True)
class SeenSprite:
    l1_distance: int  # sort sprites by their L1 distance from the Seeing creature
    sprite: Any = field(compare=False)
    offset: Tuple[int, int] = field(compare=False)


def _offset_to_distance(offset):
    return abs(offset[0]) + abs(offset[1])  # just L1 distance for now


class Sees:
    """
    A creature that sees has a sense of what entities are within its vision in the park.
    """

    def __init__(self, creature, viewing_distance):
        from park.creatures.creature import Creature
        self.creature: Creature = creature
        self.viewing_distance = viewing_distance
        # TODO the view polygon should probably just be passed in somehow

    def _get_box_collisions(self, bounding_box):
        return set(self.creature.state.background_tree.get_all_collisions(self.creature,
                                                                          bounding_box,
                                                                          ignore_self=True)) \
            .union(set(self.creature.state.creature_tree.get_all_collisions(self.creature,
                                                                            bounding_box,
                                                                            ignore_self=True)))

    def _get_sprite_offset(self, other_sprite: ParkEntity):
        """
        Determine the offset to another sprite, useful to know how to move towards it.
        """
        return other_sprite.rect.center[0] - self.creature.rect.center[0], \
               other_sprite.rect.center[1] - self.creature.rect.center[1]

    def update_seen_sprite(self, seen_sprite: SeenSprite):
        seen_sprite.offset = self._get_sprite_offset(seen_sprite.sprite)
        seen_sprite.l1_distance = _offset_to_distance(seen_sprite.offset)

    def see(self, searching_behavior):
        """
        The creature sees.
        :param searching_behavior: this function should take a list typing.List[SeenSprite] and
        peruse it for its goal. If it picks a sprite, it should return it, otherwise return None.
        :return: this creature's picked sprite, or None if it didn't find one
        """
        # TODO find a way to optimize this
        center_point = self.creature.rect.center
        center_x = center_point[0]
        center_y = center_point[1]
        seen_sprites_heap = []

        # construct a bounding box of size viewing_distance for querying the tree index to get rough collisions
        bounding_box = pygame.Rect(center_x - self.viewing_distance,
                                   center_y - self.viewing_distance,
                                   self.viewing_distance * 2,
                                   self.viewing_distance * 2)

        # TODO remove when done debug drawing
        # print("made viewing intersection bounding box", bounding_box)
        self.bounding_box = bounding_box

        points = [(center_x + self.viewing_distance * math.cos(math.radians(angle)),
                   center_y + self.viewing_distance * math.sin(math.radians(angle)))
                  for angle in OCTAGON_ANGLES]
        self.points = points
        # print("made octagon points", points)
        # TODO remove when done debug drawing

        # the inner box is guaranteed to be within the collision polygon, as long as its somewhat of a "Zonogon"
        # so let's try finding what we're looking for there first
        inner_box = pygame.Rect(center_x - self.viewing_distance / 4,
                                center_y - self.viewing_distance / 4,
                                self.viewing_distance / 2,
                                self.viewing_distance / 2)
        inner_collisions = self._get_box_collisions(inner_box)

        for collision in inner_collisions:
            collided_sprite = self.creature.state.global_sprites[collision]
            offset = self._get_sprite_offset(collided_sprite)
            heapq.heappush(seen_sprites_heap, SeenSprite(_offset_to_distance(offset), collided_sprite, offset))

        picked_inner_sprite = searching_behavior(seen_sprites_heap)
        if picked_inner_sprite:
            # we found what we wanted in the inner box, don't need to strain our vision further
            # print("Inner find")
            return picked_inner_sprite

        # construct a view polygon with radius of viewing_distance
        # the points that make up the view polygon need to be centered such that
        # their bounding box (left,top) is (0,0) for the purposes of
        # drawing it into a mask for collision detection
        viewing_mask_offset_x = center_x - self.viewing_distance
        viewing_mask_offset_y = center_y - self.viewing_distance

        points = [(center_x + self.viewing_distance * math.cos(math.radians(angle)) - viewing_mask_offset_x,
                   center_y + self.viewing_distance * math.sin(math.radians(angle)) - viewing_mask_offset_y)
                  for angle in OCTAGON_ANGLES]

        collisions = self._get_box_collisions(bounding_box)

        # if len(collisions) > 10: print(f"c  {len(collisions)}")
        viewing_surface = pygame.Surface((self.viewing_distance * 2, self.viewing_distance * 2), pygame.SRCALPHA)
        pygame.draw.polygon(viewing_surface, WHITE, points)
        viewing_mask = pygame.mask.from_surface(viewing_surface)

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
                offset = self._get_sprite_offset(collided_sprite)
                heapq.heappush(seen_sprites_heap, SeenSprite(_offset_to_distance(offset), collided_sprite, offset))

        # if len(seen_sprites_heap) > 10: print(f"h  {len(seen_sprites_heap)}")
        return searching_behavior(seen_sprites_heap)
