from park.creatures.park_entity import ParkEntity
from park.rect_util import get_rect_offset, offset_to_l1_distance


class Chomps:
    """
    A creature that chomps can chomp/remove other entities from the Park.

    creature: the creature doing the chomping
    hungry_interval: how many seconds the creature goes between wanting to chomp
    chomp_reach: how many pixels the creature can reach to chomp
    """
    def __init__(self, creature, hungry_interval: int, chomp_reach: int):
        from park.creatures.creature import Creature
        self.creature: Creature = creature
        self.hungry_interval = hungry_interval
        self.chomp_reach = chomp_reach
        self.hunger = 0

    def hungry(self):
        """
        Ticks creature hunger
        :return: True if creature now hungry, False otherwise
        """
        self.hunger += 1
        return self.hunger > self.hungry_interval * self.creature.state.tick_speed

    def chomp(self, chomp_target: ParkEntity):
        """
        Attempts to chomp a creature.
        :param chomp_target: creature that this creature is targeting to chomp
        :return: True if was able to chomp, False otherwise
        """
        if not chomp_target.is_alive():
            # possible reasons for this?
            #   - two creatures target the same creature, one chomps first, second one can't
            print("Tried to eat something that was already dead :(")
            return False

        target_rect = chomp_target.rect
        if offset_to_l1_distance(
                get_rect_offset(self.creature.rect, target_rect)) > self.chomp_reach:
            # too far away to chomp!
            return False

        # TODO: validate that the food chain is being respected
        chomp_target.die()

        self.hunger = 0

        return True
