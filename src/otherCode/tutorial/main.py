from note_seq.protobuf import music_pb2
from google.colab import files
import magenta
import note_seq
import tensorflow
import os
import random
import sys
from datetime import datetime
os.chdir("/Users/manuelmontero/PycharmProjects/NEXT")
today = datetime.now()

teapot = note_seq.midi_file_to_note_sequence('resource/mid/Deadmau5/deadmau5_TheVeldt.mid')
teapot = note_seq.extract_subsequence(sequence = teapot,
                        start_time = 0,
                        end_time = 1,
                        preserve_control_numbers=None)
print(teapot)

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
temperature = 0.4 # the higher the temperature the more random the sequence.

# Set the start time to begin on the next step after the last note ends.
last_end_time = (max(n.end_time for n in input_sequence.notes) if input_sequence.notes else 0)
qpm = input_sequence.tempos[0].qpm
print("steps_per_quarter: " + str(melody_rnn.steps_per_quarter))
seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
total_seconds = num_steps * seconds_per_step



# Ask the model to continue the sequence.
n = 0
for i in range(10):
    print(i)
    temperature = (i + 0.00001) / 10
    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = temperature
    print(total_seconds)
    print(temperature)
    generate_section = generator_options.generate_sections.add(start_time=last_end_time + seconds_per_step,
                                                               end_time=total_seconds)
    sequence = melody_rnn.generate(input_sequence, generator_options)
    note_seq.sequence_proto_to_midi_file(sequence, "resource/generated/output/gen_" +
                                         str(today) +
                                         str(n) +
                                         "_" +
                                         str(temperature) +
                                         ".mid")
    n+=1
