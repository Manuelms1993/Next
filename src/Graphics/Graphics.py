from pypianoroll import Multitrack, Track
from matplotlib import pyplot as plt

def plotMidi(path2file):

    midi = Multitrack(path2file)
    fig, ax = midi.plot()
    plt.show()

def plotPiano(npArray):

    obj = Track(npArray)
    mobj = Multitrack(filename = None, tracks=[obj])
    fig, ax = mobj.plot()
    plt.show()