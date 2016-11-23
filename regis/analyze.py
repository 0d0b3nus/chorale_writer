from collections import defaultdict
import heapq
import os

from mido import MidiFile

from musictheory import Key, Chord

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
        self.progression = []

    def __str__(self):
        return ' | '.join([str(chord) for chord in self.progression])

    def from_midi_file(self, midi_file):
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
            scale_degree = best_match.scale_degree
            quality = best_match.quality
            relative = best_match.relative
            self.progression.append(Chord.get_cached(scale_degree, quality,
                                                     inversion, relative))

    @staticmethod
    def __chunks(midi_file):

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

major_key_progressions = []
minor_key_progressions = []

for file_ in FILES:
    if file_.endswith('.mid'):
        with MidiFile('corpus/' + file_) as midi_file:
            if len(midi_file.tracks) == 5:
                if get_key_string(midi_file).endswith('m'):
                    progressions = minor_key_progressions
                else:
                    progressions = major_key_progressions
                cp = ChordProgression()
                cp.from_midi_file(midi_file)
                progressions.append(cp.progression)


def generate_transition_matrix(progressions):
    histogram = defaultdict(int)
    transition_matrix = defaultdict(int)

    for progression in progressions:
        for i in range(0, len(progression) - 1):
            from_chord, to_chord = progression[i:i+2]
            histogram[from_chord] += 1
            transition_matrix[(from_chord, to_chord)] += 1

    return (histogram, transition_matrix)

def get_n_most_common(dictionary, n):
    values = list(dictionary.values())
    largest = heapq.nlargest(n, values)
    keys = list(dictionary.keys())
    return [keys[values.index(m)] for m in largest]

def get_trimmed_transition(histogram, transition_matrix, n):
    new_matrix = defaultdict(int)

    chords = get_n_most_common(histogram, n)
    for from_chord in chords:
        for to_chord in chords:
            if from_chord == to_chord:
                continue
            new_matrix[(from_chord, to_chord)] = \
                    transition_matrix[(from_chord, to_chord)]
    return new_matrix

def get_max(dictionary):
    if not dictionary:
        return None
    else:
        current_max = dictionary.values[0]

    for value in dictionary.values():
        current_max = value if value > current_max else current_max
    return current_max

def write_graphviz(progressions, filename):
    histogram, transition_matrix = generate_transition_matrix(progressions)
    trimmed = get_trimmed_transition(histogram, transition_matrix, 11)
    chords = get_n_most_common(histogram, 11)
    max_ = get_max(trimmed)
    w = 4.0 / max_

    with open(filename, 'w') as fp:
        fp.write('digraph G {\n')
        for from_ in chords:
            for to in chords:
                if trimmed[(from_, to)] == 0:
                    continue
                weight = w * trimmed[(from_, to)]
                from_str = str(from_).encode('ascii', 'xmlcharrefreplace')
                from_str = from_str.decode('utf-8')
                to_str = str(to).encode('ascii', 'xmlcharrefreplace')
                to_str = to_str.decode('utf-8')
                format_str = '    \"{0}\" -> \"{1}\"[penwidth={2:3}];\n'
                fp.write(format_str.format(from_str, to_str, weight))
        fp.write('}')

write_graphviz(major_key_progressions, 'major.dot')
write_graphviz(minor_key_progressions, 'minor.dot')
