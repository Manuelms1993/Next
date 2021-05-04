import yaml
import logging

class Configuration:

    values = None

    # General Properties
    trackName = None

    # primary properties
    midiPath = None
    startTime_extractSubsequence = None
    endTime_extractSubsequence = None
    primaryMelodyModel = None
    numberOfMelodies = None
    stepsLenth = None

    def __init__(self, path):

        with open(path) as f:
            self.values = yaml.safe_load(f)

        logging.info("Configuration: " + str(self.values))

        # General Properties
        self.trackName = self.values['general']['name']

        # primaryMelody
        self.midiPath = self.values['primaryMelody']['midiPath']
        self.startTime_extractSubsequence = self.values['primaryMelody']['startTime_extractSubsequence']
        self.endTime_extractSubsequence = self.values['primaryMelody']['endTime_extractSubsequence']
        self.primaryMelodyModel = self.values['primaryMelody']['primaryMelodyModel']
        self.stepsLenth = self.values['primaryMelody']['stepsLenth']
