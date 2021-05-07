import yaml
import logging

class Configuration:

    # all values
    values = None

    def __init__(self, path):

        with open(path) as f:
            self.values = yaml.safe_load(f)

        logging.info("Configuration: " + str(self.values))

        # General Properties
        self.trackName = self.values['general']['name']
        self.bpm = self.values['general']['bpm']


        # primaryMelody
        self.primary_run = self.values['primaryMelody']['primary_run']
        self.primary_midiPath = self.values['primaryMelody']['primary_midiPath']
        self.primary_midiAleatoryPath = self.values['primaryMelody']['primary_midiAleatoryPath']
        self.primary_minimumAleatoryNotes = self.values['primaryMelody']['primary_minimumAleatoryNotes']
        self.primary_minimunUniqueNotes = self.values['primaryMelody']['primary_minimunUniqueNotes']
        self.primary_startTime_extractSubsequence = self.values['primaryMelody']['primary_startTime_extractSubsequence']
        self.primary_endTime_extractSubsequence = self.values['primaryMelody']['primary_endTime_extractSubsequence']
        self.primary_numberOfMelodies = self.values['primaryMelody']['primary_numberOfMelodies']
        self.primary_steps = self.values['primaryMelody']['primary_steps']
        self.primary_rnn_model = self.values['primaryMelody']['primary_rnn_model']

        # drums
        self.drums_run = self.values['drums']['drums_run']
        self.drums_numberOfMelodies = self.values['drums']['drums_numberOfMelodies']
        self.drums_steps = self.values['drums']['drums_steps']
        self.drums_vae_model = self.values['drums']['drums_vae_model']

        # melody
        self.secondaryMelody_run = self.values['secondaryMelody']['melody_run']
        self.secondaryMelody_numberOfMelodies = self.values['secondaryMelody']['melody_numberOfMelodies']
        self.secondaryMelody_steps = self.values['secondaryMelody']['melody_steps']
        self.secondaryMelody_vae_model = self.values['secondaryMelody']['melody_vae_model']
