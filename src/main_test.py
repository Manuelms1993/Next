import os
from utils.constant import Constants
os.chdir(Constants.MAIN_PATH)
import note_seq
from note_seq.protobuf import music_pb2
from persistence.writers import writeSequence
from utils.NoteSequenceUtils import secondsDuration

if __name__ == "__main__":
    song = "resources/mid/lotofmidi/midifile with lyrics 554 songs/midifile with lyrics 554 songs/Jason Derulo - In My Head.mid"
    sequence = note_seq.midi_file_to_note_sequence(Constants.MAIN_PATH + "/" + song)

    noteSeq = music_pb2.NoteSequence()
    noteSeq.tempos.add(qpm=128)
    for note in [n for n in sequence.notes]:
        if note.program == 38:
            noteSeq.notes.add(pitch=note.pitch,
                              start_time=note.start_time,
                              end_time=note.end_time,
                              velocity=note.velocity,
                              program=33)
    noteSeq.total_time = secondsDuration(noteSeq)

    writeSequence(noteSeq, Constants.MAIN_PATH + "/resources/generated/output", "multi")
