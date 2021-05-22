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

def getEndSecondsPerBpm(bpm, bars=2):
    # (120 seconds / bpm / 2) = 1 beat
    # 1 * 4 = 1Bar
    return (120 / bpm / 2) * 4 * bars + (120 / bpm / 8)

def getInstrumentPath(path):
    outputProgram = random.choice([1,2,3,4,5,6,7,8])
    if "/bass" in path:
        outputProgram = random.choice([33,34,35,36,37,38,39,40])
    if "/pad" in path:
        outputProgram = random.choice([89,90,91,92,93,94,95,96])
    if "/drums" in path:
        return None
    return outputProgram