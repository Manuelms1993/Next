from note_seq.protobuf import music_pb2
from google.colab import files
import magenta
import note_seq
import tensorflow
import os
os.chdir("/Users/manuelmontero/PycharmProjects/NEXT")

teapot = note_seq.midi_file_to_note_sequence('resource/mid/Deadmau5/Deadmau5_Strobe_2.mid')

# Import dependencies.
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from note_seq.protobuf import generator_pb2
from note_seq.protobuf import music_pb2

# Initialize the model.
print("Initializing Melody RNN...")
bundle = sequence_generator_bundle.read_bundle_file('content/attention_rnn.mag')
generator_map = melody_rnn_sequence_generator.get_generator_map()
melody_rnn = generator_map['attention_rnn'](checkpoint=None, bundle=bundle)
melody_rnn.initialize()

# Model options. Change these to get different generated sequences!
input_sequence = teapot # change this to teapot if you want
num_steps = 128*2 # change this for shorter or longer sequences
temperature = 0.01 # the higher the temperature the more random the sequence.

# Set the start time to begin on the next step after the last note ends.
last_end_time = (max(n.end_time for n in input_sequence.notes) if input_sequence.notes else 0)
qpm = 128
seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
total_seconds = num_steps * seconds_per_step

#generator_options = generator_pb2.GeneratorOptions()
#generator_options.args['temperature'].float_value = temperature
#generate_section = generator_options.generate_sections.add(start_time=last_end_time + seconds_per_step, end_time=total_seconds)

# Ask the model to continue the sequence.
#sequence = melody_rnn.generate(input_sequence, generator_options)
#note_seq.sequence_proto_to_midi_file(teapot, 'resource/generated/output/stro.mid')
#note_seq.sequence_proto_to_midi_file(sequence, 'resource/generated/output/stro_rnn.mid')



# Import dependencies.
from magenta.models.music_vae import configs
from magenta.models.music_vae.trained_model import TrainedModel

# Initialize the model.
print("Initializing Music VAE...")
music_vae = TrainedModel(
      configs.CONFIG_MAP['cat-mel_2bar_big'],
      batch_size=8,
      checkpoint_dir_or_path='content/mel_2bar_big.ckpt')

generated_sequences = music_vae.sample(n=5, length=2, temperature=0.1, same_z=True)
n = 0
for ns in generated_sequences:
  note_seq.sequence_proto_to_midi_file(ns, "resource/generated/output/ns" + str(n) + ".mid")
  n += 1
