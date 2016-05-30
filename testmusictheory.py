import unittest

from musictheory import *


class TestPitchClasses(unittest.TestCase):

    def test_validate(self):
        self.assertRaises(ValueError, PitchClass('H'))
        self.assertRaises(ValueError, PitchClass('Bb'))
        self.assertRaises(ValueError, PitchClass('C', sharps=3))
        self.assertRaises(ValueError, PitchClass('A', flats=-1))
        self.assertRaises(ValueError, PitchClass('C', sharps=1, flats=1))

    def test_eq(self):
        self.assertEqual(PitchClass('C', sharps=1), PitchClass('C', sharps=1))
        pass

    def test_cmp(self):
        pass

    def test_interval_between(self):
        pass

class Pitch(unittest.TestCase):
        pass

class TestIntervals(unittest.TestCase):

    def test_validate(self):
        self.assertRaises(ValueError, Interval('P', 0))
        self.assertRaises(ValueError, Interval('G', 1))
        self.assertRaises(ValueError, Interval('M', 4))
        self.assertRaises(ValueError, Interval('P', 6))

    def test_eq(self):
        self.assertEqual(Interval('P', 5), Interval('P', 5))
        self.assertNotEqual(Interval('P', 5), Interval('d', 5))
        self.assertNotEqual(Interval('P', 5), Interval('P', 1))
        self.assertNotEqual(Interval('d', 5), Interval('A', 4))

    def test_str(self):
        self.assertEqual(str(Interval('P', 1)), "P1")
        self.assertEqual(str(Interval('m', 3)), "m3")
        self.assertEqual(str(Interval('M', 10)), "M10")
        self.assertEqual(str(Interval('A', 7)), "A7")

    def test_semitones(self):
        self.assertEqual(Interval('P', 5).semitones, 7)
        self.assertEqual(Interval('d', 5).semitones, 6)
        self.assertEqual(Interval('M', 3).semitones, 4)
        self.assertEqual(Interval('A', 7).semitones, 12)
        self.assertEqual(Interval('M', 10).semitones, 16)

    def test_add(self):
        self.assertEqual(Interval('d', 5) + Interval('A', 4), Interval('P', 8))

        chord = Interval('M', 3)
        chord += Interval('P', 8)
        self.assertEqual(chord, Interval('M', 10))

        self.assertEqual(Interval('M', 3) + Interval('M', 3), Interval('A', 5))

    def test_mult(self):
        perfect_union = Interval('P', 1)
        diminished_fifth = Interval('d', 5)
        diminished_ninth = Interval('d', 9)

        self.assertEqual(diminished_fifth * 0, perfect_union)
        self.assertEqual(diminished_fifth * 2, diminished_ninth)
        self.assertEqual(2 * diminished_fifth, diminished_ninth)

    def test_cmp(self):
        perfect_fifth = Interval('P', 5)
        diminished_fifth = Interval('d', 5)
        self.assertFalse(perfect_fifth <= diminished_fifth)
        self.assertFalse(perfect_fifth < diminished_fifth)
        self.assertTrue(perfect_fifth >= diminished_fifth)
        self.assertTrue(perfect_fifth >= diminished_fifth)
        self.assertTrue(perfect_fifth >= perfect_fifth)

        # Check strictness.
        self.assertFalse(perfect_fifth > perfect_fifth)

    def test_inversion(self):
        perfect_unison = Interval('P', 1)
        perfect_octave = Interval('P', 8)
        self.assertEqual(perfect_octave.inversion(), perfect_unison)

        # Inversion of a compound interval is the inversion of the simple part.
        major_tenth = Interval('M', 10)
        major_third = Interval('M', 3)
        self.assertEqual(major_tenth.inversion(), major_third.inversion())

        augmented_fourth = Interval('A', 4)
        diminished_fifth = Interval('d', 5)
        self.assertEqual(diminished_fifth.inversion(), augmented_fourth)

    def test_enharmonic(self):
        augmented_fourth = Interval('A', 4)
        diminished_fifth = Interval('d', 5)
        self.assertTrue(augmented_fourth.is_enharmonic_to(diminished_fifth))
        self.assertEqual(diminished_fifth.enharmonic_equivalent(),
                         augmented_fourth)

        major_tenth = Interval('M', 10)
        pass

        major_third = Interval('M', 3)
        self.assertEqual(major_third.enharmonic_equivalent(), None)

    def test_simple_part_and_is_compound(self):
        perfect_octave = Interval('P', 8)
        major_tenth = Interval('M', 10)
        major_third = Interval('M', 3)

        self.assertEqual(major_tenth.simple_part(), major_third)
        self.assertTrue(major_tenth.is_compound())
        self.assertFalse(major_third.is_compound())
        self.assertFalse(perfect_octave.is_compound())

        # Augmented octaves are compound.
        augmented_octave = Interval('A', 8)
        self.assertTrue(augmented_octave.is_compound())

    def test_from_string(self):
        pass


class TestChords(unittest.TestCase):

    def test_eq(self):
        major_tonic = Chord(1, 'M', 0)
        other_major_tonic = Chord(1, 'M', 0)
        self.assertEqual(major_tonic, other_major_tonic)

        inverted_major_tonic = Chord(1, 'M', 1)
        self.assertNotEqual(major_tonic, inverted_major_tonic)

        minor_tonic = Chord(1, 'm', 0)
        self.assertNotEqual(major_tonic, minor_tonic)

    def test_str(self):
        minor_tonic = Chord(1, 'm', 0)
        self.assertEqual(str(minor_tonic), 'I')

        six_four = Chord(1, 'M', 2)
        self.assertEqual(str(six_four), 'I 6/4')


if __name__ == '__main__':
    unittest.main()
