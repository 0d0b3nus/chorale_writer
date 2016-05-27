from functools import total_ordering

class PitchClass(object):

    def __init__(self, pitch_class_str):
        assert 1 <= len(pitch_class_str) <= 3
        self.__pc = pitch_class_str.replace('b', '♭').replace('#', '♯')


class Pitch(object):

    def __init__(self, pitch_class_str):
        self.__pitchclass = None
        self.__octave = None


@total_ordering
class Interval(object):

    def __init__(self, quality, number):
        assert quality in ('P', 'M', 'm', 'A', 'd')
        self.__quality = quality
        self.__number = number

    @property
    def quality(self):
        return self.__quality

    @property
    def number(self):
        return self.__number

    @property
    def semitones(self):
        number = self.__number
        semitones = 0
        # Reduce to a simple interval
        while (number > 8):
            number -= 8
            semitones += 12

        # Reduce to a major or perfect interval
        if self.__quality == 'A':
            semitones += 1
        elif self.__quality == 'm':
            semitones -= 1
        elif self.__quality == 'd' and self.__number not in (4, 5, 8):
            semitones -= 2 # one to get to minor, one more to get to major
        elif self.__quality == 'd' and self.__number in (4, 5, 8):
            semitones -= 1

        # Handle major/perfect interval
        perfect_major_to_semitones = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9,
                7: 11, 8: 12}
        semitones += perfect_major_to_semitones[number]

        return semitones

    def __eq__(self, other):
        return self.quality == other.quality and self.number == other.number

    def __lt__(self, other):
        if self.number < other.number:
            return True
        else:
            return self.semitones < other.semitones

    def __add__(self):
        pass

    def __iadd__(self):
        pass

    def __str__(self):
        return "{}{}".format(self.quality, self.number)

    def inversion(self):
        pass

    def enharmonic_equivalent(self):
        pass

    def is_enharmonic_to(self, other):
        return self.semitones == other.semitones


class Key(object):

    def __init__(self):
        pass


class Chord(object):

    def __init__(self, scale_degree, quality, inversion):
        assert 1 <= scale_degree <= 7
        self.__scale_degree = scale_degree
        assert quality in ("m", "M", "M7", "7", "m7", "dim", "dim7",
                           "half-dim")
        self.__quality = quality
        assert inversion in [0, 1, 2, 3]
        self.__inversion = inversion

    @property
    def scale_degree(self):
        return self.__scale_degree

    @property
    def quality(self):
        return self.__quality

    @property
    def inversion(self):
        return self.__inversion

    def __eq__(self, other):
        return self.scale_degree == other.scale_degree and \
            self.quality == other.quality and \
            self.inversion == other.inversion

    def __str__(self):
        pass

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
