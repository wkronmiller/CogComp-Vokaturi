import pyaudio
import config
import numpy
import time
from loader import extractFeatures

##TODO
"""
@ see https://people.csail.mit.edu/hubert/pyaudio/
"""
CHUNK = 65536
FORMAT = pyaudio.paInt16
RATE = 44100

def _cleanStream(stream, audio):
    stream.stop_stream()
    stream.close()
    if audio is not None:
        audio.terminate()

def _mkStream(audio, callback=None):
    return audio.open(channels=1, format=FORMAT, frames_per_buffer=CHUNK, rate=RATE, input=True, stream_callback=callback)

def getRecordingChunk():
    audio = pyaudio.PyAudio()
    print "Starting recording..."
    stream = _mkStream(audio)
    frames = numpy.array([numpy.fromstring(stream.read(CHUNK), dtype=numpy.int16) for _ in range(int(RATE/CHUNK * config.record_seconds))])
    print "Finished recording..."
    _cleanStream(stream, audio)

    return [extractFeatures(RATE, frame) for frame in frames]

def startLiveRecording(callback):
    playing = True
    def rawCallback(in_data, num_frames, time_data, status_flags):
        data = numpy.fromstring(in_data, dtype=numpy.int16)
        features = extractFeatures(RATE, data)
        if callback is not None:
            callback(features)
        if playing:
            return (None, pyaudio.paContinue)
        return (None, pyaudio.paComplete)
    audio = pyaudio.PyAudio()
    print "Starting live handler"
    stream = _mkStream(audio, rawCallback)
    stream.start_stream()

    print "Waiting for stream to finish"
    SLEEP_EXTRA = 5
    time.sleep(config.record_seconds + SLEEP_EXTRA)
    playing = False
    while stream.is_active():
        time.sleep(.1)
    _cleanStream(stream, audio)

if __name__ == "__main__":
    #print "Testing recorder"
    #print getRecordingChunk()
    print "Testing live recorder"
    startLiveRecording(None)
