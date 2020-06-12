import os
import glob
import midi

from drum_note_processor import Note, Note_List, min_ppq

def get_note_list(path, output_name):
    f = open(output_name,"w+") #opens output_name as the file to write notes to
    for file in glob.glob(path): # for loop for all midi files in the midi directory
        song = midi.read_midifile(file) #opens a midi file as 'song'
        print("Parsing: " + os.path.basename(file)) #keeps user informed of songs being processed by printing the file name to console
        song.make_ticks_abs() # changes tick values from relative to absolute values
        note_list = Note_List() # creates a new note list for this song
        for track in song:
            for note in track:
                if note.name == 'Note On': #checks if the midi event is a Note On Event
                    c_ticks = note.tick # records the tick value of the event
                    note = Note(note.get_pitch(), c_ticks) # creates a note class with the pitch and tick of the note
                    note_list.add_note(note) # adds the note to the note list
        note_list.simplify_drums() # simplifies the drums and condenses them down to 9 drum voices
        note_list.quantise(min_ppq) # performs quantisation on the note list to sixteenth notes
        note_list_text = note_list.return_as_text() # performs the function to convert the quantised, simplified note list to text
        f.write(note_list_text) # writes the note list to a txt file
    f.close()
    print("Finished!")
    print("Saved as " + output_name)