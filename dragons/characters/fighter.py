class Fighter:
    """A Fighter, the base class of Dragon and Terminator, has armor and a Place."""
    is_dragon = False
    damage = 0
    is_watersafe=False

    # ADD CLASS ATTRIBUTES HERE

    def __init__(self, armor, place=None):
        """Create a Fighter with an ARMOR amount and a starting PLACE."""
        self.armor = armor
        self.place = place  # set by Place.add_fighter and Place.remove_fighter

    def reduce_armor(self, amount):
        """Reduce armor by AMOUNT, and remove the fighter from its place if it
        has no armor remaining.

        >>> test_fighter = Fighter(5)
        >>> test_fighter.reduce_armor(2)
        >>> test_fighter.armor
        3
        """
        self.armor -= amount
        if self.armor <= 0:
            self.place.remove_fighter(self)
            self.death_callback()

    def action(self, colony):
        """The action performed each turn.

        colony -- The DragonColony, used to access game state information.
        """

    def death_callback(self):
        # overriden by the gui
        pass

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.armor, self.place)
