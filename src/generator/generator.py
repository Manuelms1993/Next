from config.Configuration import Configuration
from utils.FSUtils import constructOutputPath, dirExist, createDirIfNotExist
from utils.constant import Constants
import logging
from generator.magentaModels.MelodyRNN import initializeRNNModel, predictRNNSequence
from persistence.loaders import loadSequence

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

        primaryPath = path + "/primaryMelody"
        createDirIfNotExist(primaryPath)

        # loading sequence
        sequence = loadSequence(self.configuration.primary_midiPath, self.configuration.bpm, True)

        for model in self.configuration.primary_rnn_model:

            logging.info("Starting model: " + model)
            modelPath = primaryPath + "/" + model
            createDirIfNotExist(modelPath)
            melody_rnn = initializeRNNModel(model=model)

            for i in range(self.configuration.primary_numberOfMelodies):
                logging.info("    Generating melody (" + model + "): " + str(i))

                predictedSequence = predictRNNSequence(melody_rnn=melody_rnn,
                                             steps=self.configuration.primary_steps,
                                             sequence=sequence,
                                             temperature=i/self.configuration.primary_numberOfMelodies)

