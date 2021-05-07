from config.Configuration import Configuration
from utils.FSUtils import constructOutputPath, dirExist, createDirIfNotExist
import logging
from generator.magentaModels.MelodyRNN import initializeRNNModel, predictRNNSequence
from generator.magentaModels.modelVAE import getTrainedModelVAE, generateVAE
from persistence.loaders import loadSequence
from persistence.writers import writeSequence
from utils.NoteSequenceUtils import cutSequence
from utils.NoteSequenceUtils import secondsDuration
from utils.constant import Constants
from utils.utilities import calculateTemperature
from collections import Counter

class MusicGenerator:

    configuration = None
    path = None

    def __init__(self, configuration: Configuration) -> None:
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
        else:
            logging.info("melody directory already exist!")

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
        else:
            logging.info("primaryMelody directory already exist!")

        if (not dirExist(self.path + "/drums") and self.configuration.drums_run):
            self.__runVAE(self.path + "/drums",
                          self.configuration.drums_numberOfMelodies,
                          self.configuration.drums_vae_model,
                          self.configuration.drums_steps)
        else:
            logging.info("drums directory already exist!")




    def __runVAE(self, pathVAE, n_melodies, models, steps):

        createDirIfNotExist(pathVAE)

        for model in models:

            loadedModel = getTrainedModelVAE(model)
            modelPath = pathVAE + "/" + model
            createDirIfNotExist(modelPath)

            for step in steps:
                for i in range(n_melodies):

                    logging.info("    Generating melody (" + model + "): " + str(i) + ", step = " + str(step))

                    temperature = calculateTemperature(n_melodies, i, 0.7)
                    sequence = generateVAE(loadedModel, 1, step, temperature)[0]

                    if (secondsDuration(sequence)<=6):
                        logging.warning("Aborting writting, sequence have less than 6 seconds")
                        continue

                    filename = "vae" \
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

                    temperature = calculateTemperature(numberOfMelodies, i, 0.7)
                    predictedSequence = predictRNNSequence(melody_rnn=melody_rnn,
                                                           steps=step,
                                                           sequence=sequenceCut,
                                                           temperature=temperature)

                    if (secondsDuration(predictedSequence)<=6):
                        logging.warning("Aborting writting, sequence have less than 6 seconds")
                        continue

                    filename = "p" \
                               + str(i) \
                               + "_" \
                               + str(round(secondsDuration(predictedSequence), 1)) \
                               + "s_" \
                               + str(round(temperature, 3))
                    writeSequence(sequence=predictedSequence, path=modelPath, name=filename)

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
