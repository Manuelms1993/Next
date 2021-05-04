from note_seq.protobuf import music_pb2
from google.colab import files
import magenta
import note_seq
import tensorflow
import os
import random
import sys
from datetime import datetime
# Import dependencies.
from magenta.models.music_vae import configs
from magenta.models.music_vae.trained_model import TrainedModel

if __name__ == "__main__":
      os.chdir("/Users/manuelmontero/PycharmProjects/NEXT")
      today = datetime.now()

      # Initialize the model.
      print("Initializing Music VAE...")
      music_vae = TrainedModel(
            configs.CONFIG_MAP['nade-drums_2bar_full'],
            batch_size=8,
            checkpoint_dir_or_path='content/drums_2bar_nade.full.ckpt')

      generated_sequences = music_vae.sample(n=1, length=128, temperature=0.9)

      n = 0
      for ns in generated_sequences:
            note_seq.sequence_proto_to_midi_file(ns, "resource/generated/output/drums_" + str(today) + str(n) + ".mid")
            n += 1