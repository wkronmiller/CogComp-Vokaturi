#!/bin/bash
source Configuration/env.sh

./RabbitMQ/start.sh && sleep 5

(cd AudioRecorder && ./start.sh) &
audio_proc=$!

(cd VokaturiAudio/ && ./start.sh) &
vokaturi_proc=$!

echo "All started"

wait "$audio_proc" "$vokaturi_proc"

echo "All stopped"

#TODO: start watson
