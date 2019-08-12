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

    def check_collision(self, creature, proposed_rect, ignore_self):
        collisions = list(self.tree.intersection(creature.get_bounding_box(proposed_rect)))
        if ignore_self and creature.sprite_id in collisions:
            collisions.remove(creature.sprite_id)

        if collisions:
            # print(collisions)
            pass

        for collision in collisions:
            # print("collision: ", collision)
            collided_sprite = self.global_sprites[collision]

            # pycharm's collision check doesn't count it as a collision if the boundaries overlap
            # this is preferred behavior so that creatures can touch
            if collided_sprite.rect.colliderect(proposed_rect):
                # print("collided!")
                return True

        # print("all good")
        return False
