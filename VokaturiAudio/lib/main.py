#!/usr/bin/env python -W ignore::DeprecationWarning
"""
Driver for Vokaturi-based voice tone analyzer
"""
import warnings
import config
import loader
import learning
import audio_processor
from rabbit_client import RabbitConnection
from shared_config import RABBIT_HOST, RABBIT_PORT

# Disable deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Confidence cutoff
CUTOFF = .65

def _prediction_to_word(prediction):
    """
    Convert predicted class to class's name
    """
    print prediction
    (prediction_class, [boring_confidence, enthus_confidence]) = prediction
    if prediction_class == config.ENTHUSIASTIC_CLASS and enthus_confidence > CUTOFF:
        return "Enthusiastic"
    if prediction_class == config.MONOTONE_CLASS and boring_confidence > CUTOFF:
        return "Boring"
    return "Meh"

def predict(trained_model, features):
    """
    Perform live prediction using trained model
    """
    prediction = map(_prediction_to_word,
                     zip(trained_model.predict(features),
                         trained_model.predict_proba(features)))
    print "You are being", prediction[0]

def main():
    """
    Program entrypoint
    """
    trained_model = loader.load_model()

    if trained_model is None:
        print "Training model"
        trained_model = learning.train_model()

    print "model", trained_model

    print "Connecting to rabbit"

    client = RabbitConnection(RABBIT_HOST, RABBIT_PORT)

    def _handle_audio(audio_data):
        features = audio_processor.extract_features_from_string(audio_data)
        predict(trained_model, features)

    client.add_audio_incoming_callback(_handle_audio)

    try:
        client.start()
    except KeyboardInterrupt:
        pass
    client.stop()

if __name__ == "__main__":
    main()
