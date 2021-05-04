from pypianoroll import Multitrack, Track
import numpy as np
import glob
from Persistence import Utilities as U
from Persistence.wavfile import read, write

def loadMidiFile(path2file, limitBars=4):
    try:
        midi = Multitrack(path2file)
        steps = 96 * limitBars

        if len(midi.tracks) > 1: print("WARNING: More than 1 track in " + path2file + ", Selecting the first.")

        pianoRoll = np.array(midi.tracks[0].pianoroll)
        if pianoRoll.shape[0] < steps:
            print("WARNING: Track " + path2file + " don't have enough dimesion. Got " + str(
                pianoRoll.shape) + ", expected (" + str(steps) + ", 128)")
            return (None)

        pianoRoll = pianoRoll[0:steps, :]

        return (pianoRoll)

    except:
        return (None)


def loadWavFile(path2file, timeLimit=20000):
    try:
        wav = read(path2file)
        wav = wav.data
        wav = wav[0:timeLimit, :] if wav.shape[0] >= timeLimit else np.concatenate((wav, np.zeros(shape=(timeLimit - wav.shape[0], 2))), axis=0)
        return (wav)
    except:
        return None

def saveMidiFile(npArray, path2save):
    obj = Track(npArray)
    mobj = Multitrack(filename=None, tracks=[obj])
    mobj.write(path2save)

def saveWavFile(npArray, path2save, samplerate=44100):
    write(path2save, npArray, samplerate, sampwidth=3)


def loadMidiBatch(path2midis, limitBars=4, augmentationData=True):
    midis = []
    midisNames = []
    for f in (glob.glob(path2midis + "/*")):
        midi = loadMidiFile(f, limitBars)
        if midi is not None:
            if augmentationData:
                midiAugmented = U.pianoAugmentation(midi)
                for i in range(len(midiAugmented)):
                    midis.append(midiAugmented[i])
                    midisNames.append(f + "_augmented_" + str(i))
            else:
                midis.append(midi)
                midisNames.append(f)
    return (np.array(midis), midisNames)


def loadWavBatch(path2wavs, timeLimit=20000):
    wavs = []
    vawsNames = []
    for f in (glob.glob(path2wavs + "/*")):
        wav = loadWavFile(f, timeLimit)
        if wav is not None:
            wavs.append(wav)
            vawsNames.append(f)
    return (np.array(wavs), vawsNames)
