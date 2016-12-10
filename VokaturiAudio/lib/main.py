#!/usr/bin/env python -W ignore::DeprecationWarning
"""
Driver for Vokaturi-based voice tone analyzer
"""
import os
import pickle
import warnings
import config
import numpy
import loader
import recorder
from sklearn.neural_network import MLPClassifier # pylint: disable=import-error

# Disable deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

CACHE_DIR = '../appCache'
MODEL_FILE = os.path.join(CACHE_DIR, 'model.p')
NUM_FLATTENERS = 4

def get_flat_features(paths):
    """
    Get a list of extracted features
    """
    flat_features = []
    for path in paths:
        flat_features += loader.load_audio(path)
    return flat_features

def learn_neural(x_1, x_2):
    """
    Train neural network on data from two classes
    """
    x_1 = numpy.array(x_1)
    x_2 = numpy.array(x_2)
    y_1 = numpy.ones(len(x_1))
    y_2 = numpy.ones(len(x_2)) * (-1.0)

    y_all = numpy.concatenate((y_1, y_2), axis=0)
    x_all = numpy.concatenate((x_1, x_2), axis=0)

#TODO: tune parameters (adam is optimized stochastic gradient descent, alpha is penalty,
    classifier = MLPClassifier(solver='adam', alpha=1e-1, hidden_layer_sizes=(5, 2))
    return classifier.fit(x_all, y_all)

def train_model():
    """
    Train neural network on audio in reference folders
    """
    monotone_features = get_flat_features(loader.get_wavs(config.MONOTONE_PATH))
    enthusiastic_features = get_flat_features(loader.get_wavs(config.ENTHUSIASTIC_PATH))
    print "Extracted features"

    trained_model = learn_neural(monotone_features, enthusiastic_features)
    print "Trained model", trained_model
    # Save model
    pickle.dump(trained_model, open(MODEL_FILE, 'wb'))
    print "Cached model"
    return trained_model

def test_model(trained_model, feature_map):
    """
    Generate in-sample error calculation using map of features
    """
    misclassification_count = 0
    total_count = 0
    for classification in feature_map.keys():
        feature_list = feature_map[classification]
        misclassification_count = len([x for x in trained_model.predict(feature_list)
                                       if numpy.sign(x) != classification]) # pylint: disable=no-member
    return float(misclassification_count) / float(total_count)

def _prediction_to_word(prediction):
    """
    Convert predicted class to class's name
    """
    if prediction < 0:
        return "Enthusiastic"
    return "Boring"

def predict_live(trained_model):
    """
    Perform live prediction using trained model
    """
    def feature_callback(live_features):
        """
        Maps audio features to classification
        """
        prediction = map(_prediction_to_word, trained_model.predict(live_features))
        print "You are being", prediction
    recorder.start_live_recording(feature_callback)

def main():
    """
    Program entrypoint
    """
    trained_model = None
    if os.path.exists(MODEL_FILE):
        print "Loading cached model"
        trained_model = pickle.load(open(MODEL_FILE, 'rb'))
    else:
        trained_model = train_model()

    print "model", trained_model

    print "Live prediction"
    predict_live(trained_model)

if __name__ == "__main__":
    main()
