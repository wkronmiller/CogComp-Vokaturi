#!/usr/bin/env python
"""
Program entrypoint script
"""
import sys
from recorder import Recorder
from rabbit_client import RabbitConnection
from rabbit_client import AUDIO_EXCHANGE

RABBIT_HOST = sys.argv[1]
RABBIT_PORT = int(sys.argv[2])

def main():
    """
    Starts rabbit connection and begins recording
    """
    recorder = Recorder()
    connection = RabbitConnection(RABBIT_HOST, RABBIT_PORT)

    def _start_recording(channel):
        def _handle_audio(audio_data):
            print "Sending audio"
            channel.basic_publish(exchange=AUDIO_EXCHANGE, routing_key='', body=audio_data)
        recorder.start_live_recording(_handle_audio)

    connection.register_callback(_start_recording)

    try:
        connection.start()
    except KeyboardInterrupt:
        pass

    connection.stop()
    recorder.stop_recording()

if __name__ == "__main__":
    main()
