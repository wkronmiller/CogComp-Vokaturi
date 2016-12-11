"""
Handles recording of audio
"""
import time
import pyaudio
from shared_config import RATE

# see https://people.csail.mit.edu/hubert/pyaudio/
CHUNK = 65536
FORMAT = pyaudio.paInt16
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

class Recorder(object):
    """
    A live recording utility
    """
    def __init__(self):
        self.playing = False
        self._stream = None
        self._audio = None

    def start_live_recording(self, callback):
        """
        Start async audio processing
        """
        self.playing = True
        def raw_callback(in_data, *_):
            """
            Gracefully handles incoming data
            and calls callback if specified
            """
            if callback is not None:
                callback(in_data)
            if self.playing:
                return (None, pyaudio.paContinue)
            return (None, pyaudio.paComplete)

        self._audio = pyaudio.PyAudio()
        print "Starting live handler"
        self._stream = _mk_stream(self._audio, raw_callback)
        self._stream.start_stream()

    def stop_recording(self):
        """
        End audio recording and clean up
        """
        self.playing = False
        # Wait for stream to end
        while self._stream.is_active():
            time.sleep(.5)
        _clean_stream(self._stream, self._audio)
