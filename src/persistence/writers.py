
import note_seq
import os
from datetime import datetime
from utils.FSUtils import rename
from note_seq.protobuf import music_pb2
from utils.NoteSequenceUtils import secondsDuration

def writeSequence(sequence, path, name, outputProgram = None):
    filepath = path + "/" + str(name) + ".mid"
    tmpName = path + "/" + str(datetime.now()).replace(" ", "_").replace(":", "_") + ".mid"

    if (not outputProgram == None):
        noteSeq = music_pb2.NoteSequence()
        for note in [n for n in sequence.notes]:
                noteSeq.notes.add(pitch = note.pitch,
                                  start_time = note.start_time,
                                  end_time = note.end_time,
                                  velocity = note.velocity,
                                  program = outputProgram)
        noteSeq.total_time = secondsDuration(noteSeq)
        note_seq.sequence_proto_to_midi_file(noteSeq, tmpName)
    else:
        note_seq.sequence_proto_to_midi_file(sequence, tmpName)
    try:
        rename(tmpName, filepath)
    except:
        os.remove(tmpName)