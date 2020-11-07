from .dragon import Dragon


class DragonRemover(Dragon):
    """Allows the player to remove dragons from the board in the GUI."""

    name = 'Remover'
    implemented = False

    def __init__(self):
        Dragon.__init__(self, 0)
