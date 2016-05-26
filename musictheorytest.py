import unittest

from musictheory import *

class TestIntervals(unittest.TestCase):

    def test_eq(self):
        perfect_fifth = Interval('P', 5)
        other_perfect_fifth = Interval('P', 5)
        diminished_fifth = Interval('d', 5)
        perfect_unison = Interval('P', 8)

    def test_str(self):
        pass

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

class TestChords(unittest.TestCase):

    def test_create(self):
        tonic = Chord(1, 'M', 0)

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
