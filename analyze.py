import os

from mido import MidiFile
from musictheory import PitchClass, Key

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
        key_string = get_key_string(midi_file)
        print(key_string)
        if key_string.endswith('m'):
            key = Key(PitchClass(key_string[:-1]), 'm')
        else:
            key = Key(PitchClass(key_string), 'M')

        print(key)
        chunks = self.__chunks(midi_file)

        for chunk in chunks:
            for chord in key.common_chords():
                if set(chunk).issubset(set(chord.equivalence_classes(key))):
                    print(chunk, ' is ', chord)
                    break
            else:
                print("The fuck is ", chunk)

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

FILES = os.listdir('corpus/')

for file_ in FILES:
    if file_.endswith('.mid'):
        with MidiFile('corpus/' + file_) as midi_file:
            if len(midi_file.tracks) == 5:
                cp = ChordProgression()
                print(file_)
                print(cp.from_midi_file(midi_file))
                break
