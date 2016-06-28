from musictheory import *

CMajor = Key(PitchClass('C'))
print(CMajor.degrees)
Cminor = Key(PitchClass('C'), scale="m")
print(Cminor.degrees)
I= Chord(1, 'M', 0)
print(I.pitch_classes(CMajor))

for chord in CMajor.common_chords():
    print(chord)

for chord in Cminor.common_chords():
    print(chord)

five_of_five = Chord(5, 'M7', 2, (5, 'M'))
print(five_of_five)
print(five_of_five.pitch_classes(Key(PitchClass('C'))))
print(five_of_five.equivalence_classes(Key(PitchClass('C'))))
