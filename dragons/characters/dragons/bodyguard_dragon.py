from .dragon import Dragon


class BodyguardDragon(Dragon):
    """BodyguardDragon provides protection to other Dragons."""

    name = 'Bodyguard'
    food_cost=4
    armor=2
    implemented = True  # Change to True to view in the GUI
    is_container=True

    def __init__(self, armor=2):
        Dragon.__init__(self, armor)
        self.contained_dragon = None  # The Dragon hidden in this bodyguard

    def can_contain(self, other):
        if self.contained_dragon==None and other.is_container==False:
            return True
        else:
            return False

    def contain_dragon(self, dragon):
        # BEGIN 3.2
        self.contained_dragon=dragon
        # END 3.2

    def action(self, colony):
        # BEGIN 3.2
        if self.contained_dragon!=None:
            (self.contained_dragon).action(colony)
        # END 3.2
