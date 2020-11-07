from .place import Place
from utils import TerminatorsWinException


class Throne(Place):
    """Throne at the end of the tunnel, where the king resides."""

    def add_fighter(self, fighter):
        """Add a Fighter to this Place.

        Can't actually add Dragons to a Throne. However, if a Terminator attempts to
        enter the Throne, a TerminatorsWinException is raised, signaling the end
        of a game.
        """
        assert not fighter.is_dragon, 'Cannot add {0} to Throne'
        raise TerminatorsWinException()
