#!/usr/bin/env python
"""
Neural Network learning utilities
"""
import os
import pickle
import numpy
from sklearn.neural_network import MLPClassifier # pylint: disable=import-error
from sklearn import svm
import config
import loader

def _learn_neural(feature_map, **kwargs):
    """
    Train neural network on data from two classes
    """
    x_all = None
    y_all = None
    print "feature map", feature_map.keys()
    for class_id in feature_map.keys():
        x_n = numpy.array(feature_map[class_id])
        y_n = numpy.ones(len(x_n)) * float(class_id)
        print "Adding class %d" % float(class_id)
        if x_all is None:
            x_all = x_n
            y_all = y_n
        else:
            x_all = numpy.concatenate((x_all, x_n), axis=0)
            y_all = numpy.concatenate((y_all, y_n), axis=0)
    print "y's", y_all

#TODO: tune parameters (adam is optimized stochastic gradient descent, alpha is penalty)
    classifier = MLPClassifier(**kwargs)
    #classifier = svm.SVC(C=1000) #TODO: remove
    return classifier.fit(x_all, y_all)

def train_model(feature_map=None, hidden_layer_sizes=(100, 9), **kwargs):
    """
    Train neural network on audio in reference folders
    """
    if feature_map is None:
        feature_map = loader.get_feature_map()
        print "Extracted features"

    trained_model = _learn_neural(feature_map,
                                  hidden_layer_sizes=hidden_layer_sizes,
                                  **kwargs)
    print "Trained model", trained_model
    # Save model
    pickle.dump(trained_model, open(config.MODEL_FILE, 'wb'))
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
        misclassification_count += len([x for x in trained_model.predict(feature_list)
                                       if int(numpy.sign(x)) != int(classification)]) # pylint: disable=no-member
        total_count += len(feature_list)
    return float(misclassification_count) / float(total_count)

def main():
    """
    Perform default training operations
    """
    if os.path.exists(config.FEATURES_FILE):
        feature_map = pickle.load(open(config.FEATURES_FILE, 'rb'))
    else:
        print "%s does not exist" % config.FEATURES_FILE
        feature_map = loader.get_feature_map()
        pickle.dump(feature_map, open(config.FEATURES_FILE, 'wb'))

    trained_model = train_model(feature_map, activation='tanh', max_iter=1000, learning_rate='adaptive')

    print "E_in:", test_model(trained_model, feature_map)

if __name__ == "__main__":
    main()
