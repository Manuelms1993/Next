
import note_seq
import os
from datetime import datetime
from utils.FSUtils import rename

def writeSequence(sequence, path, name):
    filepath = path + "/" + str(name) + ".mid"
    tmpName = path + "/" + str(datetime.now()).replace(" ", "_").replace(":", "_") + ".mid"
    note_seq.sequence_proto_to_midi_file(sequence, tmpName)
    try:
        rename(tmpName, filepath)
    except:
        os.remove(tmpName)