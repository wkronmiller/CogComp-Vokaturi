"""
Responsible for loading data and extracting features using Vokaturi
"""
import sys
import os
import scipy.io.wavfile
from config import OS
import numpy
VOKATURI_PATH = "OpenVokaturi-1-2"

sys.path.append(os.path.join(VOKATURI_PATH, 'api'))
import Vokaturi # pylint: disable=wrong-import-position,import-error

def _get_lib_name():
    lib_name = None
    if OS == 'MAC':
        lib_name = 'Vokaturi_mac.so'
    elif OS == 'WIN32':
        lib_name = 'Vokaturi_win32.dll'
    elif OS == 'WIN64':
        lib_name = 'Vokaturi_win64.dll'
    else:
        raise ValueError('Unknown operating system specified in config')
    return lib_name

Vokaturi.load(os.path.join(os.path.join(VOKATURI_PATH, 'lib'), _get_lib_name()))

print "Vokaturi initialized"

PCM_MAX = 32768.0

def _print_props(obj):
    for key in dir(obj):
        if key[0] != '_':
            print "%s: %s" % (key, getattr(obj, key))
def _mk_mono(samples):
    if len(samples.shape) > 1:
        return samples[:, 0]
    return samples

SECONDS_PER_SLICE = 1
def _slice_audio(rate, samples):
    slice_size = rate * SECONDS_PER_SLICE
    indices = range(0, len(samples), slice_size)
    return [samples[index:index+slice_size] for index in indices]

def extract_features(rate, samples):
    """
    Extract features from audio numpy array
    """
    samp_len = len(samples)
    c_buffer = Vokaturi.SampleArrayC(samp_len)
    c_buffer[:] = samples[:] / PCM_MAX

    voice = Vokaturi.Voice(rate, samp_len)
    # Load audio into analyzer
    voice.fill(samp_len, c_buffer)
    # Analyze audio
    cue_strengths = Vokaturi.CueStrengths()

    voice.extract(None, cue_strengths, None)
    voice.destroy()
    return numpy.array([
        cue_strengths.int_ave,
        cue_strengths.int_slo,
        cue_strengths.pit_ave,
        cue_strengths.pit_slo,
        cue_strengths.spc_slo])

def get_wavs(path):
    """
    Get list of relative paths to all wav files in specified folder
    """
    return [os.path.join(path, x) for x in os.listdir(path) if x.endswith('.wav')]

def load_audio(path):
    """
    Load audio and extract features from files in specified path
    """
    (rate, samples) = scipy.io.wavfile.read(path)
    sample_slices = _slice_audio(rate, _mk_mono(samples))
    return [extract_features(rate, x) for x in sample_slices]
