#!/usr/bin/env python
"""
Start streaming audio from computer Mic to rabbit MQ
"""
from recorder import Recorder
from rabbit_client import RabbitConnection, AUDIO_EXCHANGE
from shared_config import RABBIT_HOST, RABBIT_PORT

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
