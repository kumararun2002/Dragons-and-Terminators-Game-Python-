from collections import OrderedDict
from .throne import Throne
from utils import DragonsWinException, TerminatorsWinException


class DragonColony(object):
    """An dragon collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    places -- A list of all places in the colony (including a Skynet)
    terminator_entrances -- A list of places that terminators can enter
    """

    def __init__(self, strategy, skynet, dragon_types, create_places, dimensions,
                 food=2):
        """Create a DragonColony for simulating a game.

        Arguments:
        strategy -- a function to deploy dragons to places
        skynet -- a Skynet full of terminators
        dragon_types -- a list of dragon constructors
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout
        """
        self.time = 0
        self.food = food
        self.strategy = strategy
        self.skynet = skynet
        self.dragon_types = OrderedDict((a.name, a) for a in dragon_types)
        self.dimensions = dimensions
        self.active_terminators = []
        self.configure(skynet, create_places)

    def configure(self, skynet, create_places):
        """Configure the places in the colony."""
        self.base = Throne('DragonKing')
        self.places = OrderedDict()
        self.terminator_entrances = []

        def register_place(place, is_terminator_entrance):
            self.places[place.name] = place
            if is_terminator_entrance:
                place.entrance = skynet
                self.terminator_entrances.append(place)

        register_place(self.skynet, False)
        create_places(self.base, register_place, self.dimensions[0],
                      self.dimensions[1])

    def simulate(self):
        """Simulate an attack on the dragon colony (i.e., play the game)."""
        num_terminators = len(self.terminators)
        try:
            while True:
                self.strategy(self)  # Dragons deploy
                self.skynet.strategy(self)  # Terminators invade
                for dragon in self.dragons:  # Dragons take actions
                    if dragon.armor > 0:
                        dragon.action(self)
                for terminator in self.active_terminators[:]:  # Terminators take actions
                    if terminator.armor > 0:
                        terminator.action(self)
                    if terminator.armor <= 0:
                        num_terminators -= 1
                        self.active_terminators.remove(terminator)
                if num_terminators == 0:
                    raise DragonsWinException()
                self.time += 1
        except DragonsWinException:
            print('All terminators are vanquished. You win!')
            return True
        except TerminatorsWinException:
            print('The dragon king has perished. Please try again.')
            return False

    def deploy_dragon(self, place_name, dragon_type_name):
        """Place a dragon if enough food is available.

        This method is called by the current strategy to deploy dragons.
        """
        constructor = self.dragon_types[dragon_type_name]
        if self.food < constructor.food_cost:
            print('Not enough food remains to place ' + dragon_type_name)
        else:
            dragon = constructor()
            self.places[place_name].add_fighter(dragon)
            self.food -= constructor.food_cost
            return dragon

    def remove_dragon(self, place_name):
        """Remove a Dragon from the Colony."""
        place = self.places[place_name]
        if place.dragon is not None:
            place.remove_fighter(place.dragon)

    @property
    def dragons(self):
        return [p.dragon for p in self.places.values() if p.dragon is not None]

    @property
    def terminators(self):
        return [b for p in self.places.values() for b in p.terminators]

    @property
    def fighters(self):
        return self.dragons + self.terminators

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.dragons + self.terminators]) + status
