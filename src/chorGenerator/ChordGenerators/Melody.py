from ChordGenerators.Chords import Chords, Chord, KEYS_NUMBERS, Note
import random
from Persistence.Persistence import saveMidiFile
import numpy as np

BAR_SIZE = 96
NOTE_TIMES = [1/16 * BAR_SIZE, 1/15 * BAR_SIZE, 1/12 * BAR_SIZE, 1/9 * BAR_SIZE, 1/8 * BAR_SIZE, 1/6 * BAR_SIZE, 1/4 * BAR_SIZE, 1/3 * BAR_SIZE, 1/2 * BAR_SIZE, 1 * BAR_SIZE]

class Melody:

    __chords = None
    __totalLength = None
    __bars = None
    melody = None

    def __init__(self, bars = 4):
        self.__chords = Chords()
        self.__totalLength = bars * BAR_SIZE
        self.__bars = bars

    def __str__(self):
        if self.melody != None:
            f = ""
            for n in self.melody:
                f += n.chord.__str__ + ", Initial: " + str(n.initial) + ", Duration: " + str(n.duration) + ", Octave: " + str(n.octave) + "\n"
            return f
        return "Empty melody!"

    def __createMelodyMatrix(self):
        matrix = np.zeros(shape=(self.__totalLength, 128))
        for note in self.melody:
            for keys in note.chord.keys_numbers:
                matrix[int(note.initial):int(note.duration), keys-1+(12*note.octave)] = 100
        return(matrix)

    def saveMelody(self, path):
        if self.melody == None:
            print("Melody empty!")
            return ()
        matrix = self.__createMelodyMatrix()
        saveMidiFile(matrix, path2save=path)


    def aleatoryGeneration(self, durationInBars = None, family = None, octave = 3, silenceNote = -1):
        melody = list()
        initial = 0

        while True:

            chord = self.__chords.getChord(family)
            silence = silenceNote*BAR_SIZE if silenceNote>-0.1 else random.choice(NOTE_TIMES)
            time = random.choice(NOTE_TIMES) if durationInBars == None else durationInBars*BAR_SIZE

            if initial+time<self.__totalLength:
                melody.append(Note(chord, initial, initial+time, octave))
                initial += time + silence
                if initial>= self.__totalLength: initial = self.__totalLength
            else:
                self.melody = melody
                return()
