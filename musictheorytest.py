import unittest

from musictheory import *

class TestIntervals(unittest.TestCase):

    def test_eq(self):
        perfect_unison = Interval('P', 1)
        augmented_fourth = Interval('A', 4)
        diminished_fifth = Interval('d', 5)
        perfect_fifth = Interval('P', 5)
        other_perfect_fifth = Interval('P', 5)

        self.assertEqual(perfect_fifth, other_perfect_fifth)
        self.assertNotEqual(perfect_fifth, diminished_fifth)
        self.assertNotEqual(perfect_fifth, perfect_unison)
        self.assertNotEqual(diminished_fifth, augmented_fourth)

    def test_str(self):
        perfect_unison = Interval('P', 1)
        self.assertEqual(str(perfect_unison), "P1")

        minor_third = Interval('m', 3)
        self.assertEqual(str(minor_third), "m3")

        major_tenth = Interval('M', 10)
        self.assertEqual(str(major_tenth), "M10")

        augmented_seventh = Interval('A', 7)
        self.assertEqual(str(augmented_seventh), "A7")

    def test_semitones(self):
        perfect_fifth = Interval('P', 5)
        self.assertEqual(perfect_fifth.semitones, 7)

        diminished_fifth = Interval('d', 5)
        self.assertEqual(diminished_fifth.semitones, 6)

        major_third = Interval('M', 3)
        self.assertEqual(major_third.semitones, 4)

        augmented_seventh = Interval('A', 7)
        self.assertEqual(augmented_seventh.semitones, 12)

        diminished_sixth = Interval('d', 6)
        self.assertEqual(diminished_sixth.semitones, 7)

        major_tenth = Interval('M', 10)
        self.assertEqual(major_tenth.semitones, 16)

    def test_add(self):
        diminished_fifth = Interval('d', 5)
        augmented_fourth = Interval('A', 4)
        perfect_octave = Interval('P', 8)
        self.assertEqual(diminished_fifth + augmented_fourth, perfect_octave)

        major_tenth = Interval('M', 10)
        chord = Interval('M', 3)
        chord += perfect_octave
        self.assertEqual(chord, major_tenth)

        major_third = Interval('M', 3)
        augmented_fifth = Interval('A', 5)
        self.assertEqual(major_third + major_third, augmented_fifth)

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
