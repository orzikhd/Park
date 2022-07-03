from collections import deque
from typing import Optional

from park.behaviors.sees import SeenEntity


class Remembers:
    """
    A creature that remembers can recall information about the board.

    Currently provided memory behaviors:
       - the creature has a deque of a certain size, which it can use to remember whatever it wants.
       - the creature has a current target that it recalls across ticks
    """
    def __init__(self, memory_size=0):
        self.target: Optional[SeenEntity] = None
        self.memory = deque(maxlen=memory_size)
