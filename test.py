from musictheory import *

CMajor = Key(PitchClass('C'))
print(CMajor.degrees)
Cminor = Key(PitchClass('C'), scale="m")
print(Cminor.degrees)
I= Chord(1, 'M', 0)
print(I.pitch_classes(CMajor))
