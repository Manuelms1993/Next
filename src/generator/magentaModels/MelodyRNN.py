import magenta
import note_seq
import tensorflow
import os
import random
import sys
from datetime import datetime
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from note_seq.protobuf import generator_pb2
import logging
from utils.constant import Constants

def predictRNNSequence(sequence,
                    melody_rnn,
                    steps,
                    temperature):
    """

    :type sequence: NoteSequence
    :type mellody_rnn
    :type configuration: Configuration
    """
    qpm = sequence.tempos[0].qpm

    # Set the start time to begin on the next step after the last note ends.
    last_end_time = (max(n.end_time for n in sequence.notes) if sequence.notes else 0)
    seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
    total_seconds = steps * seconds_per_step

    logging.info("Generating MIDI sequence with "
                 + str(total_seconds)
                 + " seconds (" + str(steps)
                 + " steps) and BPM = "
                 + str(qpm))

    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = temperature
    generate_section = generator_options.generate_sections.add(start_time=last_end_time + seconds_per_step,
                                                               end_time=total_seconds)
    sequence = melody_rnn.generate(sequence, generator_options)
    return sequence



def initializeRNNModel(model):
    logging.info("Initializing Melody RNN")

    if (model == "basic_rnn"):
        note_seq.notebook_utils.download_bundle('basic_rnn.mag', Constants.DOWLOAD_PATH)
        bundle = sequence_generator_bundle.read_bundle_file(Constants.MELODYRNN_BASIC_RNN)
        logging.info("Basic Melody RNN load")
    elif (model == "mono_rnn"):
        note_seq.notebook_utils.download_bundle('mono_rnn.mag', Constants.DOWLOAD_PATH)
        bundle = sequence_generator_bundle.read_bundle_file(Constants.MELODYRNN_MONO_RNN)
        logging.info("Mono Melody RNN load")
    elif (model == "lookback_rnn"):
        note_seq.notebook_utils.download_bundle('lookback_rnn.mag', Constants.DOWLOAD_PATH)
        bundle = sequence_generator_bundle.read_bundle_file(Constants.MELODYRNN_LOOKBACK_RNN)
        logging.info("Lookback Melody RNN load")
    elif (model == "attention_rnn"):
        note_seq.notebook_utils.download_bundle('attention_rnn.mag', Constants.DOWLOAD_PATH)
        bundle = sequence_generator_bundle.read_bundle_file(Constants.MELODYRNN_ATTENTION_RNN)
        logging.info("Attention Melody RNN load")
    else:
        logging.error("Bad model in melody rnn")
        sys.exit(1)

    generator_map = melody_rnn_sequence_generator.get_generator_map()
    melody_rnn = generator_map[model](checkpoint=None, bundle=bundle)
    melody_rnn.initialize()
    return melody_rnn