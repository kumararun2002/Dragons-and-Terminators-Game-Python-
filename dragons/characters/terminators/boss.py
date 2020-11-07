from .mariatron import Mariatron
from .fast_terminator import FastTerminator


class Boss(Mariatron, FastTerminator):
    """The leader of the terminators. Combines the high damage of the Mariatron along with
    status effect immunity of FastTerminators. Damage to the boss is capped up to 8
    damage by a single attack.
    """
    name = 'Boss'
    damage_cap = 8
    action = Mariatron.action

    def reduce_armor(self, amount):
        super().reduce_armor(self.damage_modifier(amount))

    def damage_modifier(self, amount):
        return amount * self.damage_cap / (self.damage_cap + amount)
