import random
from .place import Place


class Skynet(Place):
    """The Place from which the Terminators launch their assault.

    assault_plan -- An AssaultPlan; when & where terminators enter the colony.
    """

    def __init__(self, assault_plan):
        self.name = 'Skynet'
        self.assault_plan = assault_plan
        self.terminators = []
        for terminator in assault_plan.all_terminators:
            self.add_fighter(terminator)
        # The following attributes are always None for a Skynet
        self.entrance = None
        self.dragon = None
        self.exit = None

    def strategy(self, colony):
        exits = [p for p in colony.places.values() if p.entrance is self]
        for terminator in self.assault_plan.get(colony.time, []):
            terminator.move_to(random.choice(exits))
            colony.active_terminators.append(terminator)
