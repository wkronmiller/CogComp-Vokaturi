#!/usr/bin/env python
"""
Create Watson sentiment predictions based on incoming audio
"""
from rabbit_client import RabbitConnection
from shared_config import RABBIT_HOST, RABBIT_PORT

def _handle_audio(audio_data):# pylint: disable=unused-argument
    """
    Handle incoming audio string and send to Watson for
    Speech to Text
    """
    print "TODO: process audio data thru watson here"

def main():
    """
    Connect to RabbitMQ and start processing audio
    """
    client = RabbitConnection(RABBIT_HOST, RABBIT_PORT)
    client.add_audio_incoming_callback(_handle_audio)

    try:
        client.start()
    except KeyboardInterrupt:
        pass
    client.stop()

if __name__ == "__main__":
    main()
