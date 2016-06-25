import unittest

from musictheory import PitchClass, Pitch, Interval, Chord

class TestPitchClasses(unittest.TestCase):

    def test_validate(self):
        with self.assertRaises(ValueError):
            PitchClass('H')
        with self.assertRaises(ValueError):
            PitchClass('Bb')
        with self.assertRaises(ValueError):
            PitchClass('C', sharps=3)
        with self.assertRaises(ValueError):
            PitchClass('A', flats=-1)
        with self.assertRaises(ValueError):
            PitchClass('C', sharps=1, flats=1)

    def test_eq(self):
        self.assertEqual(PitchClass('C', sharps=1), PitchClass('C', sharps=1))
        self.assertNotEqual(PitchClass('C', sharps=1), PitchClass('C', flats=1))
        self.assertNotEqual(PitchClass('B', sharps=1), PitchClass('C', flats=1))

    def test_hash(self):
        self.assertEqual(hash(PitchClass('C', sharps=1)),
                         hash(PitchClass('C', sharps=1)))
        self.assertNotEqual(hash(PitchClass('C', sharps=1)),
                            hash(PitchClass('C', flats=1)))
        self.assertNotEqual(hash(PitchClass('B', sharps=1)),
                            hash(PitchClass('C', sharps=1)))

    def test_cmp(self):
        self.assertLess(PitchClass('C'), PitchClass('D'))
        self.assertLess(PitchClass('E'), PitchClass('F', flats=1))
        self.assertFalse(PitchClass('C') < PitchClass('C'))
        self.assertLessEqual(PitchClass('C'), PitchClass('C'))
        self.assertGreater(PitchClass('G'), PitchClass('C'))

    def test_interval_between(self):
        self.assertEqual(PitchClass('C').interval_between(PitchClass('G')), \
                Interval('P', 5))
        self.assertEqual(PitchClass('B').interval_between(PitchClass('D')), \
                Interval('M', 6))
        self.assertEqual(PitchClass('C').interval_between(
            PitchClass('C', sharps=1)), Interval('A', 1))

    def test_add(self):
        self.assertEqual(PitchClass('C') + Interval('P', 5), PitchClass('G'))
        self.assertEqual(PitchClass('D') + Interval('P', 12), PitchClass('A'))
        self.assertEqual(PitchClass('G') + Interval('d', 6), PitchClass('E', flats=2))

    def test_str(self):
        self.assertEqual(str(PitchClass('C')), 'C')
        self.assertEqual(str(PitchClass('F', sharps=1)), 'F♯')
        self.assertEqual(str(PitchClass('G', sharps=2)), 'G♯♯')
        self.assertEqual(str(PitchClass('A', flats=1)), 'A♭')

    def test_repr(self):
        C = PitchClass('C')
        Fs = PitchClass('F', sharps=1)
        Gbb = PitchClass('C', flats=2)
        self.assertEqual(C, eval(repr(C)))
        self.assertEqual(Fs, eval(repr(Fs)))
        self.assertEqual(Gbb, eval(repr(Gbb)))

    def test_enharmonic(self):
        self.assertTrue(
            PitchClass('B', sharps=1).is_enharmonic_to(PitchClass('C')))
        self.assertFalse(
            PitchClass('B').is_enharmonic_to(PitchClass('C')))
        pass

class TestPitches(unittest.TestCase):

    def test_validate(self):
        with self.assertRaises(TypeError):
            Pitch(None, 3)

        with self.assertRaises(TypeError):
            Pitch(PitchClass('C'), None)

    def test_eq(self):
        C = PitchClass('C')
        Bs = PitchClass('B', sharps=1)

        self.assertEqual(Pitch(C, 3), Pitch(C, 3))
        self.assertNotEqual(Pitch(C, 3), Pitch(C, 4))
        self.assertNotEqual(Pitch(Bs, -1), Pitch(C, 0))

    def test_hash(self):
        C = PitchClass('C')
        Bs = PitchClass('B', sharps=1)

        self.assertEqual(hash(Pitch(C, 3)), hash(Pitch(C, 3)))
        self.assertNotEqual(hash(Pitch(C, 3)), hash(Pitch(C, 4)))
        self.assertNotEqual(hash(Pitch(Bs, -1)), hash(Pitch(C, 0)))

    def test_str(self):
        pass

    def test_repr(self):
        C3 = Pitch(PitchClass('C'), 3)
        Fs2 = Pitch(PitchClass('F', sharps=1), 2)
        Gbb5 = Pitch(PitchClass('C', flats=2), 5)
        self.assertEqual(C3, eval(repr(C3)))
        self.assertEqual(Fs2, eval(repr(Fs2)))
        self.assertEqual(Gbb5, eval(repr(Gbb5)))

    def test_add(self):
        C, G, D, A = (PitchClass(l) for l in 'CGDA')
        Ebb = PitchClass('E', flats=2)

        self.assertEqual(Pitch(C, 3) + Interval('P', 5), Pitch(G, 3))
        self.assertEqual(Pitch(D, 5) + Interval('P', 12), Pitch(A, 6))
        self.assertEqual(Pitch(G, -2) + Interval('d', 6), Pitch(Ebb, -1))

    def test_cmp(self):
        pass

    def test_enharmonic(self):
        pass

    def test_to_midi(self):
        self.assertEqual(Pitch(PitchClass('C'), 3).to_midi(), 48)
        self.assertEqual(Pitch(PitchClass('B'), -1).to_midi(), 11)

        with self.assertRaises(ValueError):
            Pitch(PitchClass('C'), 11).to_midi()

        with self.assertRaises(ValueError):
            Pitch(PitchClass('C'), -2).to_midi()

    def test_interval_between(self):
        pass


class TestIntervals(unittest.TestCase):

    def test_validate(self):
        with self.assertRaises(ValueError):
            Interval('P', 0)
        with self.assertRaises(ValueError):
            Interval('G', 1)
        with self.assertRaises(ValueError):
            Interval('M', 4)
        with self.assertRaises(ValueError):
            Interval('P', 6)

    def test_eq(self):
        self.assertEqual(Interval('P', 5), Interval('P', 5))
        self.assertNotEqual(Interval('P', 5), Interval('d', 5))
        self.assertNotEqual(Interval('P', 5), Interval('P', 1))
        self.assertNotEqual(Interval('d', 5), Interval('A', 4))

    def test_hash(self):
        self.assertEqual(hash(Interval('P', 5)), hash(Interval('P', 5)))
        self.assertNotEqual(hash(Interval('P', 5)), hash(Interval('d', 5)))
        self.assertNotEqual(hash(Interval('P', 5)), hash(Interval('P', 1)))
        self.assertNotEqual(hash(Interval('d', 5)), hash(Interval('A', 4)))

    def test_str(self):
        self.assertEqual(str(Interval('P', 1)), "P1")
        self.assertEqual(str(Interval('m', 3)), "m3")
        self.assertEqual(str(Interval('M', 10)), "M10")
        self.assertEqual(str(Interval('A', 7)), "A7")

    def test_semitones(self):
        self.assertEqual(Interval('P', 5).semitones(), 7)
        self.assertEqual(Interval('d', 5).semitones(), 6)
        self.assertEqual(Interval('M', 3).semitones(), 4)
        self.assertEqual(Interval('A', 7).semitones(), 12)
        self.assertEqual(Interval('M', 10).semitones(), 16)

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
        self.assertEqual(Interval('P', 8).inversion(), Interval('P', 1))

        # Inversion of a compound interval is the inversion of the simple part.
        self.assertEqual(Interval('M', 10).inversion(),
                         Interval('M', 3).inversion())

        self.assertEqual(Interval('d', 5).inversion(), Interval('A', 4))

    def test_enharmonic(self):
        self.assertTrue(Interval('A', 4).is_enharmonic_to(Interval('d', 5)))
        self.assertEqual(Interval('d', 5).enharmonic_equivalent(),
                         Interval('A', 4))

        self.assertEqual(Interval('A', 10).enharmonic_equivalent(),
                         Interval('d', 11))

        self.assertEqual(Interval('M', 3).enharmonic_equivalent(), None)

    def test_simple_part_and_is_compound(self):
        self.assertEqual(Interval('M', 10).simple_part(), Interval('M', 3))
        self.assertTrue(Interval('M', 10).is_compound())
        self.assertFalse(Interval('M', 3).is_compound())
        self.assertFalse(Interval('P', 8).is_compound())

        # Augmented octaves are compound.
        self.assertTrue(Interval('A', 8).is_compound())
        self.assertEqual(Interval('A', 8).simple_part(), Interval('A', 1))

        self.assertEqual(Interval('d', 8).simple_part(), Interval('d', 8))

    def test_octaves(self):
        self.assertEqual(Interval('d', 8).octaves(), 0)
        self.assertEqual(Interval('A', 8).octaves(), 1)
        self.assertEqual(Interval('A', 15).octaves(), 2)
        self.assertEqual(Interval('M', 14).octaves(), 1)


class TestChords(unittest.TestCase):

    def test_eq(self):
        self.assertEqual(Chord(1, 'M', 0), Chord(1, 'M', 0))
        self.assertNotEqual(Chord(1, 'M', 0), Chord(1, 'M', 1))
        self.assertNotEqual(Chord(1, 'M', 0), Chord(1, 'm', 0))

    def test_hash(self):
        self.assertEqual(hash(Chord(1, 'M', 0)), hash(Chord(1, 'M', 0)))
        self.assertNotEqual(hash(Chord(1, 'M', 0)), hash(Chord(1, 'M', 1)))
        self.assertNotEqual(hash(Chord(1, 'M', 0)), hash(Chord(1, 'm', 0)))

    def test_str(self):
        minor_tonic = Chord(1, 'm', 0)
        self.assertEqual(str(minor_tonic), 'i')

        six_four = Chord(4, 'M', 2)
        self.assertEqual(str(six_four), 'IV⁶⁄₄')


if __name__ == '__main__':
    unittest.main()
