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
        self.centerTemperature = self.values['general']['centerTemperature']

        # inter
        self.interpolate_model = self.values['interpolates']['interpolate_model']
        self.interpolate_limit = self.values['interpolates']['interpolate_limit']
        self.interpolate_primary_secondary = self.values['interpolates']['interpolate_primary_secondary']
        self.interpolate_arp_primary = self.values['interpolates']['interpolate_arp_primary']
        self.interpolate_arp_secondary = self.values['interpolates']['interpolate_arp_secondary']
        self.interpolate_bass_primary = self.values['interpolates']['interpolate_bass_primary']
        self.interpolate_bass_secondary = self.values['interpolates']['interpolate_bass_secondary']
        self.interpolate_pad_primary = self.values['interpolates']['interpolate_pad_primary']
        self.interpolate_pad_secondary = self.values['interpolates']['interpolate_pad_secondary']

        # chords
        self.chords_run = self.values['chords']['chords_run']
        self.chords_scales = self.values['chords']['chords_scales']
        self.chords_by_key = self.values['chords']['chords_by_key']
        self.chords_secondary = self.values['chords']['chords_secondary']

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
        self.secondaryMelody_run = self.values['VAE']['melody_run']
        self.secondaryMelody_numberOfMelodies = self.values['VAE']['melody_numberOfMelodies']
        self.secondaryMelody_steps = self.values['VAE']['melody_steps']
        self.secondaryMelody_vae_model = self.values['VAE']['melody_vae_model']
        self.secondaryMelody_melody_own_vae_ckpt = self.values['VAE']['melody_own_vae_ckpt']

        # bass
        self.bass_run = self.values['bass']['bass_run']
        self.bass_midiPath = self.values['bass']['bass_midiPath']
        self.bass_midiAleatoryPath = self.values['bass']['bass_midiAleatoryPath']
        self.bass_minimumAleatoryNotes = self.values['bass']['bass_minimumAleatoryNotes']
        self.bass_minimunUniqueNotes = self.values['bass']['bass_minimunUniqueNotes']
        self.bass_startTime_extractSubsequence = self.values['bass']['bass_startTime_extractSubsequence']
        self.bass_endTime_extractSubsequence = self.values['bass']['bass_endTime_extractSubsequence']
        self.bass_numberOfMelodies = self.values['bass']['bass_numberOfMelodies']
        self.bass_steps = self.values['bass']['bass_steps']
        self.bass_rnn_model = self.values['bass']['bass_rnn_model']

        # arp
        self.arp_run = self.values['arp']['arp_run']
        self.arp_midiPath = self.values['arp']['arp_midiPath']
        self.arp_midiAleatoryPath = self.values['arp']['arp_midiAleatoryPath']
        self.arp_minimumAleatoryNotes = self.values['arp']['arp_minimumAleatoryNotes']
        self.arp_minimunUniqueNotes = self.values['arp']['arp_minimunUniqueNotes']
        self.arp_startTime_extractSubsequence = self.values['arp']['arp_startTime_extractSubsequence']
        self.arp_endTime_extractSubsequence = self.values['arp']['arp_endTime_extractSubsequence']
        self.arp_numberOfMelodies = self.values['arp']['arp_numberOfMelodies']
        self.arp_steps = self.values['arp']['arp_steps']
        self.arp_rnn_model = self.values['arp']['arp_rnn_model']

        # pad
        self.pad_run = self.values['pad']['pad_run']
        self.pad_midiPath = self.values['pad']['pad_midiPath']
        self.pad_midiAleatoryPath = self.values['pad']['pad_midiAleatoryPath']
        self.pad_minimumAleatoryNotes = self.values['pad']['pad_minimumAleatoryNotes']
        self.pad_minimunUniqueNotes = self.values['pad']['pad_minimunUniqueNotes']
        self.pad_startTime_extractSubsequence = self.values['pad']['pad_startTime_extractSubsequence']
        self.pad_endTime_extractSubsequence = self.values['pad']['pad_endTime_extractSubsequence']
        self.pad_numberOfMelodies = self.values['pad']['pad_numberOfMelodies']
        self.pad_steps = self.values['pad']['pad_steps']
        self.pad_rnn_model = self.values['pad']['pad_rnn_model']
