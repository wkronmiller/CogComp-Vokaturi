#!/usr/bin/env python
"""
Test ML model
"""
import loader
from learning import test_model

def _get_in_sample(trained_model):
    """
    Get the in-sample error
    """
    train_features = loader.get_feature_map()
    in_sample_error = test_model(trained_model, train_features)

    print "In sample error", in_sample_error

def main():
    """
    Perform accuracy tests on model
    """
    trained_model = loader.load_model()

    _get_in_sample(trained_model)

if __name__ == "__main__":
    main()
