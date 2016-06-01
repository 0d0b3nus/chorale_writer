import os

from mido import MidiFile

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


def chunks(midi_file):

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

files = os.listdir('corpus/')

for file_ in files:
    if file_.endswith('.mid'):
        with MidiFile('corpus/' + file_) as midi_file:
            if len(midi_file.tracks) == 5:
                chunks(midi_file)
