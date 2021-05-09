from copy import deepcopy
import random
import logging

KEYS_NUMBERS = {
    "Cb": 12,
    "C": 1,
    "C#": 2,
    "Db": 2,
    "D": 3,
    "D#": 4,
    "Ebb" : 3,
    "Eb": 4,
    "E": 5,
    "E#": 6,
    "Fb" : 5,
    "F": 6,
    "F#": 7,
    "Gb": 7,
    "G": 8,
    "G#": 9,
    "Ab": 9,
    "A": 10,
    "A#": 11,
    "Bbb" : 10,
    "Bb": 11,
    "B": 12,
    "B#" : 1
}


class Chord:
    chordName = None
    family = None
    keys = None
    keys_numbers = None

    def __init__(self, chordName, family, keys):
        self.chordName = chordName
        self.family = family
        self.keys = keys

        self.keys_numbers = deepcopy(keys)
        for i in range(len(keys)):
            self.keys_numbers[i] = KEYS_NUMBERS[keys[i]]

    @property
    def __str__(self):
        return ("(" + str(self.family) + ", " + str(self.chordName) + ") --> " + str(self.keys) + " | " + str(
            self.keys_numbers))


class Chords:

    chords = None
    dictChors = None

    def __init__(self):
        self.chords = list()

        self.chords.append(Chord("C major", "Major Chords", ["C", "E", "G"]))
        self.chords.append(Chord("C# major", "Major Chords", ["C#", "E#", "G#"]))
        self.chords.append(Chord("D major", "Major Chords", ["D", "F#", "A"]))
        self.chords.append(Chord("Eb major", "Major Chords", ["Eb", "G", "Bb"]))
        self.chords.append(Chord("E major", "Major Chords", ["E", "G#", "B"]))
        self.chords.append(Chord("F major", "Major Chords", ["F", "A", "C"]))
        self.chords.append(Chord("F# major", "Major Chords", ["F#", "A#", "C#"]))
        self.chords.append(Chord("G major", "Major Chords", ["G", "B", "D"]))
        self.chords.append(Chord("Ab major", "Major Chords", ["Ab", "C", "Eb"]))
        self.chords.append(Chord("A major", "Major Chords", ["A", "C#", "E"]))
        self.chords.append(Chord("Bb major", "Major Chords", ["Bb", "D", "F"]))
        self.chords.append(Chord("B major", "Major Chords", ["B", "D#", "F#"]))

        self.chords.append(Chord("C minor", "Minor Chords", ["C", "Eb", "G"]))
        self.chords.append(Chord("C# minor", "Minor Chords", ["C#", "E", "G#"]))
        self.chords.append(Chord("D minor", "Minor Chords", ["D", "F", "A"]))
        self.chords.append(Chord("Eb minor", "Minor Chords", ["Eb", "Gb", "Bb"]))
        self.chords.append(Chord("E minor", "Minor Chords", ["E", "G", "B"]))
        self.chords.append(Chord("F minor", "Minor Chords", ["F", "Ab", "C"]))
        self.chords.append(Chord("F# minor", "Minor Chords", ["F#", "A", "C#"]))
        self.chords.append(Chord("G minor", "Minor Chords", ["G", "Bb", "D"]))
        self.chords.append(Chord("Ab minor", "Minor Chords", ["Ab", "Cb", "Eb"]))
        self.chords.append(Chord("A minor", "Minor Chords", ["A", "C", "E"]))
        self.chords.append(Chord("Bb minor", "Minor Chords", ["Bb", "Db", "F"]))
        self.chords.append(Chord("B minor", "Minor Chords", ["B", "D", "F#"]))

        self.chords.append(Chord("C diminished", "Diminished Chords", ["C", "Eb", "Gb"]))
        self.chords.append(Chord("C# diminished", "Diminished Chords", ["C#", "E", "G"]))
        self.chords.append(Chord("D diminished", "Diminished Chords", ["D", "F", "Ab"]))
        self.chords.append(Chord("Eb diminished", "Diminished Chords", ["Eb", "Gb", "Bbb"]))
        self.chords.append(Chord("E diminished", "Diminished Chords", ["E", "G", "Bb"]))
        self.chords.append(Chord("F diminished", "Diminished Chords", ["F", "Ab", "Cb"]))
        self.chords.append(Chord("F# diminished", "Diminished Chords", ["F#", "A", "C"]))
        self.chords.append(Chord("G diminished", "Diminished Chords", ["G", "Bb", "Db"]))
        self.chords.append(Chord("Ab diminished", "Diminished Chords", ["Ab", "Cb", "Ebb"]))
        self.chords.append(Chord("A diminished", "Diminished Chords", ["A", "C", "Eb"]))
        self.chords.append(Chord("Bb diminished", "Diminished Chords", ["Bb", "Db", "Fb"]))
        self.chords.append(Chord("B diminished", "Diminished Chords", ["B", "D", "F"]))

        self.chords.append(Chord("C major seventh", "Major 7th Chords", ["C", "E", "G", "B"]))
        self.chords.append(Chord("C# major seventh", "Major 7th Chords", ["C#", "E#", "G#", "B#"]))
        self.chords.append(Chord("D major seventh", "Major 7th Chords", ["D", "F#", "A", "C#"]))
        self.chords.append(Chord("Eb major seventh", "Major 7th Chords", ["Eb", "G", "Bb", "D"]))
        self.chords.append(Chord("E major seventh", "Major 7th Chords", ["E", "G#", "B", "D#"]))
        self.chords.append(Chord("F major seventh", "Major 7th Chords", ["F", "A", "C", "E"]))
        self.chords.append(Chord("F# major seventh", "Major 7th Chords", ["F#", "A#", "C#", "E#"]))
        self.chords.append(Chord("G major seventh", "Major 7th Chords", ["G", "B", "D", "F#"]))
        self.chords.append(Chord("Ab major seventh", "Major 7th Chords", ["Ab", "C", "Eb", "G"]))
        self.chords.append(Chord("A major seventh", "Major 7th Chords", ["A", "C#", "E", "G#"]))
        self.chords.append(Chord("Bb major seventh", "Major 7th Chords", ["Bb", "D", "F", "A"]))
        self.chords.append(Chord("B major seventh", "Major 7th Chords", ["B", "D#", "F#", "A#"]))

        self.dictChors = {
            "Major Chords": [x for x in self.chords if x.family == "Major Chords" ],
            "Minor Chords": [x for x in self.chords if x.family == "Minor Chords"],
            "Major 7th Chords": [x for x in self.chords if x.family == "Major 7th Chords"],
            "Diminished Chords": [x for x in self.chords if x.family == "Diminished Chords"]
        }


    def getChord(self, family=None):
        cho = random.sample(self.chords, len(self.chords))
        if family == None:
            return (cho[0])
        else:
            for c in cho:
                if c.family == family: return c


    def getFinalChord(self, scale, key_number):
        listChords = self.dictChors[scale]

        for c in listChords:
            logging.info(c.chordName + ": " + str(c.keys_numbers))
            if key_number == c.keys_numbers[0]:
                return c

        return None


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
