import os
os.chdir("/Users/manuelmontero/PycharmProjects/NEXT")
from  ChordGenerators.Melody import Melody

m = Melody(bars = 40)
m.aleatoryGeneration(durationInBars = None, family = None, octave = 4, silenceNote = -1)
print(m)
m.saveMelody("./model/prueba.mid")