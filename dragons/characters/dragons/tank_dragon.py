from .bodyguard_dragon import BodyguardDragon


class TankDragon(BodyguardDragon):
    """TankDragon provides both offensive and defensive capabilities."""

    name = 'Tank'
    damage = 1
    # OVERRIDE CLASS ATTRIBUTES HERE
    food_cost=6
    armor=2
    # BEGIN 3.3
    implemented = True  # Change to True to view in the GUI

    # END 3.3
    def __init__(self, armor=2):
        BodyguardDragon.__init__(self, armor)
        self.contained_dragon = None
        
    def action(self, colony):
        # BEGIN 3.3
        k=(self.place).terminators[:]
        for i in k:
            i.reduce_armor(self.damage)
        if self.contained_dragon!=None:
            (self.contained_dragon).action(colony)
