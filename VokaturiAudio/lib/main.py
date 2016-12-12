#!/usr/bin/env python
"""
Driver for Vokaturi-based voice tone analyzer
"""
import sys
import time
import config
import loader
import audio_processor
import pika
from rabbit_client import RabbitConnection
from shared_config import RABBIT_HOST, RABBIT_PORT

DECISION_THRESHOLD = .65

def _prediction_to_word(prediction):
    """
    Convert predicted class to class's name
    """
    (prediction_class, [boring_confidence, engaging_confidence]) = prediction
    if prediction_class == config.ENTHUSIASTIC_CLASS and engaging_confidence > DECISION_THRESHOLD:
        return "Engaging {0}".format(engaging_confidence)
    if prediction_class == config.MONOTONE_CLASS and boring_confidence > DECISION_THRESHOLD:
        return "Boring {0}".format(boring_confidence)
    return "Meh (boring: {0}, engaging: {1})".format(boring_confidence, engaging_confidence)

def predict(trained_model, features):
    """
    Perform live prediction using trained model
    """
    features = features.reshape(1, -1)
    prediction = map(_prediction_to_word,
                     zip(trained_model.predict(features),
                         trained_model.predict_proba(features)))
    sys.stderr.write("You are being " + str(prediction[0]) + "\n")

def main():
    """
    Program entrypoint
    """
    sys.stdout.write("Starting Vokaturi\n")
    trained_model = loader.load_model()

    if trained_model is None:
        raise Exception("No trained model available")

    sys.stdout.write("loaded model\n")

    sys.stdout.write("Connecting to rabbit\n")

    def _handle_audio(audio_data):
        features = audio_processor.extract_features_from_string(audio_data)
        predict(trained_model, features)

    while True:
        while True:
            try:
                client = RabbitConnection(RABBIT_HOST, RABBIT_PORT)
                break
            except pika.exceptions.AMQPConnectionError:
                time.sleep(5)
        client.add_audio_incoming_callback(_handle_audio)

        try:
            client.start()
        except KeyboardInterrupt:
            break
        except pika.exceptions.IncompatibleProtocolError:
            sys.stderr.write("Pika connection error\n")
    client.stop()

if __name__ == "__main__":
    main()
