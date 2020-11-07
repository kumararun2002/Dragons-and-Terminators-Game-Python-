from characters import Terminator, Mariatron, NinjaTerminator, FastTerminator, Boss


class AssaultPlan(dict):
    """The Terminators' plan of attack for the colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Terminators).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Terminator(3, None), Terminator(3, None)]}
    """

    def add_wave(self, terminator_type, terminator_armor, time, count):
        """Add a wave at time with count Terminators that have the specified armor."""
        terminators = [terminator_type(terminator_armor) for _ in range(count)]
        self.setdefault(time, []).extend(terminators)
        return self

    @property
    def all_terminators(self):
        """Place all Terminators in the skynet and return the list of Terminators."""
        return [terminator for wave in self.values() for terminator in wave]


def make_test_assault_plan():
    return AssaultPlan().add_wave(Terminator, 3, 2, 1).add_wave(Terminator, 3, 3, 1)


def make_easy_assault_plan():
    plan = AssaultPlan()
    for time in range(3, 16, 2):
        plan.add_wave(Terminator, 3, time, 1)
    plan.add_wave(Mariatron, 3, 4, 1)
    plan.add_wave(NinjaTerminator, 3, 8, 1)
    plan.add_wave(FastTerminator, 3, 12, 1)
    plan.add_wave(Boss, 15, 16, 1)
    return plan


def make_normal_assault_plan():
    plan = AssaultPlan()
    for time in range(3, 16, 2):
        plan.add_wave(Terminator, 3, time, 2)
    plan.add_wave(Mariatron, 3, 4, 1)
    plan.add_wave(NinjaTerminator, 3, 8, 1)
    plan.add_wave(FastTerminator, 3, 12, 1)
    plan.add_wave(Mariatron, 3, 16, 1)

    # Boss Stage
    for time in range(21, 30, 2):
        plan.add_wave(Terminator, 3, time, 2)
    plan.add_wave(Mariatron, 3, 22, 2)
    plan.add_wave(FastTerminator, 3, 24, 2)
    plan.add_wave(NinjaTerminator, 3, 26, 2)
    plan.add_wave(FastTerminator, 3, 28, 2)
    plan.add_wave(Boss, 20, 30, 1)
    return plan


def make_hard_assault_plan():
    plan = AssaultPlan()
    for time in range(3, 16, 2):
        plan.add_wave(Terminator, 4, time, 2)
    plan.add_wave(FastTerminator, 4, 4, 2)
    plan.add_wave(Mariatron, 4, 8, 2)
    plan.add_wave(NinjaTerminator, 4, 12, 2)
    plan.add_wave(Mariatron, 4, 16, 2)

    # Boss Stage
    for time in range(21, 30, 2):
        plan.add_wave(Terminator, 4, time, 3)
    plan.add_wave(Mariatron, 4, 22, 2)
    plan.add_wave(FastTerminator, 4, 24, 2)
    plan.add_wave(NinjaTerminator, 4, 26, 2)
    plan.add_wave(FastTerminator, 4, 28, 2)
    plan.add_wave(Boss, 30, 30, 1)
    return plan


def make_extra_hard_assault_plan():
    plan = AssaultPlan()
    plan.add_wave(FastTerminator, 5, 2, 2)
    for time in range(3, 16, 2):
        plan.add_wave(Terminator, 5, time, 2)
    plan.add_wave(FastTerminator, 5, 4, 2)
    plan.add_wave(Mariatron, 5, 8, 2)
    plan.add_wave(NinjaTerminator, 5, 12, 2)
    plan.add_wave(Mariatron, 5, 16, 2)

    # Boss Stage
    for time in range(21, 30, 2):
        plan.add_wave(Terminator, 5, time, 3)
    plan.add_wave(Mariatron, 5, 22, 2)
    plan.add_wave(FastTerminator, 5, 24, 2)
    plan.add_wave(NinjaTerminator, 5, 26, 2)
    plan.add_wave(FastTerminator, 5, 28, 2)
    plan.add_wave(Boss, 30, 30, 2)
    return plan
