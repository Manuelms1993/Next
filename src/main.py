import os
import logging
from generator.generator import MusicGenerator
from config.Configuration import Configuration
from utils.Constant import Constants
os.chdir(Constants.MAIN_PATH)
logging.basicConfig(level = logging.INFO)


if __name__ == "__main__":
    logging.info("Reading config file...")
    configuration = Configuration("config/config.yaml")
    logging.info("Creating Generator...")
    generator = MusicGenerator(configuration)
    logging.info("Executing Generator...")
    generator.execute()

