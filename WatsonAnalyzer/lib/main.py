#!/usr/bin/env python
#pylint: skip-file

"""
Create Watson sentiment predictions based on incoming audio
"""
from rabbit_client import RabbitConnection
from shared_config import RABBIT_HOST, RABBIT_PORT, RATE
import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
import speech_recognition as sr
from os import path
import wave
import pyaudio
audio_group = []


def _handle_audio(audio_data_):# pylint: disable=unused-argument
    """
    Handle incoming audio string and send to Watson for
    Speech to Text
    """
    #print "TODO: process audio data thru watson here"

    #!/usr/bin/env python3
    p = pyaudio.PyAudio()

    wf = wave.open("temp_audio.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(audio_data_)
    wf.close()


    #audio_group.append(audio_data_)
    #audio_data = sr.AudioData(audio_data_, RATE, 2)
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "temp_audio.wav")

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source) # read the entire audio file



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
