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
        r = random.uniform(aleatoryDuration, seconds-aleatoryDuration)
        logging.info("Automatic cut in range " + str(round(r-aleatoryDuration, 2)) + "-" + str(round(r,2)))
        sequence = note_seq.extract_subsequence(
            sequence=sequence,
            start_time= 0 if (r-aleatoryDuration) <= 0 else r-aleatoryDuration,
            end_time=r)
    else:
        sys.exit(1)

    return sequence

def secondsDuration(sequence):
    return (max(n.end_time for n in sequence.notes) if sequence.notes else 0)
