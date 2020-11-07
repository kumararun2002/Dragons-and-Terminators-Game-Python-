from .terminator import Terminator


class NinjaTerminator(Terminator):
    """A Terminator that cannot be blocked. Is capable of moving past all defenses to
    assassinate the King.
    """
    name = 'NinjaTerminator'

    def blocked(self):
        return False
