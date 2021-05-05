import random
import note_seq
import os
from glob import glob
from utils.constant import Constants
import logging


def loadSequence(path: str, bpm: int, loadAleatory: bool = True):

    if (path == None or path == "auto" and loadAleatory):
        result = [y for x in os.walk(Constants.GENERAL_MID_PATH) for y in glob(os.path.join(x[0], '*.mid'))]
        path = random.choice(result)

    logging.info("Loading midi file: " + path)
    sequence = note_seq.midi_file_to_note_sequence(path)
    sequence.ticks_per_quarter = 0
    if (bpm != None): sequence.tempos[0].qpm = bpm

    return sequence
