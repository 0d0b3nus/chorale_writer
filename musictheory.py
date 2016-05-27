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
        assert not (quality in ('M', 'm') and self.__has_perfect_quality(number))
        self.__number = number

    @property
    def quality(self):
        return self.__quality

    @property
    def number(self):
        return self.__number

    @property
    def semitones(self):
        number = self.number
        semitones = 0
        # Reduce to a simple interval
        while number > 8:
            number -= 7
            semitones += 12

        # Reduce to a major or perfect interval
        if self.quality == 'A':
            semitones += 1
        elif self.quality == 'm':
            semitones -= 1
        elif self.quality == 'd' and not self.__has_perfect_quality(number):
            semitones -= 2 # one to get to minor, one more to get to major
        elif self.quality == 'd' and self.__has_perfect_quality(number):
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

    def __add__(self, other):
        pass

    def __iadd__(self, other):
        pass

    def __str__(self):
        return "{}{}".format(self.quality, self.number)

    def inversion(self):
        if self.is_compound():
            return self.simple_part().inversion()

        inverted_number = 9 - self.number
        inverted_quality = {'M': 'm', 'm': 'M', 'P': 'P', 'A': 'd', 'd': 'A'}
        return type(self)(inverted_quality[self.quality], inverted_number)

    def enharmonic_equivalent(self):
        number = self.number
        quality = self.quality

        if quality == 'A':
            return type(self)('d', number+1)
        elif quality == 'd':
            return type(self)('A', number-1)
        return None

    def is_enharmonic_to(self, other):
        return self.semitones == other.semitones

    def is_compound(self):
        return self.number > 8

    def simple_part(self):
        """ Returns the simple part of a compound interval """
        number = self.number
        quality = self.quality
        number = number % 7 if number > 8 else number
        return type(self)(quality, number)

    @classmethod
    def from_str(cls, string):
        pass

    @staticmethod
    def __has_perfect_quality(number):
        """ Returns whether number corresponds to potentially perfect interval

        i.e. a 1, 4 or 5 + octaves
        """
        return number % 7 in [1, 4, 5]


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
        """ Returns a list of realizations of the chord as 4 pitch classes

        We can get multiple results because we may have choice which pitch to
        double. The doublings are in descending order of appropriateness for
        voice leading. First pitch is always the root, rest are arbitrary.

        """
        pass


class ChordProgression(object):

    def __init__(self):
        pass
