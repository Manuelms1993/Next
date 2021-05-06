from config.Configuration import Configuration
from utils.FSUtils import constructOutputPath, dirExist, createDirIfNotExist
import logging
from generator.magentaModels.MelodyRNN import initializeRNNModel, predictRNNSequence
from generator.magentaModels.modelVAE import getTrainedModelVAE, generateVAE
from persistence.loaders import loadSequence
from persistence.writers import writeSequence
from utils.NoteSequenceUtils import cutSequence
from utils.NoteSequenceUtils import secondsDuration

class MusicGenerator:

    configuration = None
    path = None

    def __init__(self, configuration: Configuration) -> None:
        super().__init__()
        self.configuration = configuration

    def execute(self):

        self.path = constructOutputPath(self.configuration.trackName)
        createDirIfNotExist(self.path)

        if (not dirExist(self.path + "/primaryMelody") and self.configuration.primary_run):
            self.__predictPrimaryMelody()
        else:
            logging.info("primaryMelody directory already exist!")


        if (not dirExist(self.path + "/secondaryMelody") and self.configuration.secondaryMelody_run):
            self.__runVAE(self.path + "/secondaryMelody",
                          self.configuration.secondaryMelody_numberOfMelodies,
                          self.configuration.secondaryMelody_vae_model,
                          self.configuration.secondaryMelody_steps)
        else:
            logging.info("melody directory already exist!")

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

                    temperature = i/n_melodies + 0.0000000001
                    sequence = generateVAE(loadedModel, 1, step, temperature)[0]

                    filename = "vae" \
                               + str(i) \
                               + "_" \
                               + str(round(secondsDuration(sequence), 1)) \
                               + "_" \
                               + str(step) \
                               + "_" \
                               + str(round(temperature, 3))
                    writeSequence(sequence=sequence, path=modelPath, name=filename)


    def __predictPrimaryMelody(self):

        # creating some paths
        primaryPath = self.path + "/primaryMelody"
        createDirIfNotExist(primaryPath)
        infoPath = self.path + "/info"
        createDirIfNotExist(infoPath)

        # loading and cut sequence
        sequence = loadSequence(self.configuration.primary_midiPath, self.configuration.bpm, True)
        sequenceCut = cutSequence(sequence,
                                  self.configuration.primary_startTime_extractSubsequence,
                                  self.configuration.primary_endTime_extractSubsequence)

        # Save master sequences
        writeSequence(sequence=sequence, path=infoPath, name="originalMid")
        writeSequence(sequence=sequenceCut, path=infoPath, name="originalCutMid")

        for model in self.configuration.primary_rnn_model:

            logging.info("Starting model: " + model)
            modelPath = primaryPath + "/" + model
            createDirIfNotExist(modelPath)
            melody_rnn = initializeRNNModel(model=model)

            for step in self.configuration.primary_steps:
                for i in range(self.configuration.primary_numberOfMelodies):
                    logging.info("    Generating melody (" + model + "): " + str(i) + ", step = " + str(step))

                    temperature = i/self.configuration.primary_numberOfMelodies + 0.0000000001
                    predictedSequence = predictRNNSequence(melody_rnn=melody_rnn,
                                                 steps=step,
                                                 sequence=sequenceCut,
                                                 temperature=temperature)

                    filename = "p" \
                               + str(i) \
                               + "_" \
                               + str(round(secondsDuration(predictedSequence), 1)) \
                               + "s_" \
                               + str(round(temperature, 3))
                    writeSequence(sequence=predictedSequence, path=modelPath, name=filename)

