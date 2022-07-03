import heapq
import math
from dataclasses import dataclass, field
from typing import Any, Tuple

import pygame

from park.park_util import WHITE
from park.rect_util import get_rect_offset, offset_to_l1_distance

OCTAGON_ANGLE_DIFF = 45
OCTAGON_ANGLES = [OCTAGON_ANGLE_DIFF * i for i in range(8)]


@dataclass(order=True)
class SeenEntity:
    l1_distance: int  # sort sprites by their L1 distance from the Seeing creature
    entity: Any = field(compare=False)
    offset: Tuple[int, int] = field(compare=False)


def _offset_to_distance(offset):
    return offset_to_l1_distance(offset)  # just L1 distance for now


class Sees:
    """
    A creature that sees has a sense of what entities are within its vision in the park.
    """

    def __init__(self, creature, viewing_distance, see_background=True):
        from park.creatures.creature import Creature
        self.creature: Creature = creature
        self.viewing_distance = viewing_distance
        self.see_background = see_background
        # TODO the view polygon should probably just be passed in somehow

    def _get_box_collisions(self, bounding_box):
        res = set(self.creature.state.creature_tree.get_all_collisions(
            self.creature,
            bounding_box,
            ignore_self=True))
        if self.see_background:
            return res.union(set(self.creature.state.background_tree.get_all_collisions(
                self.creature,
                bounding_box,
                ignore_self=True)))
        return res

    def update_seen_entity(self, seen_entity: SeenEntity):
        """
        Update the seen entity to have the latest distance info.

        TODO shouldn't be able to do this if the entity is outside viewing distance
        """
        seen_entity.offset = get_rect_offset(self.creature.rect, seen_entity.entity.rect)
        seen_entity.l1_distance = _offset_to_distance(seen_entity.offset)

    def see(self, searching_behavior) -> SeenEntity:
        """
        The creature sees.
        :param searching_behavior: this function should take a list typing.List[SeenEntity] and
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
            collided_entity = self.creature.state.global_entities[collision]
            offset = get_rect_offset(self.creature.rect, collided_entity.rect)
            heapq.heappush(seen_sprites_heap, SeenEntity(_offset_to_distance(offset), collided_entity, offset))

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
            collided_entity = self.creature.state.global_entities[collision]

            # some silly logic for getting the sprites within the view polygon using pygame
            # involving a pixel by pixel mask of the collided_sprite and overlapping it with the self.creature
            collision_surface = pygame.Surface((collided_entity.rect.width,
                                                collided_entity.rect.height), pygame.SRCALPHA)
            collision_surface.fill(WHITE)  # the color is arbitrary, just fills 1s in the mask
            collision_mask = pygame.mask.from_surface(collision_surface)
            collision_offset = collided_entity.rect[0] - bounding_box[0], collided_entity.rect[1] - bounding_box[1]
            exists_intersection = viewing_mask.overlap(collision_mask, collision_offset)

            if exists_intersection:
                offset = get_rect_offset(self.creature.rect, collided_entity.rect)
                heapq.heappush(seen_sprites_heap, SeenEntity(_offset_to_distance(offset), collided_entity, offset))

        # if len(seen_sprites_heap) > 10: print(f"h  {len(seen_sprites_heap)}")
        return searching_behavior(seen_sprites_heap)
