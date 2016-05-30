from musictheory import *

C = PitchClass('C')
G = PitchClass('G')
Gb = PitchClass('G', flats=1)
print(C, G, C.interval_between(G))
print(C, C, C.interval_between(C))
print(C, Gb, C.interval_between(Gb))
print(Gb, C, Gb.interval_between(C))
