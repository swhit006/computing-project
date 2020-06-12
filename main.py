import os
from get_note_list import get_note_list

def main():
    dirpath = os.getcwd() # selects the current working directory as the path
    path = dirpath + "\midi\*.mid" # selects all midi files in the midi directory
    output_name = "old-notes.txt" # outputs the converted files to a text file called old-notes
    get_note_list(path, output_name) # runs the get_note_list function
    with open('notes.txt', 'w') as outfile, open('old-notes.txt', 'r') as infile:
        for line in infile:
            outfile.write(line.replace('  ',' ').strip()) 
            # any double spaced characters as a result of adding a space at the end of BAR are reset to single spaced characters
            # and outputed to notes.txt

if __name__ == '__main__':
  main() #runs the main function on execution