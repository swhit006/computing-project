# DeepDrummer

DeepDrummer is a beat generation tool that allows the user to automatically generate new drum patterns with a Generative Long Short-Term Memory Model. This model is trained using sequential drum patterns represented as text documents and outputs entirely new sequences based on patterns derived from the text with elements of semi-random diversity. This is achieved primarily through the use of Python, TensorFlow and Keras.

## Getting Started

The instructions below will guide you on setting up the two environments required to run the project from end-to-end

### Prerequisites

Anaconda3 / Miniconda3

### Installing

Create a Python 3 environment in Anaconda, and install the python3-requirements.txt by running
```
pip install -r python3-requirements.txt
```
The same must be done for a Python 2 environment, running
```
pip install -r python2-requirements.txt
```

This is the simplest way to set-up the environments, however most of the modules contained within the requirements files are not needed. If you run into any issues running the Python 3 environment, it is likely because the requirements.txt installs the wrong version of Python-Midi. The correct version can be found [here](https://github.com/louisabraham/python3-midi) as the standard version of Python-Midi only works in Python 2
