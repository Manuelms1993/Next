from config.Configuration import Configuration
from utils.FSUtils import constructOutputPath, dirExist, createDir
from utils.Constant import Constants
import logging

class MusicGenerator:

    configuration = None

    def __init__(self, configuration: Configuration) -> None:
        super().__init__()
        self.configuration = configuration

    def execute(self):

        path = constructOutputPath(self.configuration.trackName)
        if (not dirExist(path)):
            logging.info("Path not exist, creating: " + path)
            createDir(path)
        else:
            logging.info("Path exist: " + path)
            pass

