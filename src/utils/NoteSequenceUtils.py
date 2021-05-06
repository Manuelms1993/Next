import sys
import note_seq
import random
import logging

def cutSequence(sequence, start: int, end: int, aleatoryCut = True, aleatoryDuration = 1):
    if (start != None and end != None and start != "None" and end != "None"):
        logging.info("Cutting sequence. Start = " + str(start) + ", End = " + str(end))
        sequence = note_seq.extract_subsequence(
                sequence=sequence,
                start_time=start,
                end_time=end)
    elif (aleatoryCut):
        logging.info("Aleatory cut.")
        seconds = round(secondsDuration(sequence))
        r = random.randint(1, seconds-aleatoryDuration)
        logging.info("Automatic cut in range " + str(r-aleatoryDuration) + "-" + str(r))
        sequence = note_seq.extract_subsequence(
            sequence=sequence,
            start_time=r-aleatoryDuration,
            end_time=r)
    else:
        sys.exit(1)

    return sequence

def secondsDuration(sequence):
    return (max(n.end_time for n in sequence.notes) if sequence.notes else 0)
