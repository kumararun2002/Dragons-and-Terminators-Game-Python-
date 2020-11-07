from .thrower_dragon import ThrowerDragon


class LaserDragon(ThrowerDragon):
    # This class is optional. Only one test is provided for this class.

    name = 'Laser'
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN 4.5
    implemented = True  # Change to True to view in the GUI
    food_cost=10
    # END 4.5

    def __init__(self, armor=1):
        ThrowerDragon.__init__(self, armor)
        self.fighters_shot = 0
        self.damage=2

    def fighters_in_front(self, skynet):
        # BEGIN 4.5
        figh={}
        dist=0
        k=self.place
        while k!=skynet:
            
            if k.dragon!=None :
                if dist!=0:
                    figh.update({k.dragon:dist})
            for t in k.terminators:
                if t!=None:
                    figh.update({t:dist})
            k=k.entrance
            dist+=1
        return figh
        # END 4.5

    def calculate_damage(self, distance):
        # BEGIN 4.5
        dam=self.damage-0.2*distance-0.05*self.fighters_shot
        if dam>0:
            return dam
        else:
            return 0
        # END 4.5

    def action(self, colony):
        fighters_and_distances = self.fighters_in_front(colony.skynet)
        for fighter, distance in fighters_and_distances.items():
            damage = self.calculate_damage(distance)
            fighter.reduce_armor(damage)
            if damage:
                self.fighters_shot += 1
