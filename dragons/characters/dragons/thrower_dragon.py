from .dragon import Dragon
from utils import random_or_none


class ThrowerDragon(Dragon):
    """ThrowerDragon throws a stone each turn at the nearest Terminator in its range."""

    name = 'Thrower'
    implemented = True
    damage = 1

    # ADD/OVERRIDE CLASS ATTRIBUTES HERE
    food_cost=3
    armor=1
    min_range=None
    max_range=None

    def nearest_terminator(self, skynet):
        """Return the nearest Terminator in a Place that is not the SKYNET, connected to
        the ThrowerDragon's Place by following entrances.

        This method returns None if there is no such Terminator (or none in range).
        """
        # BEGIN 1.3 and 2.1
        count=0
        s=self.place
        m=self.place
        if self.min_range==None and self.max_range==None:
            while s!=skynet:
                k=random_or_none(s.terminators)
                if k!=None:
                    return k
                s=s.entrance
            else:
                return None
        elif self.min_range==None:
            while s!=skynet:
                if count<=self.max_range:
                    k=random_or_none(s.terminators)
                    if k!=None:
                        return k
                s=s.entrance
                count+=1
            else:
                return None
        elif self.max_range==None:
            while s!=skynet:
                if count>=self.min_range:
                    k=random_or_none(s.terminators)
                    if k!=None:
                        return k
                s=s.entrance
                count+=1
            else:
                return None
        else:
            while s!=skynet:
                if count>=self.min_range and count<=self.max_range:
                    k=random_or_none(s.terminators)
                    if k!=None:
                        return k
                s=s.entrance
                count+=1
            else:
                return None
        # END 1.3 and 2.1

    def throw_at(self, target):
        """Throw a stone at the TARGET Terminator, reducing its armor."""
        if target is not None:
            target.reduce_armor(self.damage)

    def action(self, colony):
        """Throw a stone at the nearest Terminator in range."""
        self.throw_at(self.nearest_terminator(colony.skynet))
