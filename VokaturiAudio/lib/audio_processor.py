"""
Handles recording of audio
"""
import numpy
import loader
from shared_config import RATE

def extract_features_from_string(in_data):
    """
    Parse raw audio, extract features
    """
    data = numpy.fromstring(in_data, dtype=numpy.int16)
    return loader.extract_features(RATE, data)
