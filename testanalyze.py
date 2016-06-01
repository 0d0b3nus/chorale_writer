import os
import unittest

from mido import MidiFile

from analyze import chunks

class TestChunker (unittest.TestCase):

    def test_chunking(self):
        with MidiFile('test_chunking.mid') as midi_file:
            expected_chunks = [[4, 7, 0], [2, 11, 9, 4], [4, 11, 7, 6, 9],
                               [6, 0, 11, 9, 7], [4, 11, 7, 9, 0],
                               [4, 9, 11, 7], [2, 9, 11], [0, 2, 9]]
            for produced, expected in zip(chunks(midi_file), expected_chunks):
                self.assertEqual(produced, expected)

if __name__ == '__main__':
    unittest.main()
