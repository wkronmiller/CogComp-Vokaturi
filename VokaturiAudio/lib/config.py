"""
Configuration settings for project
"""
import os
import platform

def _get_os():
    return {
        'Linux': 'LINUX64',
        'Darwin': 'MAC'
    }[platform.system()]
#OS = 'MAC'
#OS = 'LINUX64'
# OS = 'WIN32'
# OS = 'WIN64'
OS = _get_os()

NUM_FEATURES = 5

ENTHUSIASTIC_PATH = '../trainData/enthusiastic'
ENTHUSIASTIC_CLASS = 1.0

MONOTONE_PATH = '../trainData/monotone'
MONOTONE_CLASS = -1.0

TEST_PATH = '../testData'
TEST_MONOTONE_PATH = os.path.join(TEST_PATH, 'monotone')
TEST_ENTHUSIASTIC_PATH = os.path.join(TEST_PATH, 'enthusiastic')

CACHE_DIR = '../appCache'
MODEL_FILE = os.path.join(CACHE_DIR, 'model.p')
FEATURES_FILE = os.path.join(CACHE_DIR, 'features.p')

# Number of processes used to extract audio features
LOADER_PROCESSES = 100
