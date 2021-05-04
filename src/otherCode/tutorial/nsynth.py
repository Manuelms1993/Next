import os
import numpy as np
import matplotlib.pyplot as plt
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen
from IPython.display import Audio



if __name__ == "__main__":
    os.chdir("/Users/manuelmontero/PycharmProjects/NEXT")

    fname = "resource/one-shots/clap/126BPM_Clap001.wav"
    sr = 16000
    audio = utils.load_audio(fname, sample_length=40000, sr=sr)
    sample_length = audio.shape[0]
    print('{} samples, {} seconds'.format(sample_length, sample_length / float(sr)))

    encoding = fastgen.encode(audio, '/Users/manuelmontero/PycharmProjects/NEXT/content/model.ckpt-200000', sample_length)
    fastgen.synthesize(encoding, save_paths=['resource/generated/wavs/' + "gen1.wav"], samples_per_save=sample_length)