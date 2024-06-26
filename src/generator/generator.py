from config.Configuration import Configuration
from utils.FSUtils import constructOutputPath, dirExist, createDirIfNotExist
import logging
from generator.magentaModels.MelodyRNN import initializeRNNModel, predictRNNSequence
from generator.magentaModels.modelVAE import getTrainedModelVAE, generateVAE
from persistence.loaders import loadSequence
from persistence.writers import writeSequence
from utils.NoteSequenceUtils import cutSequence
from utils.NoteSequenceUtils import secondsDuration, getInstrumentPath
from utils.constant import Constants
from utils.utilities import calculateTemperature
from collections import Counter
from generator.magentaModels.interpolate import interpolate
import os
from glob import glob
import random

class MusicGenerator:

    configuration = None
    path = None

    def __init__(self, configuration: Configuration) -> None:
        """

        :rtype: object
        """
        super().__init__()
        self.configuration = configuration

    def execute(self):

        self.path = constructOutputPath(self.configuration.trackName)
        createDirIfNotExist(self.path)
        infoPath = self.path + "/general"
        createDirIfNotExist(infoPath)

        if (not dirExist(self.path + "/secondaryMelody") and self.configuration.secondaryMelody_run):
            self.__runVAE(self.path + "/secondaryMelody",
                          self.configuration.secondaryMelody_numberOfMelodies,
                          self.configuration.secondaryMelody_vae_model,
                          self.configuration.secondaryMelody_steps)


        if (not dirExist(self.path + "/primaryMelody") and self.configuration.primary_run):
            self.__run_rnnModel(
                 pathrnn=self.path + "/primaryMelody",
                 stringId="primaryMelody",
                 midiPath=self.configuration.primary_midiPath,
                 minNotes=self.configuration.primary_minimumAleatoryNotes,
                 minUniques=self.configuration.primary_minimunUniqueNotes,
                 midiAleatoryPath=self.configuration.primary_midiAleatoryPath,
                 startSelectionTime=self.configuration.primary_startTime_extractSubsequence,
                 endSelectionTime=self.configuration.primary_endTime_extractSubsequence,
                 bpm=self.configuration.bpm,
                 models=self.configuration.primary_rnn_model,
                 steps=self.configuration.primary_steps,
                 numberOfMelodies=self.configuration.primary_numberOfMelodies)

        if (not dirExist(self.path + "/drums") and self.configuration.drums_run):
            self.__runVAE(self.path + "/drums",
                          self.configuration.drums_numberOfMelodies,
                          self.configuration.drums_vae_model,
                          self.configuration.drums_steps)

        if (not dirExist(self.path + "/bass") and self.configuration.bass_run):
            self.__run_rnnModel(
                 pathrnn=self.path + "/bass",
                 stringId="bass",
                 midiPath=self.configuration.bass_midiPath,
                 minNotes=self.configuration.bass_minimumAleatoryNotes,
                 minUniques=self.configuration.bass_minimunUniqueNotes,
                 midiAleatoryPath=self.configuration.bass_midiAleatoryPath,
                 startSelectionTime=self.configuration.bass_startTime_extractSubsequence,
                 endSelectionTime=self.configuration.bass_endTime_extractSubsequence,
                 bpm=self.configuration.bpm,
                 models=self.configuration.bass_rnn_model,
                 steps=self.configuration.bass_steps,
                 numberOfMelodies=self.configuration.bass_numberOfMelodies)


        if (not dirExist(self.path + "/arp") and self.configuration.arp_run):
            self.__run_rnnModel(
                 pathrnn=self.path + "/arp",
                 stringId="arp",
                 midiPath=self.configuration.arp_midiPath,
                 minNotes=self.configuration.arp_minimumAleatoryNotes,
                 minUniques=self.configuration.arp_minimunUniqueNotes,
                 midiAleatoryPath=self.configuration.arp_midiAleatoryPath,
                 startSelectionTime=self.configuration.arp_startTime_extractSubsequence,
                 endSelectionTime=self.configuration.arp_endTime_extractSubsequence,
                 bpm=self.configuration.bpm,
                 models=self.configuration.arp_rnn_model,
                 steps=self.configuration.arp_steps,
                 numberOfMelodies=self.configuration.arp_numberOfMelodies)

        if (not dirExist(self.path + "/pad") and self.configuration.pad_run):
            self.__run_rnnModel(
                 pathrnn=self.path + "/pad",
                 stringId="pad",
                 midiPath=self.configuration.pad_midiPath,
                 minNotes=self.configuration.pad_minimumAleatoryNotes,
                 minUniques=self.configuration.pad_minimunUniqueNotes,
                 midiAleatoryPath=self.configuration.pad_midiAleatoryPath,
                 startSelectionTime=self.configuration.pad_startTime_extractSubsequence,
                 endSelectionTime=self.configuration.pad_endTime_extractSubsequence,
                 bpm=self.configuration.bpm,
                 models=self.configuration.pad_rnn_model,
                 steps=self.configuration.pad_steps,
                 numberOfMelodies=self.configuration.pad_numberOfMelodies)

        if self.configuration.interpolate_primary_secondary:
            self.__interpolate(self.path + "/primaryMelody", self.path + "/secondaryMelody", "primVSsec")
        if self.configuration.interpolate_arp_primary:
            self.__interpolate(self.path + "/arp", self.path + "/primaryMelody", "arpVSprim")
        if self.configuration.interpolate_arp_secondary:
            self.__interpolate(self.path + "/arp", self.path + "/secondaryMelody", "arpVSsec")
        if self.configuration.interpolate_bass_primary:
            self.__interpolate(self.path + "/bass", self.path + "/primaryMelody", "bassVSprim")
        if self.configuration.interpolate_bass_secondary:
            self.__interpolate(self.path + "/bass", self.path + "/secondaryMelody", "bassVSsec")
        if self.configuration.interpolate_pad_primary:
            self.__interpolate(self.path + "/pad", self.path + "/primaryMelody", "padVSprim")
        if self.configuration.interpolate_pad_secondary:
            self.__interpolate(self.path + "/pad", self.path + "/secondaryMelody", "padVSsec")


    def __runVAE(self, pathVAE, n_melodies, models, steps):

        createDirIfNotExist(pathVAE)

        for model in models:

            loadedModel = getTrainedModelVAE(model)
            modelPath = pathVAE + "/" + model
            createDirIfNotExist(modelPath)

            for step in steps:
                for i in range(n_melodies):

                    logging.info("    Generating melody (" + model + "): " + str(i) + ", step = " + str(step))

                    temperature = calculateTemperature(n_melodies, i, self.configuration.centerTemperature)
                    sequence = generateVAE(loadedModel, 1, step, temperature)[0]

                    if (secondsDuration(sequence)<=3):
                        logging.warning("Aborting writting, sequence have less than 3 seconds")
                        continue

                    filename = "vae_" \
                               + str(i) \
                               + "_" \
                               + str(round(secondsDuration(sequence), 1)) \
                               + "_" \
                               + str(step) \
                               + "_" \
                               + str(round(temperature, 3))
                    writeSequence(sequence=sequence, path=modelPath, name=filename)

    def __run_rnnModel(self,
                     pathrnn,
                     stringId,
                     midiPath,
                     minNotes,
                     minUniques,
                     midiAleatoryPath,
                     startSelectionTime,
                     endSelectionTime,
                     bpm,
                     models,
                     steps,
                     numberOfMelodies):

        # creating some paths
        createDirIfNotExist(pathrnn)

        # loading and cut sequence
        sequenceCut = self.__loadCutSequence(midiPath,
                                             midiAleatoryPath,
                                             minNotes,
                                             minUniques,
                                             bpm,
                                             startSelectionTime,
                                             endSelectionTime, stringId)

        for model in models:

            logging.info("Starting model: " + model)
            modelPath = pathrnn + "/" + model
            createDirIfNotExist(modelPath)
            melody_rnn = initializeRNNModel(model=model)

            for step in steps:
                for i in range(numberOfMelodies):
                    logging.info("    Generating melody (" + model + "): " + str(i) + ", step = " + str(step))

                    temperature = calculateTemperature(numberOfMelodies, i, self.configuration.centerTemperature)
                    predictedSequence = predictRNNSequence(melody_rnn=melody_rnn,
                                                           steps=step,
                                                           sequence=sequenceCut,
                                                           temperature=temperature)

                    if (secondsDuration(predictedSequence)<=3):
                        logging.warning("Aborting writting, sequence have less than 3 seconds")
                        continue

                    filename = "rnn_" \
                               + str(i) \
                               + "_" \
                               + str(round(secondsDuration(predictedSequence), 1)) \
                               + "s_" \
                               + str(round(temperature, 3))
                    writeSequence(sequence=predictedSequence,
                                  path=modelPath,
                                  name=filename,
                                  outputProgram=getInstrumentPath(pathrnn))

    def __loadCutSequence(self, midiPath: str,
                          midiAleatoryPath: str,
                          minNotes,
                          minUniques,
                          bpm: int,
                          startSelectionTime: int,
                          endSelectionTime: int,
                          stringId: str):
        """

        :rtype: NoteSequence
        """
        pathMidi =  None if (midiPath == None) else Constants.MAIN_PATH + "/" + midiPath
        pathAleatoryMidi =  None if (midiAleatoryPath == None) else Constants.MAIN_PATH + "/" + midiAleatoryPath

        # load and cut
        aleatoryLength = 1
        correct = False
        while not correct:
            logging.info("Start selecting track")
            sequence = loadSequence(pathMidi, pathAleatoryMidi, bpm, True)
            sequenceCut = cutSequence(sequence,
                                      startSelectionTime,
                                      endSelectionTime,
                                      aleatoryCut = True,
                                      aleatoryDuration = aleatoryLength)

            if pathMidi != None:
                correct = True
            else:
                uniques = Counter([n.pitch for n in sequenceCut.notes]).keys()
                if (len(sequenceCut.notes) >= int(minNotes)) and len(uniques) >= int(minUniques):
                    correct = True
                    logging.info("Track is valid. Notes: " + str(len(sequenceCut.notes)) + ", Uniques: " + str(len(uniques)))
                else:
                    logging.info("Track is not valid. Notes: " + str(len(sequenceCut.notes)) + ", Uniques: " + str(len(uniques)))
                    aleatoryLength += 0.1

        # Save master sequences
        writeSequence(sequence=sequence, path=self.path + "/general", name="selectedTrack_" + stringId)
        writeSequence(sequence=sequenceCut, path=self.path + "/general", name="selectedTrack_" + stringId + "_cut")

        return sequenceCut

    def __interpolate(self, pathTrack, interPath, name):

        if not dirExist(pathTrack) or not dirExist(interPath): return

        interpolatePath = pathTrack + "/interpolate"

        # creating some paths
        createDirIfNotExist(interpolatePath)

        logging.info("Interpolate path1: " + str(pathTrack))
        logging.info("Interpolate path2: " + str(interPath))

        filesTrack = [y for x in os.walk(pathTrack) for y in glob(os.path.join(x[0], '*.mid'))]
        filesInter = [y for x in os.walk(interPath) for y in glob(os.path.join(x[0], '*.mid'))]

        if (len(filesTrack) == 0):
            logging.info("No tracks to interpolate in " + pathTrack)
            return
        if (len(filesInter) == 0):
            logging.info("No tracks to interpolate in " + filesInter)
            return

        lens = [8, 16]
        steps = [16, 32]

        model = getTrainedModelVAE(self.configuration.interpolate_model)

        i = 0
        exp = 0
        while i < self.configuration.interpolate_limit:

            f1 = random.choice(filesTrack)
            f2 = random.choice(filesInter)
            l = random.choice(lens)
            s = random.choice(steps)
            temperature = calculateTemperature(self.configuration.interpolate_limit,
                                               i,
                                               self.configuration.centerTemperature)

            try:
                seq = interpolate(model, f1, f2, self.configuration.bpm, l, s, temperature)

                if (secondsDuration(seq) <= 3):
                    logging.warning("Aborting writting, sequence have less than 3 seconds")
                    continue

                if not seq == None:
                    writeSequence(sequence=seq, path=interpolatePath, name=name + str(i), outputProgram=getInstrumentPath(pathTrack))
                    i += 1
            except:
                logging.warning("Exception interpolate")
                exp += 1
                if (exp >= 30):
                    logging.warning("Abort interpolate in " + str(interPath))
                    return