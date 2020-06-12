import keras
import numpy as np

def lstm(units, seq_len, num_notes):
    
    # creates a two-layered LSTM model with a dropout layer between the two LSTMs and a dense output layer
    
	model = keras.models.Sequential()
	model.add(keras.layers.LSTM(units, return_sequences=True, input_shape=(seq_len, num_notes)))
	model.add(keras.layers.Dropout(0.2))
	model.add(keras.layers.LSTM(units))
	model.add(keras.layers.Dense(num_notes))
	model.add(keras.layers.Activation('softmax')) # softmax output layer creates a probability distribution for next note in the sequence

	model.compile(loss='categorical_crossentropy', optimizer='adam')
	return model

def sample(preds, temperature=1.0):
    preds = np.log(preds) / temperature # takes input predictions, performs natural logarithm and divides by temp value
    dist = np.exp(preds) / np.sum(np.exp(preds)) # takes input predictions, calculates the exponential of all elements in the array,
                                                 # divides the values by the sum of all the exponential values
    choices = range(len(preds)) # creates a range of numbers of the length of the preds array
    return np.random.choice(choices, p=dist) # returns a value from the range of numbers, weighted by the probabilities created by dist
