import os

import numpy as np
from mido import MidiFile

from musictheory import PitchClass, Key, Chord

def get_key_string(midi_file):
    meta_track = midi_file.tracks[0]
    for message in meta_track:
        if message.type == 'key_signature':
            return message.key


def get_tempo(midi_file):
    meta_track = midi_file.tracks[0]
    for message in meta_track:
        if message.type == 'set_tempo':
            return message.tempo

class ChordProgression(object):

    def __init__(self):
        progression = []

    def from_midi_file(self, midi_file):
        chords = []
        key_string = get_key_string(midi_file)
        key = Key.from_str(key_string)

        chunks = self.__chunks(midi_file)

        for chunk in chunks:
            best_match_rate = 0
            chunk_set = set(chunk)
            for chord in key.common_chords():
                chord_set = set(chord.equivalence_classes(key))
                if chunk_set.issubset(chord_set):
                    best_match = chord
                    break
                match_rate = len(chunk_set & chord_set) / \
                             len(chunk_set | chord_set)
                if match_rate > best_match_rate:
                    best_match = chord
                    best_match_rate = match_rate
            try:
                inversion = best_match.equivalence_classes(key).index(chunk[0])
            except ValueError:
                inversion = 0 # Bass note is not a chord tone, assume root pos
            chords.append(best_match)

        return chords

    def __chunks(self, midi_file):

        def chunkify_track(bucket, midi_track, ticks_per_beat):
            index = 0
            bucket_capacity = {}
            for message in midi_track:
                if message.type == 'note_off':
                    note = message.note % 12
                    time = message.time
                    while time > 0:
                        bucket_capacity.setdefault(index, ticks_per_beat)
                        if time <= bucket_capacity[index]:
                            bucket_capacity[index] -= time
                            time = 0
                        else:
                            time -= bucket_capacity[index]
                            bucket_capacity[index] = 0
                        insert_once(note, bucket.setdefault(index, list()))
                        if bucket_capacity[index] == 0:
                            index += 1

        def insert_once(item, list_):
            if item not in list_:
                list_.append(item)

        bucket = {}

        bass_track = midi_file.tracks[4]
        tenor_track = midi_file.tracks[3]
        alto_track = midi_file.tracks[2]
        soprano_track = midi_file.tracks[1]

        for midi_track in (bass_track, tenor_track, alto_track, soprano_track):
            chunkify_track(bucket, midi_track, midi_file.ticks_per_beat)

        bucket_list = []
        for i in range(0, len(bucket)):
            bucket_list.append(bucket[i])
        return bucket_list

class MarkovChain(object):

    def __init__(self, training_data, order=1):
        self.tokens = {} #FIXME: Use a bidict?
        self.__train(training_data, order)

    def __train(self, training_data, order):
        num_tokens = 0
        for token in training_data:
            if token not in self.tokens.values():
                self.tokens[num_tokens] = token
                num_tokens += 1
        print(self.tokens)
        frequency_table = np.array([], dtype='d', ndmin=order+1)

        # FIXME: Read about slice objects?
        window_start = 0
        window_end = order + 1
        while window_end < len(training_data)

    def generate_sequence(self, start_token=None, end_token=None):
        pass

FILES = os.listdir('corpus/')

for file_ in FILES:
    if file_.endswith('.mid'):
        print(file_)
        with MidiFile('corpus/' + file_) as midi_file:
            if len(midi_file.tracks) == 5:
                cp = ChordProgression()
                chords = cp.from_midi_file(midi_file)
                print(' | '.join(map(str, chords)))
                m = MarkovChain(chords)
                break
