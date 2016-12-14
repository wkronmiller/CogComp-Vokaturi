#!/usr/bin/env python
"""
Test ML model
"""
import loader
from learning import test_model
from config import TEST_MONOTONE_PATH, TEST_ENTHUSIASTIC_PATH

def _get_in_sample(trained_model):
    """
    Get the in-sample error
    """
    train_features = loader.get_feature_map()
    in_sample_error = test_model(trained_model, train_features)

    print "In sample error", in_sample_error

def _get_test_error(trained_model):
    """
    Get out-of-sample error
    """
    test_features = loader.get_feature_map(TEST_MONOTONE_PATH, TEST_ENTHUSIASTIC_PATH)
    test_error = test_model(trained_model, test_features)

    print "Test error", test_error

def main():
    """
    Perform accuracy tests on model
    """
    trained_model = loader.load_model()

    #_get_in_sample(trained_model)
    _get_test_error(trained_model)

if __name__ == "__main__":
    main()
