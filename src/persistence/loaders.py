import random
import note_seq
import os
from glob import glob
from utils.constant import Constants
import logging
from note_seq.protobuf import music_pb2


def load(path, bpm):
    seq = note_seq.midi_file_to_note_sequence(path)
    noteSeq = music_pb2.NoteSequence()
    noteSeq.tempos.add(qpm=bpm)
    for note in [n for n in seq.notes]:
        noteSeq.notes.add(pitch=note.pitch, start_time=note.start_time, end_time=note.end_time, velocity=note.velocity)
    return noteSeq

def loadSequence(path: str, midiAleatoryPath: str, bpm: int, loadAleatory: bool = True):

    if (path == None or path == "auto" and loadAleatory):
        logging.info("Searching midi file: " + str(midiAleatoryPath))
        result = [y for x in os.walk(midiAleatoryPath) for y in glob(os.path.join(x[0], '*.mid'))]
        path = random.choice(result)

    logging.info("Loading midi file: " + path)
    sequence = note_seq.midi_file_to_note_sequence(path)
    sequence.ticks_per_quarter = 0
    if (bpm != None): sequence.tempos[0].qpm = bpm

    return sequence
