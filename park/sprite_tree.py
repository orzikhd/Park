from typing import Dict

from rtree import index


class SpriteTree:
    """
    A wrapper around an R-Tree to provide park-relevant functions
    """

    def __init__(self, global_sprites):
        from park.creatures.park_entity import ParkEntity
        self.tree = index.Index()
        self.global_sprites: Dict[int, ParkEntity] = global_sprites

    def check_spawning_collision(self, creature, proposed_rect):
        return self.check_collision(creature, proposed_rect, ignore_self=False)

    def check_moving_collision(self, creature, proposed_rect):
        return self.check_collision(creature, proposed_rect, ignore_self=True)

    def get_nearest_creatures(self, creature, num_creatures=1):
        # because the creature itself will always be the closest thing when we use its rect as
        # the bounding box in the rtree, we increment the number of neighbors we want
        # and then remove the creature from the list returned
        nearest_creature_ids = list(self.tree.nearest(creature.get_bounding_box(), num_creatures + 1))
        nearest_creature_ids.remove(creature.sprite_id)
        return [self.global_sprites[c_id] for c_id in nearest_creature_ids]

    def get_all_collisions(self, creature, proposed_rect, ignore_self):
        collisions = list(self.tree.intersection(creature.get_bounding_box(proposed_rect)))
        if ignore_self and creature.sprite_id in collisions:
            collisions.remove(creature.sprite_id)

        return collisions

    def check_collision(self, creature, proposed_rect, ignore_self):
        collisions = self.get_all_collisions(creature, proposed_rect, ignore_self)

        for collision in collisions:
            collided_sprite = self.global_sprites[collision]

            # pycharm's collision check doesn't count it as a collision if the boundaries overlap
            # this is preferred behavior so that creatures can touch
            if collided_sprite.rect.colliderect(proposed_rect):
                return True

        return False
