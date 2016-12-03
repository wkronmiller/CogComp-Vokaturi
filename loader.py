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

def load_audio(path = config.audio_path ):
    (rate, samples) = scipy.io.wavfile.read(path)
    samp_len = len(samples)
    c_buffer = Vokaturi.SampleArrayC(samp_len)
    c_buffer[:] = samples[:] / 32768.0 #TODO: why this magic number?
    voice = Vokaturi.Voice(rate, samp_len)
    # Load audio into analyzer
    voice.fill(samp_len, c_buffer)
    # Analyze audio
    emotion_probabilities = Vokaturi.EmotionProbabilities()
    voice.extract(None, None, emotion_probabilities)

    voice.destroy()
    return emotion_probabilities
#TODO
