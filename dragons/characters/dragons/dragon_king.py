from .dragon import Dragon
from .scuba_thrower import ScubaThrower
from utils import terminators_win


class DragonKing(ScubaThrower):  # You should change this line
    # END 4.3
    """The King of the colony. The game is over if a terminator enters his place."""

    name = 'King'
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN 4.3
    implemented = True  # Change to True to view in the GUI
    food_cost=7
    is_watersafe=True
    instantiated=False

    # END 4.3

    def __init__(self, armor=1):
        # BEGIN 4.3
        self.armor=armor
        self.dradoub=[]
        if self.instantiated==False:
            DragonKing.instantiated=True
            self.imp=False
        else:
            self.imp=True
        # END 4.3

    def action(self, colony):
        """A dragon king throws a stone, but also doubles the damage of dragons
        in his tunnel.

        Impostor kings do only one thing: reduce their own armor to 0.
        """
        # BEGIN 4.3
        if self.imp==True:
            self.reduce_armor(self.armor)
        else:
            ScubaThrower.action(self,colony)
            k=self.place
            k=k.exit
            while k!=None:
                if k.dragon!=None:
                    if (k.dragon).is_container==False:
                        if k.dragon not in self.dradoub:
                            ((k.dragon).damage)*=2
                            (self.dradoub).append(k.dragon)
                    else:
                        if k.dragon not in self.dradoub:
                            ((k.dragon).damage)*=2
                            (self.dradoub).append(k.dragon)
                        if (k.dragon).contained_dragon!=None:
                            if (k.dragon).contained_dragon not in self.dradoub:
                                (((k.dragon).contained_dragon).damage)*=2
                                (self.dradoub).append((k.dragon).contained_dragon)
                k=k.exit
            
        # END 4.3

    def reduce_armor(self, amount):
        """Reduce armor by AMOUNT, and if the True DragonKing has no armor
        remaining, signal the end of the game.
        """
        # BEGIN 4.3
        Dragon.reduce_armor(self,amount)
        if self.imp==False:
            if self.armor<=0:
                terminators_win()
