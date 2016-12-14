#!/usr/bin/env python
"""
Create Watson sentiment predictions based on incoming audio
"""
from rabbit_client import RabbitConnection
from shared_config import RABBIT_HOST, RABBIT_PORT
import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1

def _handle_audio(audio_data):# pylint: disable=unused-argument
    """
    Handle incoming audio string and send to Watson for
    Speech to Text
    """
    print "TODO: process audio data thru watson here"

    #!/usr/bin/env python3

    import speech_recognition as sr

    # obtain path to "english.wav" in the same folder as this script
    #from os import path
    #AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")
    #AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
    #AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

    # use the audio file as the audio source
    r = sr.Recognizer()
    #with sr.AudioFile(AUDIO_FILE) as source:
    #    audio = r.record(source) # read the entire audio file

    audio = audio_data

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


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
