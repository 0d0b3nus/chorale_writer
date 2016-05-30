from functools import total_ordering

class PitchClass(object):

    def __init__(self, letter, sharps=0, flats=0):
        if not 0 <= sharps <= 2 or not 0 <= flats <= 2:
            raise ValueError('No. of sharps/flats has to be between 0 and 2.')
        if sharps != 0 and flats !=0:
            raise ValueError('Cannot have sharps and flats.')
        if letter.upper() not in (chr(n) for n in range(ord('A'), ord('G')+1)):
            raise ValueError("Letter has to be a character "
            "between 'A' and 'G'")
        self.__letter = letter.upper()
        self.__sharps = sharps
        self.__flats = flats

    @property
    def letter(self):
        return self.__letter

    @property
    def sharps(self):
        return self.__sharps

    @property
    def flats(self):
        return self.__flats

    def __str__(self):
        string = self.letter
        sharps_dict = {0: '', 1: '♯', 2: '♯♯'}
        flats_dict = {0: '', 1: '♭', 2: '♭♭'}
        string += sharps_dict[self.sharps] + flats_dict[self.flats]
        return string

    def __eq__(self, other):
        return self.letter == other.letter and self.sharps == other.sharps \
                and self.flats == other.flats

    def enharmonic_equivalents(self):
        pass

    def is_enharmonic_to(self, other):
        return self in self.enharmonic_equivalents()

    @staticmethod
    def __prev_letter(letter):
        return chr(ord(letter) - 1) if letter != 'A' else 'G'

    @staticmethod
    def __next_letter(letter):
        return chr(ord(letter) + 1) if letter != 'G' else 'A'


@total_ordering
class Pitch(object):

    def __init__(self, pitch_class, octave):
        self.__pitch_class = pitch_class
        self.__octave = octave

    @property
    def pitch_class(self):
        return self.__pitch_class

    @property
    def octave(self):
        return self.__octave

    def interval_between(self, other):
        pass

    def __add__(self, other):
        assert isinstance(other, Interval), \
                "Can only add intervals to pitches."
        pass

    def __eq__(self, other):
        return self.pitch_class == other.pitch_class and \
            self.octave == self.octave

    def __lt__(self, other):
        pass

    def __str__(self):
        return str(self.pitch_class) + str(self.octave)

    def enharmonic_equivalent(self):
        pass

    def is_enharmonic_to(self, other):
        pass


@total_ordering
class Interval(object):

    def __init__(self, quality, number):
        valid_qualities = ('P', 'M', 'm', 'A', 'd')
        if quality not in valid_qualities:
            raise ValueError('Quality neds to be one of {}'.valid_qualities)
        self.__quality = quality
        if (quality in ('M', 'm') and self.__has_perfect_quality(number)):
            raise ValueError('{} does not have major/minor quality.')
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
        new_number = self.number + other.number - 1
        new_semitones = self.semitones + other.semitones

        if self.__has_perfect_quality(new_number):
            for quality in ('d', 'P', 'A'):
                candidate_interval = Interval(quality, new_number)
                if new_semitones == candidate_interval.semitones:
                    return candidate_interval
        else:
            for quality in ('d', 'm', 'M', 'A'):
                candidate_interval = Interval(quality, new_number)
                if new_semitones == candidate_interval.semitones:
                    return candidate_interval
        assert False, "{} or {} are invalid intervals".format(self, other)

    def __mul__(self, multiplicand):
        assert isinstance(multiplicand, int) and multiplicand >= 0, \
                "can only multiply by a nonnegative integer"
        result = Interval('P', 1)
        while multiplicand > 0:
            result += self
            multiplicand -= 1
        return result

    def __rmul__(self, multiplicand):
        return self.__mul__(multiplicand)

    def __str__(self):
        return "{}{}".format(self.quality, self.number)

    def inversion(self):
        """ Returns the inversion of the interval. """
        if self.is_compound():
            return self.simple_part().inversion()

        inverted_number = 9 - self.number
        inverted_quality = {'M': 'm', 'm': 'M', 'P': 'P', 'A': 'd', 'd': 'A'}
        return Interval(inverted_quality[self.quality], inverted_number)

    def enharmonic_equivalent(self):
        """ Returns the enharmonic equivalent of interval, if it exists.

        Returns none otherwise.
        """
        number = self.number
        quality = self.quality

        if quality == 'A':
            return Interval('d', number+1)
        elif quality == 'd':
            return Interval('A', number-1)
        return None

    def is_enharmonic_to(self, other):
        """ Determines if interval is enharmonically equivalent to another. """
        return self.semitones == other.semitones

    def is_compound(self):
        """ Determines if the interval is a compound interval.

        DBEND: We take the convention that all intervals STRICTLY bigger than
        perfect octaves are compound.
        """
        return self > Interval('P', 8)

    def simple_part(self):
        """ Returns the simple part of a compound interval. """
        number = self.number
        quality = self.quality
        number = number % 7 if number > 8 else number
        return Interval(quality, number)

    @classmethod
    def from_str(cls, string):
        pass

    @staticmethod
    def __has_perfect_quality(number):
        """ Returns whether number corresponds to potentially perfect interval

        i.e. a 1, 4 or 5 + octaves.
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
