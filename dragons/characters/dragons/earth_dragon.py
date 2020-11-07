from .dragon import Dragon

class EarthDragon(Dragon):
    name="Earth"
    food_cost=4
    implemented=True
    def __init__(self, armor=4):
        self.armor=armor
    
    pass
