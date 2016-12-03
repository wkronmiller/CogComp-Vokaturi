#!/usr/bin/env python
import sys
import scipy.io.wavfile
from loader import *

if __name__ == "__main__":
    print "Activated", Vokaturi

    emotion_probabilities = load_audio()

    print "Fear", emotion_probabilities.fear

