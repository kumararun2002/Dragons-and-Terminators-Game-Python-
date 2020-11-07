from .dragon import Dragon


class NinjaDragon(Dragon):
    """NinjaDragon does not block the path and damages all terminators in its place."""

    name = 'Ninja'
    damage = 1
    # OVERRIDE CLASS ATTRIBUTES HERE
    food_cost=5
    armor=1
    # BEGIN 2.4
    implemented = True  # Change to True to view in the GUI
    blocks_path=False

    # END 2.4

    def action(self, colony):
        # BEGIN 2.4
        t=(self.place.terminators)[:]
        for k in t:
            k.reduce_armor(self.damage)
