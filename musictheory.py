from collections import namedtuple
from functools import total_ordering

import util

@total_ordering
class PitchClass(object):

    def __init__(self, letter, sharps=0, flats=0):
        if not 0 <= sharps <= 2 or not 0 <= flats <= 2:
            raise ValueError('No. of sharps/flats has to be between 0 and 2.')
        if sharps != 0 and flats != 0:
            raise ValueError('Cannot have both sharps and flats.')
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

    def class_number(self):
        """ Returns how many semitones above the C pitch class it is. """
        for class_number, equivalence_class in enumerate(equivalence_classes):
            if self in equivalence_class:
                return class_number

    def __str__(self):
        return self.letter + ('♯'*self.sharps) + ('♭'*self.flats)

    def __repr__(self):
        representation = "PitchClass('{}'".format(self.letter)
        if self.sharps:
            representation += ", sharps={}".format(self.sharps)
        elif self.flats:
            representation += ", flats={}".format(self.flats)
        representation += ")"
        return representation

    def __eq__(self, other):
        return self.letter == other.letter and self.sharps == other.sharps \
                and self.flats == other.flats

    def __hash__(self):
        return hash((type(self), self.letter, self.sharps, self.flats))

    def __lt__(self, other):
        if self.class_number() != other.class_number():
            return self.class_number() < other.class_number()
        else:
            return other.letter in (
                self.next_letter(self.letter),
                self.next_letter(self.next_letter(self.letter))
            )

    def __add__(self, interval):
        assert isinstance(interval, Interval), \
            "Can only add intervals to pitch classes."

        interval = interval.simple_part()
        number = interval.number
        new_letter = self.letter
        while number > 1:
            new_letter = self.next_letter(new_letter)
            number -= 1

        new_class_number = (interval.semitones() + self.class_number()) % 12
        for pitch_class in equivalence_classes[new_class_number]:
            if pitch_class.letter == new_letter:
                return pitch_class
        pass


    def enharmonic_equivalents(self):
        """ Returns all pitch classes equivalent to self, except self. """
        for equivalence_class in equivalence_classes:
            if self in equivalence_class:
                return [pitch_class for pitch_class in equivalence_class
                        if pitch_class != self]

    def is_enharmonic_to(self, other):
        return other in self.enharmonic_equivalents()

    def interval_between(self, other):
        smaller, bigger = sorted([self, other])
        number = letter_classes.index(bigger.letter) \
                - letter_classes.index(smaller.letter) + 1
        semitones = bigger.class_number() - smaller.class_number()
        return Interval.from_number_and_semitones(number, semitones)

    @staticmethod
    def prev_letter(letter):
        return chr(ord(letter) - 1) if letter != 'A' else 'G'

    @staticmethod
    def next_letter(letter):
        return chr(ord(letter) + 1) if letter != 'G' else 'A'


# FIXME: Ugly as hell
letter_classes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
equivalence_classes = []
for letter in letter_classes:
    if letter in ('B', 'E'):
        equivalence_classes.append([
            PitchClass(PitchClass.prev_letter(letter), sharps=2),
            PitchClass(letter),
            PitchClass(PitchClass.next_letter(letter), flats=1)
        ])
    elif letter in ('C', 'F'):
        # white key
        equivalence_classes.append([
            PitchClass(PitchClass.prev_letter(letter), sharps=1),
            PitchClass(letter),
            PitchClass(PitchClass.next_letter(letter), flats=2)
        ])
        # black key
        equivalence_classes.append([
            PitchClass(letter, sharps=1),
            PitchClass(PitchClass.next_letter(letter), flats=1)
        ])
    else:
        # white key
        equivalence_classes.append([
            PitchClass(PitchClass.prev_letter(letter), sharps=2),
            PitchClass(letter),
            PitchClass(PitchClass.next_letter(letter), flats=2)
        ])
        # black key
        equivalence_classes.append([
            PitchClass(letter, sharps=1),
            PitchClass(PitchClass.next_letter(letter), flats=1)
        ])


@total_ordering
class Pitch(object):

    def __init__(self, pitch_class, octave):
        if isinstance(pitch_class, PitchClass):
            self.__pitch_class = pitch_class
        else:
            raise TypeError("First argument has to be a PitchClass.")
        if isinstance(octave, int):
            self.__octave = octave
        else:
            raise TypeError("Octave has to be an integer.")

    @property
    def pitch_class(self):
        return self.__pitch_class

    @property
    def octave(self):
        return self.__octave

    def interval_between(self, other):
        """ Returns the interval between this pitch and another. """
        smaller, bigger = sorted(self, other)
        octaves = bigger.octave - smaller.octave
        return octaves * Interval('P', 8) + \
                bigger.pitch_class.interval_between(smaller.pitch_class)

    def __add__(self, interval):
        assert isinstance(interval, Interval), \
                "Can only add intervals to pitches."
        new_octave = self.octave + interval.octaves()
        new_pitch_class = self.pitch_class + interval
        if new_pitch_class < self.pitch_class:
            new_octave += 1 # carry an octave
        return Pitch(new_pitch_class, new_octave)

    def __eq__(self, other):
        return self.pitch_class == other.pitch_class and \
            self.octave == other.octave

    def __hash__(self):
        return hash((type(self), self.pitch_class, self.octave))

    def __lt__(self, other):
        if self.octave != other.octave:
            return self.octave < other.octave
        else:
            return self.pitch_class < other.pitch_class

    def __str__(self):
        return str(self.pitch_class) + str(self.octave)

    def __repr__(self):
        return 'Pitch(' + repr(self.pitch_class) + \
               ', {}'.format(self.octave) + ')'

    def enharmonic_equivalent(self):
        """ Returns a list of all pitches self is enharmonic to, except self.
        """
        pass

    def is_enharmonic_to(self, other):
        """ Checks if self is enharmonicly equivalent to another pitch. """
        pass

    def to_midi(self):
        """ Returns the MIDI note value of the pitch, if possible.

        Otherwise, raises ValueError.
        """
        midi = 12 * (self.octave + 1) + self.pitch_class.class_number()
        if 0 <= midi <= 127:
            return midi
        else:
            raise ValueError('Pitch is not in MIDI range (C-1 to G9)')


@total_ordering
class Interval(object):

    def __init__(self, quality, number):
        valid_qualities = ('P', 'M', 'm', 'A', 'd')
        if quality not in valid_qualities:
            raise ValueError('Quality neds to be one of '
                             '{}'.format(valid_qualities))
        self.__quality = quality
        if quality in ('M', 'm') and self.__has_perfect_quality(number):
            raise ValueError('{} does not have major/minor '
                             'quality.'.format(number))
        elif quality == 'P' and not self.__has_perfect_quality(number):
            raise ValueError('{} does not have perfect '
                             'quality.'.format(number))
        if number <= 0 or not isinstance(number, int):
            raise ValueError('{} is not integer > 0'.format(number))
        self.__number = number

    @property
    def quality(self):
        return self.__quality

    @property
    def number(self):
        return self.__number

    def semitones(self):
        """ Returns how many semitones the interval contains. """

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

    def __hash__(self):
        return hash((type(self), self.quality, self.number))

    def __lt__(self, other):
        if self.number < other.number:
            return True
        else:
            return self.semitones() < other.semitones()

    def __add__(self, interval):
        assert isinstance(interval, Interval), \
            "Can only add another interval to an interval"
        new_number = self.number + interval.number - 1
        new_semitones = self.semitones() + interval.semitones()

        return Interval.from_number_and_semitones(new_number, new_semitones)

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
        """ Returns the enharmonic equivalent of the interval, if it exists.

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
        return self.semitones() == other.semitones()

    def is_compound(self):
        """ Determines if the interval is a compound interval.

        DBEND: We take the convention that all intervals STRICTLY bigger than
        perfect octaves are compound.
        """
        return self > Interval('P', 8)

    def octaves(self):
        """ Returns the number of perfect octaves contained in interval. """
        octaves = 0
        interval = self
        while interval.is_compound():
            interval = Interval(interval.quality, interval.number - 7)
            octaves += 1
        return octaves

    def simple_part(self):
        """ Returns the simple part of a compound interval. """
        number = self.number
        quality = self.quality
        number = number % 7 if number > 8 else number
        if number == 8 and quality == 'A':
            return Interval('A', 1)
        return Interval(quality, number)

    @classmethod
    def from_number_and_semitones(cls, number, semitones):
        """ Returns the interval with a given number and semitones. """
        if cls.__has_perfect_quality(number):
            qualities = ('d', 'P', 'A')
        else:
            qualities = ('d', 'm', 'M', 'A')

        for quality in qualities:
            candidate_interval = Interval(quality, number)
            if semitones == candidate_interval.semitones():
                return candidate_interval
        raise ValueError('No such interval exists.')

    @staticmethod
    def __has_perfect_quality(number):
        """ Returns whether number corresponds to potentially perfect interval

        i.e. a 1, 4 or 5 + octaves.
        """
        return number % 7 in [1, 4, 5]


class Key(object):

    def __init__(self, pitch_class, scale="M"):
        self.__tonic = pitch_class
        self.__scale = scale
        self.__degrees = self.__generate_degrees(pitch_class, scale)

    @property
    def tonic(self):
        return self.__tonic

    @property
    def scale(self):
        return self.__scale

    @property
    def degrees(self):
        return self.__degrees

    def __eq__(self, other):
        return self.tonic == other.tonic and self.scale == other.scale

    def __hash__(self):
        return hash((type(self), self.tonic, self.scale))

    @staticmethod
    def __generate_degrees(tonic, scale):
        major_pattern = "MMmMMMm"
        minor_pattern = "MmMMmMM"

        degrees = {1: tonic}
        pattern = major_pattern if scale == "M" else minor_pattern
        for n in range(2, 8):
            degrees[n] = degrees[n-1] + Interval(pattern[n-2], 2)
        return degrees

class Chord(object):

    __lowercase_qualities = frozenset(('m', 'm7', 'dim', 'dim7', 'half-dim'))
    __uppercase_qualities = frozenset(('M', 'M7', '7'))
    __non_roman_qualities = frozenset(('Fr', 'Ger', 'It', 'N'))
    __qualities = frozenset.union(__lowercase_qualities, __uppercase_qualities,
                                  __non_roman_qualities)

    __quality_to_interval_pattern = {
        'm': (Interval('m', 3), Interval('P', 5)),
        'M': (Interval('M', 3), Interval('P', 5)),
        'M7': (Interval('M', 3), Interval('P', 5), Interval('M', 7)),
        '7': (Interval('M', 3), Interval('P', 5), Interval('m', 7)),
        'm7': (Interval('m', 3), Interval('P', 5), Interval('m', 7)),
        'dim': (Interval('m', 3), Interval('d', 5)),
        'dim7': (Interval('m', 3), Interval('d', 5), Interval('d', 7)),
        'half-dim': (Interval('m', 3), Interval('d', 5), Interval('m', 7))}

    def __init__(self, scale_degree, quality, inversion, relative=None):
        assert 1 <= scale_degree <= 7
        self.__scale_degree = scale_degree
        assert quality in self.__qualities
        self.__quality = quality
        assert inversion in [0, 1, 2, 3]
        self.__inversion = inversion
        if relative:
            Relative = namedtuple('Relative', ['degree', 'scale'])
            self.__relative = Relative(relative[0], relative[1])
        else:
            self.__relative = None

    @property
    def scale_degree(self):
        return self.__scale_degree

    @property
    def quality(self):
        return self.__quality

    @property
    def inversion(self):
        return self.__inversion

    @property
    def relative(self):
        return self.__relative

    def __eq__(self, other):
        return self.scale_degree == other.scale_degree and \
            self.quality == other.quality and \
            self.inversion == other.inversion and \
            self.relative == other.relative

    def __hash__(self):
        return hash((type(self), self.scale_degree, self.quality,
                     self.inversion, self.relative))

    def __str__(self):
        result = ""
        # Base
        if self.quality in self.__uppercase_qualities:
            result += util.to_roman(self.scale_degree).upper()
        elif self.quality in self.__lowercase_qualities:
            result += util.to_roman(self.scale_degree).lower()
        else:
            result += self.quality

        quality_suffix = {'M7': ' M7', 'dim': '°', 'half-dim': 'ø',
                          'dim7': '°'}
        result += quality_suffix.get(self.quality, '')

        # Inversion
        if self.quality in ('M', 'm', 'dim'): # 3 note chords
            if self.inversion == 1:
                result += '⁶'
            elif self.inversion == 2:
                result += '⁶⁄₄'
        else: # 7th chords
            if self.inversion == 0 and self.quality not in ('M7', 'Ger', 'Fr'):
                result += '⁷'
            elif self.inversion == 1:
                result += '⁶⁄₅'
            elif self.inversion == 2:
                result += '⁴⁄₃'
            elif self.inversion == 3:
                result += '⁴⁄₂'

        # Relative
        if self.relative:
            relative_suffix = util.to_roman(self.relative.degree).upper()
            if self.relative.scale == 'm':
                relative_suffix = relative_suffix.lower()
            result += '/' + relative_suffix

        return result

    def pitch_classes(self, key):
        """ Returns a tuple of the pitch classes of the chord.

        The pitch classes are in order of ascending thirds.
        """
        if self.relative:
            actual_key = Key(key.degrees[self.relative.degree],
                             self.relative.scale)
            return Chord(self.scale_degree, self.quality,
                         self.inversion).pitch_classes(actual_key)

        classes = [key.degrees[self.scale_degree]]
        pattern = self.__quality_to_interval_pattern[self.quality]
        for interval in pattern:
            classes.append(classes[0] + interval)

        return tuple(classes)

    def equivalence_classes(self, key):
        return tuple(pitch_class.class_number() for pitch_class
                     in self.pitch_classes(key))

    def four_voice_realizations(self, key):
        """ Returns a tuple of realizations of the chord as 4 pitch classes.

        We can get multiple results because we may have choice which pitch to
        double. The doublings are in descending order of appropriateness for
        voice leading. The first pitch is always the bass, rest are arbitrary.
        """
        pass
