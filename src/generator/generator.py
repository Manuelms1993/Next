from config.Configuration import Configuration
from utils.FSUtils import constructOutputPath, dirExist, createDirIfNotExist
from utils.constant import Constants
import logging
from generator.magentaModels.MelodyRNN import initializeRNNModel, predictRNNSequence
from persistence.loaders import loadSequence
from persistence.writers import writeSequence
from utils.NoteSequenceUtils import cutSequence
from utils.NoteSequenceUtils import secondsDuration

class MusicGenerator:

    configuration = None

    def __init__(self, configuration: Configuration) -> None:
        super().__init__()
        self.configuration = configuration

    def execute(self):

        path = constructOutputPath(self.configuration.trackName)
        if (not dirExist(path)):
            logging.info("Path not exist, creating: " + path)
            createDirIfNotExist(path)
            self.__predictPrimaryMelody(path)
        else:
            logging.info("Path exist: " + path)
            pass

    def __predictPrimaryMelody(self, path):

        # creating some paths
        primaryPath = path + "/primaryMelody"
        createDirIfNotExist(primaryPath)
        infoPath = path + "/info"
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

            for i in range(self.configuration.primary_numberOfMelodies):
                logging.info("    Generating melody (" + model + "): " + str(i))

                temperature = i/self.configuration.primary_numberOfMelodies + 0.0000000001
                predictedSequence = predictRNNSequence(melody_rnn=melody_rnn,
                                             steps=self.configuration.primary_steps,
                                             sequence=sequenceCut,
                                             temperature=temperature)

                filename = "p" \
                           + str(i) \
                           + "_" \
                           + str(round(secondsDuration(predictedSequence), 1)) \
                           + "s_" \
                           + str(round(temperature, 3))
                writeSequence(sequence=predictedSequence, path=modelPath, name=filename)

