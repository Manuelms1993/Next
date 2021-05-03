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

      veldt = note_seq.midi_file_to_note_sequence('resource/mid/Deadmau5/deadmau5_TheVeldt.mid')
      strobe = note_seq.midi_file_to_note_sequence('resource/mid/Deadmau5/Deadmau5_Strobe_1.mid')

      veldt = note_seq.extract_subsequence(sequence=veldt,
                                            start_time=0,
                                            end_time= (60.0 / veldt.tempos[0].qpm) * 4,
                                            preserve_control_numbers=None)

      strobe = note_seq.extract_subsequence(sequence=strobe,
                                            start_time=0,
                                            end_time= (60.0 / strobe.tempos[0].qpm) * 4,
                                            preserve_control_numbers=None)

      note_seq.sequence_proto_to_midi_file(strobe, "resource/generated/output/strobe1.mid")
      note_seq.sequence_proto_to_midi_file(veldt, "resource/generated/output/veldt1.mid")

      veldt.ticks_per_quarter = 0
      strobe.ticks_per_quarter = 0
      strobe.tempos[0].qpm = 128
      veldt.tempos[0].qpm = 128
      print(veldt.ticks_per_quarter)
      print(strobe.ticks_per_quarter)

      # Initialize the model.
      print("Initializing Music VAE...")
      music_vae = TrainedModel(
            configs.CONFIG_MAP['cat-mel_2bar_big'],
            batch_size=8,
            checkpoint_dir_or_path='content/mel_2bar_big.ckpt')

      # This gives us a list of sequences.
      note_sequences = music_vae.interpolate(
            veldt,
            strobe,
            length=16,
            num_steps=16,
            temperature=0.1)

      # Concatenate them into one long sequence, with the start and
      # end sequences at each end.
      print(note_sequences)
      interp_seq = note_seq.sequences_lib.concatenate_sequences(note_sequences)

      note_seq.sequence_proto_to_midi_file(interp_seq, "resource/generated/output/inter" + str(today) + ".mid")