from pygame.sprite import LayeredDirty


class LayeredDirtyCutoff(LayeredDirty):
    def __init__(self, cutoff, *sprites, **kwargs):
        super().__init__(*sprites, **kwargs)
        self.cutoff = cutoff

    def update(self, *args):
        """
        Call the update method of every member sprite, up to the cutoff

        Group.update(*args): return None

        Calls the update method of every member sprite. All arguments that
        were passed to this method are passed to the Sprite update function.

        """
        update_count = 0
        for s in self.sprites():
            if update_count > self.cutoff:
                # print("reached cutoff")
                return

            update_count += 1
            s.update(*args)
