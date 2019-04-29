from rtree import index


class State:
    def __init__(self):
        self.global_sprites = {}
        self.global_tree = index.Index()
        self.global_sprite_counter = -1

    def add_sprite_to_park(self, sprite):
        self.global_sprite_counter += 1
        self.global_sprites[self.global_sprite_counter] = sprite
        self.global_tree.insert(self.global_sprite_counter, sprite.get_bounding_box())
        return self.global_sprite_counter  # return the index given to this sprite just in case
