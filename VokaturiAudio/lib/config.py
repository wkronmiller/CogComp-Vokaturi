"""
Configuration settings for project
"""
import os

OS = 'MAC'
# OS = 'WIN32'
# OS = 'WIN64'

NUM_FEATURES = 5

ENTHUSIASTIC_PATH = '../trainData/enthusiastic'
ENTHUSIASTIC_CLASS = 1.0

MONOTONE_PATH = '../trainData/monotone'
MONOTONE_CLASS = -1.0

CACHE_DIR = '../appCache'
MODEL_FILE = os.path.join(CACHE_DIR, 'model.p')
FEATURES_FILE = os.path.join(CACHE_DIR, 'features.p')

# Number of processes used to extract audio features
LOADER_PROCESSES = 10
