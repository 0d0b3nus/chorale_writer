import os

from mido import MidiFile

'''
files = os.listdir('corpus/')

for file_ in files:
    if file_.endswith('.mid'):
        with MidiFile('corpus/' + file_) as midi_file:
            print(file_, len(midi_file.tracks))
'''

with MidiFile('corpus/064900b_.mid') as midi_file:
    for i, track in enumerate(midi_file.tracks):
        print(i)
        print(' ')
        for message in track:
            print('   {}'.format(message))
