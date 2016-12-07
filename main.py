#!/usr/bin/env python -W ignore::DeprecationWarning
import sys
import scipy.io.wavfile
import config
import numpy
from loader import *
from sklearn.neural_network import MLPClassifier
import pickle
import os
from recorder import startLiveRecording

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

#TODO: tune parameters (adam is optimized stochastic gradient descent, alpha is penalty,
    classifier = MLPClassifier(solver='adam', alpha=1e-1, hidden_layer_sizes=(5,2))
    return classifier.fit(X,y)

def trainModel():
    print "Activated", Vokaturi
    monotone_features = getFlatFeatures(getWavs(config.monotone_path))
    enthusiastic_features = getFlatFeatures(getWavs(config.enthusiastic_path))
    print "Extracted features"

    trained_model = learnNeural(monotone_features, enthusiastic_features)
    print "Trained model", trained_model
    # Save model
    pickle.dump(trained_model, open(MODEL_FILE, 'wb'))
    print "Cached model"
    return trained_model

def testModel(trained_model):
    monotone_features = numpy.array(getFlatFeatures(getWavs(config.monotone_path)))
    print "Extracted monotone features"
    prediction = trained_model.predict(monotone_features)
    print "Generated prediction"
    print "Error rate", float(len(filter(lambda x: x < 0, prediction))) / float(len(prediction))

def _predictionToWord(prediction):
    if prediction < 0:
        return "Enthusiastic"
    return "Boring"

def predictLive(trained_model):
    def featureCallback(live_features):
        prediction = map(_predictionToWord, trained_model.predict(live_features))
        print prediction
    startLiveRecording(featureCallback)

if __name__ == "__main__":
    trained_model = None
    if os.path.exists(MODEL_FILE):
        print "Loading cached model"
        trained_model = pickle.load(open(MODEL_FILE, 'rb'))
    else:
        trained_model = trainModel()

    print "model", trained_model
    print "testing model"
    #testModel(trained_model)

    print "Live prediction"
    predictLive(trained_model)
