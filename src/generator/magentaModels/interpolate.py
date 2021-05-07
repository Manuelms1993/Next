from persistence.loaders import load
import note_seq
from utils.NoteSequenceUtils import secondsDuration
import logging

def interpolate(model, path1, path2, bpm, length, num_steps, temperature):

    logging.info("Interpolate: ")
    logging.info("  Path1: " + str(path1))
    logging.info("  Path2: " + str(path2))

    seq1 = load(path1, bpm)
    seq2 = load(path2, bpm)

    if secondsDuration(seq1)>12 or secondsDuration(seq2)>12: return None

    #seq1 = note_seq.extract_subsequence(sequence=seq1, start_time=0, end_time=(60.0 / seq1.tempos[0].qpm) * 8, preserve_control_numbers=None)
    #seq2 = note_seq.extract_subsequence(sequence=seq2, start_time=0, end_time=(60.0 / seq2.tempos[0].qpm) * 8, preserve_control_numbers=None)

    logging.info("Interpolating: ")
    logging.info("  Path1: " + str(path1))
    logging.info("      Info1: " + str(secondsDuration(seq1)) + "s - " + str(len(seq1.notes)) + " notes")
    logging.info("  Path2: " + str(path2))
    logging.info("      Info2: " + str(secondsDuration(seq2)) + "s - " + str(len(seq2.notes)) + " notes")

    note_sequences = model.interpolate(seq1, seq2, length=length, num_steps=num_steps, temperature=temperature)
    return note_seq.sequences_lib.concatenate_sequences(note_sequences)
