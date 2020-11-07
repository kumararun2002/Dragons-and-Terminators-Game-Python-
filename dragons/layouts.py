from places import Place, Water
from characters import Dragon


def dragon_types():
    """Return a list of all implemented Dragon classes."""
    all_dragon_types = []
    new_types = [Dragon]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_dragon_types.extend(new_types)
    return [t for t in all_dragon_types if t.implemented]


def wet_layout(king, register_place, tunnels=3, length=9, moat_frequency=3):
    """Register a mix of wet and and dry places."""
    for tunnel in range(tunnels):
        exit = king
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)


def dry_layout(king, register_place, tunnels=3, length=9):
    """Register dry tunnels."""
    wet_layout(king, register_place, tunnels, length, 0)
