import sys
import os
import scipy.io.wavfile
from config import OS
import config
VOKATURI_PATH = "OpenVokaturi-1-2"

sys.path.append(os.path.join(VOKATURI_PATH, 'api'))
import Vokaturi

lib_name = None
if OS == 'MAC':
    lib_name = 'Vokaturi_mac.so'
elif OS == 'WIN32':
    lib_name = 'Vokaturi_win32.dll'
elif OS == 'WIN64':
    lib_name = 'Vokaturi_win64.dll'
else:
    raise ValueError('Unknown operating system specified in config')

Vokaturi.load(os.path.join(os.path.join(VOKATURI_PATH, 'lib'), lib_name))

print "Vokaturi initialized"

PCM_MAX = 32768.0

def _printProps(obj):
    for key in dir(obj):
        if key[0] != '_':
            print "%s: %s" % (key, getattr(obj, key))
def _mkMono(samples):
    if len(samples.shape) > 1:
        return samples[:,0]
    return samples

def loadAudio(path = config.audio_path ):
    (rate, samples) = scipy.io.wavfile.read(path)
    samples = _mkMono(samples)
    samp_len = len(samples)
    c_buffer = Vokaturi.SampleArrayC(samp_len)
    c_buffer[:] = samples[:] / PCM_MAX
    voice = Vokaturi.Voice(rate, samp_len)
    # Load audio into analyzer
    voice.fill(samp_len, c_buffer)
    # Analyze audio
    cue_strengths = Vokaturi.CueStrengths()
    emotion_probabilities = Vokaturi.EmotionProbabilities()
    voice.extract(None, cue_strengths, emotion_probabilities)
    _printProps(cue_strengths)
    _printProps(emotion_probabilities)
    voice.destroy()
    return emotion_probabilities
#TODO
