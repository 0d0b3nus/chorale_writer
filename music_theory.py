class PitchClass(object):

    def __init__(self):
        pass


class Interval(object):

    def __init__(self):
        pass


class Key(object):

    def __init__(self):
        pass


class Chord(object):

    def __init__(self, scale_degree, quality, inversion):
        assert 1 <= scale_degree <= 7
        self.__scale_degree = scale_degree
        assert quality in ["m", "M", "M7", "7", "m7", "dim", "dim7",
                           "half-dim"]
        self.__quality = quality
        assert inversion in [0, 1, 2, 3]
        self.__inversion = inversion

    def four_voice_realizations(self, key):
        pass
    """ Returns a list of realizations of the chord as 4 pitch classes

    We can get multiple results because we may have choice which pitch to
    double. The doublings are in descending order of appropriateness for
    voice leading. The first pitch is always the root, the rest are arbitrary.

    """


class ChordProgression(object):

    def __init__(self):
        pass
