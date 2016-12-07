#!/usr/bin/env python
import sys
import scipy.io.wavfile
import config
import numpy
from loader import *
from sklearn.neural_network import MLPClassifier
import pickle
import os

CACHE_DIR = 'appCache'
MODEL_FILE = os.path.join(CACHE_DIR, 'model.p')
NUM_FLATTENERS = 4

def listToQueue(in_list):
    out = multiprocessing.Queue()
    for elem in in_list:
        out.put(elem)
    return out

def getFlatFeatures(paths):
    flat_features = []
    for path in paths:
        flat_features += loadAudio(path)
    return flat_features

def learnNeural(a, b):
    a = numpy.array(a)
    b = numpy.array(b)
    y_a = numpy.ones(len(a))
    y_b = numpy.ones(len(b)) * (-1.0)
    print "Arrays", a.shape, b.shape, y_a.shape, y_b.shape
    y = numpy.concatenate((y_a, y_b), axis=0)
    print "y", y.shape
    X = numpy.concatenate((a,b), axis=0)
    print "X", X.shape

#TODO: tune parameters
    classifier = MLPClassifier(solver='lbgfs', alpha=1e-1, hidden_layer_sizes=(5,2), random_state=1)
    return classifier.fit(X,y)

def trainModel():
    print "Activated", Vokaturi
    monotone_features = getFlatFeatures(getWavs(config.monotone_path))
    enthusiastic_features = getFlatFeatures(getWavs(config.enthusiastic_path))
    print "Extracted features"

    trained_model = learnNeural(monotone_features, enthusiastic_features)
    print "Trained model", trained_model
    return trained_model

# Save model
    pickle.dump(trained_model, open(MODEL_FILE, 'wb'))

if __name__ == "__main__":
    trained_model = None
    if os.path.exists(MODEL_FILE):
        print "Loading cached model"
        trained_model = pickle.load(open(MODEL_FILE, 'rb'))
    else:
        trained_model = trainModel()

    print "model", trained_model
