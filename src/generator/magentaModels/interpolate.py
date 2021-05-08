from persistence.loaders import load
import note_seq
from utils.NoteSequenceUtils import secondsDuration
import logging

def interpolate(model, path1, path2, bpm, length, num_steps, temperature):

    bar = 8

    logging.info("Interpolate: ")
    logging.info("  Path1: " + str(path1))
    logging.info("  Path2: " + str(path2))

    seq1 = load(path1, bpm)
    seq2 = load(path2, bpm)

    d1 = secondsDuration(seq1)
    d2 = secondsDuration(seq1)

    logging.info("Interpolating: ")
    logging.info("  Path1: " + str(path1))
    logging.info("      Info1: " + str(d1) + "s - " + str(len(seq1.notes)) + " notes")
    logging.info("      Cut1: " + str((60.0 / seq1.tempos[0].qpm) * bar))
    logging.info("  Path2: " + str(path2))
    logging.info("      Info2: " + str(d2) + "s - " + str(len(seq2.notes)) + " notes")
    logging.info("      Cut2: " + str((60.0 / seq2.tempos[0].qpm) * bar))

    seq_1 = note_seq.extract_subsequence(sequence=seq1, start_time=0, end_time=(60.0 / seq1.tempos[0].qpm) * bar, preserve_control_numbers=None)
    seq_2 = note_seq.extract_subsequence(sequence=seq2, start_time=0, end_time=(60.0 / seq2.tempos[0].qpm) * bar, preserve_control_numbers=None)

    logging.info("Total time 1: " + str(seq_1.total_time))
    logging.info("Total time 2: " + str(seq_2.total_time))

    note_sequences = model.interpolate(seq_1, seq_2, length=length, num_steps=num_steps, temperature=temperature)
    return note_seq.sequences_lib.concatenate_sequences(note_sequences)
