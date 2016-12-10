"""
Handles recording of audio
"""
import time
import pyaudio
import config
import numpy
from loader import extract_features

# see https://people.csail.mit.edu/hubert/pyaudio/
CHUNK = 65536
FORMAT = pyaudio.paInt16
RATE = 44100
# Time to wait before closing audio stream after finished
SLEEP_EXTRA = 5
def _clean_stream(stream, audio):
    """
    Close stream
    """
    stream.stop_stream()
    stream.close()
    if audio is not None:
        audio.terminate()

def _mk_stream(audio, callback=None):
    """
    Create audio stream
    """
    return audio.open(channels=1,
                      format=FORMAT,
                      frames_per_buffer=CHUNK,
                      rate=RATE, input=True,
                      stream_callback=callback)

def get_recording_chunk():
    """
    Get a buffer of recording data
    """
    audio = pyaudio.PyAudio()
    print "Starting recording..."
    stream = _mk_stream(audio)
    frames = numpy.array([numpy.fromstring(stream.read(CHUNK), dtype=numpy.int16)
                          for _ in range(int(RATE/CHUNK * config.RECORD_SECONDS))])
    print "Finished recording..."
    _clean_stream(stream, audio)

    return [extract_features(RATE, frame) for frame in frames]

def start_live_recording(callback):
    """
    Start async audio processing
    """
    playing = True
    def raw_callback(in_data, *_):
        """
        Parse raw audio, extract features, call callback
        """
        data = numpy.fromstring(in_data, dtype=numpy.int16)
        features = extract_features(RATE, data)
        if callback is not None:
            callback(features)
        if playing:
            return (None, pyaudio.paContinue)
        return (None, pyaudio.paComplete)
    audio = pyaudio.PyAudio()
    print "Starting live handler"
    stream = _mk_stream(audio, raw_callback)
    stream.start_stream()

    if config.RECORD_SECONDS is not None:
        print "Waiting for stream to finish"
        time.sleep(config.RECORD_SECONDS + SLEEP_EXTRA)
        playing = False
    while stream.is_active():
        time.sleep(.5)
    _clean_stream(stream, audio)
