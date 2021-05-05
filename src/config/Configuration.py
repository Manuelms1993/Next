import yaml
import logging

class Configuration:

    # all values
    values = None

    # General Properties
    trackName = None

    # primary properties
    primary_midiPath = None
    primary_startTime_extractSubsequence = None
    primary_endTime_extractSubsequence = None
    primary_numberOfMelodies = None
    primary_steps = None
    primary_rnn_model = None

    def __init__(self, path):

        with open(path) as f:
            self.values = yaml.safe_load(f)

        logging.info("Configuration: " + str(self.values))

        # General Properties
        self.trackName = self.values['general']['name']

        # primaryMelody
        self.primary_midiPath = self.values['primaryMelody']['primary_midiPath']
        self.primary_startTime_extractSubsequence = self.values['primaryMelody']['primary_startTime_extractSubsequence']
        self.primary_endTime_extractSubsequence = self.values['primaryMelody']['primary_endTime_extractSubsequence']
        self.primary_numberOfMelodies = self.values['primaryMelody']['primary_numberOfMelodies']
        self.primary_steps = self.values['primaryMelody']['primary_steps']
        self.primary_rnn_model = self.values['primaryMelody']['primary_rnn_model']
