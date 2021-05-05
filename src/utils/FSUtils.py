import os
from utils.constant import Constants

def dirExist(path):
    return os.path.exists(path)

def constructOutputPath(name):
    return Constants.MAIN_PATH + "/" + Constants.OUTPUT_PATH + "/" + name

def createDir(path):
    os.mkdir(path)

def createDirIfNotExist(path):
    if (not dirExist(path)):
        createDir(path)

def rename(a, b):
    os.rename(a, b)