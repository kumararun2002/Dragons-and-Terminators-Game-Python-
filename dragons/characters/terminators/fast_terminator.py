from .terminator import Terminator


class FastTerminator(Terminator):
    """Class of terminator that is capable of taking two actions per turn, although
    its overall damage output is lower. Immune to status effects.
    """
    name = 'FastTerminator'
    damage = 0.25

    def action(self, colony):
        for i in range(2):
            if self.armor > 0:
                super().action(colony)

    def __setattr__(self, name, value):
        if name != 'action':
            object.__setattr__(self, name, value)
