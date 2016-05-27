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

        major_eleventh = Interval('M', 11)
        self.assertEqual(str(major_eleventh), "M11")

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

        major_eleventh = Interval('M', 11)
        self.assertEqual(major_eleventh.semitones, 16)

    def test_add(self):
        pass

    def test_cmp(self):
        perfect_fifth = Interval('P', 5)
        diminished_fifth = Interval('d', 5)
        self.assertFalse(perfect_fifth <= diminished_fifth)
        self.assertFalse(perfect_fifth < diminished_fifth)
        self.assertTrue(perfect_fifth >= diminished_fifth)
        self.assertTrue(perfect_fifth >= diminished_fifth)
        self.assertTrue(perfect_fifth >= perfect_fifth)


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
