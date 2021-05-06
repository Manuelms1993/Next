import os
import logging
from generator.generator import MusicGenerator
from config.Configuration import Configuration
from utils.constant import Constants
os.chdir(Constants.MAIN_PATH)
logging.basicConfig(level = logging.INFO)
import math
from persistence.loaders import loadSequence
from utils.utilities import calculateTemperature
import time

if __name__ == "__main__":
    start = time.time()
    logging.info("Reading config file...")
    configuration = Configuration("config/config.yaml")
    logging.info("Creating Generator...")
    generator = MusicGenerator(configuration)
    logging.info("Executing Generator...")
    generator.execute()
    logging.info("Execution time: " + str(time.time()-start))
    # calculateTemperature()




