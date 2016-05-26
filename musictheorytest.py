import unittest

from musictheory import *

class TestIntervals(unittest.TestCase):
    pass

class TestChords(unittest.TestCase):

    def test_create(self):
        tonic = Chord(1, "M", 0)

    def test_eq(self):
        major_tonic = Chord(1, "M", 0)
        other_major_tonic = Chord(1, "M", 0)
        self.assertEqual(major_tonic, other_major_tonic)

        inverted_major_tonic = Chord(1, "M", 1)
        self.assertNotEqual(major_tonic, inverted_major_tonic)

        minor_tonic = Chord(1, "m", 0)
        self.assertNotEqual(major_tonic, minor_tonic)

    def test_str(self):
        minor_tonic = Chord(1, "m", 0)
        self.assertEqual(str(minor_tonic), "I")

        six_four = Chord(1, "M", 2)
        self.assertEqual(str(six_four), "I 6/4")


if __name__ == "__main__":
    unittest.main()
