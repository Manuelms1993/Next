import os
from utils.Constant import Constants

def dirExist(path):
    return os.path.exists(path)

def constructOutputPath(name):
    return Constants.MAIN_PATH + "/" + Constants.OUTPUT_PATH + "/" + name

def createDir(path):
    os.mkdir(path)