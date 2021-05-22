from copy import deepcopy
import random
import logging

class Chord:
    chordName = None
    type = None
    keys_numbers = None

    def __init__(self, chordName, type, keys_numbers):
        self.chordName = chordName
        self.type = type
        self.keys_numbers = keys_numbers

    def print(self):
        return(self.chordName + ", " + str(self.type) + ", " + str(self.keys_numbers))


class Chords:

    chords = None
    dictChors = None
    noteKeys = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]

    def __init__(self):
        self.chords = list()


        # Mayor
        self.__addType([3, 2], "Major Chords")
        self.__addType([2, 3], "Minor Chords")
        self.__addType([2, 2], "Diminished Chords")
        self.__addType([3, 3], "Augmented Chord")
        self.__addType([3, 2, 3], "Major Seventh Chord")
        self.__addType([2, 3, 2], "Minor Seventh Chord")
        self.__addType([3, 3, 1], "Augmented 7th")
        self.__addType([3, 2, 2], "Dominant Seventh")
        self.__addType([1, 4], "Sus2")
        self.__addType([4, 1], "Sus4")
        self.__addType([3, 2, 1], "Mayor Sixth")
        self.__addType([2, 3, 1], "Minor Sixth")
        self.__addType([3, 2, 2, 3], "Dominant Ninth")
        self.__addType([3, 2, 3, 2, 2], "Major Eleventh")


        self.dictChors = {
            "Major Chords": [x for x in self.chords if x.type == "Major Chords" ],
            "Minor Chords": [x for x in self.chords if x.type == "Minor Chords"],
            "Diminished Chords": [x for x in self.chords if x.type == "Diminished Chords"],
            "Major Seventh Chord": [x for x in self.chords if x.type == "Major Seventh Chord"],
            "Minor Seventh Chord": [x for x in self.chords if x.type == "Minor Seventh Chord"],
            "Dominant Seventh": [x for x in self.chords if x.type == "Dominant Seventh"],
            "Sus2": [x for x in self.chords if x.type == "Sus2"],
            "Sus4": [x for x in self.chords if x.type == "Sus4"],
            "Mayor Sixth": [x for x in self.chords if x.type == "Mayor Sixth"],
            "Minor Sixth": [x for x in self.chords if x.type == "Minor Sixth"],
            "Dominant Ninth": [x for x in self.chords if x.type == "Dominant Ninth"],
            "Major Eleventh": [x for x in self.chords if x.type == "Major Eleventh"]
        }


    def __addType(self, noteFormula, name):
        for i in range(1, 12):
            keys = []
            keys.append(i)
            last = i
            for n in noteFormula:
                last = last + n + 1
                keys.append(last)
            self.chords.append(Chord(self.noteKeys[i - 1], name, keys))

class Note:
    chord = None
    initial = None
    duration = None
    octave = None

    def __init__(self, chord, initial, duration, octave):
        self.chord = chord
        self.initial = initial
        self.duration = duration
        self.octave = octave
