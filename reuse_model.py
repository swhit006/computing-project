import keras
import numpy as np
import random
import sys

from helper import sample

def generate(custom_seed):

    notes_in_bar = 17 # 16 notes plus a BAR seperator 
    seq_len = 8*notes_in_bar # 8 bars of notes
    bars = 32*notes_in_bar # 32 bars worth of notes to generate by the model
    
    path = 'notes.txt'
    text = open(path).read() # opens the notes.txt file and prints the length
    print('corpus length:', len(text))
    
 
    notes = text.split(' ')
    chars = set(notes) # creates a set of every unique note in the text file
    text = notes
    print('amount of notes:', len(text))
    
    char_indices = dict((c, i) for i, c in enumerate(chars)) # maps every unique note to a value (key value pairs)
    next_pred = sorted(list(set(text))) # creates a sorted list of every unique note to draw upon for predicting the next in the sequence
    num_notes = len(char_indices) # integer value of the total number of unique notes in the text file, printed to console
    print('total chars:', len(next_pred))
    
    sentences = [] # two blank lists, one to contain all the note sequences, and the other to contain the note sequences that follow
    next_chars = []
    for i in range(0, len(text) - seq_len, notes_in_bar):
        sentences.append(text[i: i + seq_len]) # for loop to append the note sequences to the two lists as described above
        next_chars.append(text[i + seq_len])
    print('nb sequences:', len(sentences)) # prints the number of note sequences
    print('Vectorisation...')
    X = np.zeros((len(sentences), seq_len, num_notes), dtype=np.bool) # 3-d array of dimensions, number of note sequences, by sequence length, by number of unique notes
    y = np.zeros((len(sentences), num_notes), dtype=np.bool) # 2-d target array of dimensions, number of note sequences, by number of unique notes
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            X[i, t, char_indices[char]] = 1 # double for loop to append both X and y with their respective values for one-hot encoded notes
        y[i, char_indices[next_chars[i]]] = 1

    result_directory = 'results/' # directory to store the resulting text files
    
    filepath_model = '%smodel.h5' % result_directory # looks in the results directory for a 'model.h5' file
    model = keras.models.load_model(filepath_model) # loads the model

    start_index = random.randint(0, len(text) - seq_len - 1) # random value for seed

    if custom_seed:
        seed_path = 'seed.txt' # opens seed.txt if custom seed is selected, prints confirmation to console
        print("Custom seed text applied")
    else:
        print("Custom seed not selected. Random seed to be taken from dataset") # prints confirmation of random seed to console
      
    for temperature in [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]: # temperature values for reweighting probability distributions for next note in sequence
           txt_file = '%stemperature_%4.2f.txt' % (result_directory, temperature) # file name with temperature value
           with open(txt_file, 'w') as f:
               print()
               print('Saving temperature %4.2f to' % temperature, txt_file )
               f.write('temperature:%4.2f\n' % temperature) # writes the temperature value to the beginning of the text file
    
               generated = []
               
               if custom_seed:         
                   seed_sentence = open(seed_path).read() # if custom seed is selected, chooses this for seed
                   seed=seed_sentence.split(' ')
               else:	 
                   seed = text[start_index: start_index + seq_len] # if no custom seed, takes random seed from dataset
                   
               sentence = seed				  
               generated = generated + sentence # appends the seed to the start of the text file
                   
               for i in range(bars):
                   x = np.zeros((1, seq_len, num_notes)) # creates a new numpy array for dimensions 1, by 8 bars, by number of unique notes
                   
                   for j, char in enumerate(sentence):
                       x[0, j, char_indices[char]] = 1. # appends the seed sentence to the beginning of the numpy array x
    
                   preds = model.predict(x, verbose=0)[0] # generates the softmax probability distribution with respect to the seed and what the model has learned
                   next_index = sample(preds, temperature) # reweights the probability distribution by the temperature and chooses next note in sequence
                   next_char = next_chars[next_index] # finds the note value in the list of notes
                   
                   generated.append(next_char) # appends the predicted note to the end of the already generated notes
                   sentence = sentence[1:]
                   sentence.append(next_char)
    
                   sys.stdout.flush() # flushes the buffer, meaning everything in the buffer is written before proceeding to next step loop
    
               if custom_seed:
                   f.write(sentence + '\n')
               else:
                   f.write(' '.join(sentence) + '\n')
                   
               f.write(' ' .join(generated))
               
if __name__=='__main__':

    custom_seed=False # user can select if they wish to use a custom seed here
    generate(custom_seed=custom_seed) # begin process of generating new notes