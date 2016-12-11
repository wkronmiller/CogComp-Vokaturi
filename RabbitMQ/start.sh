#!/bin/bash
source ../Configuration/env.sh
echo "WARNING: This will clobber existing docker container named 'rabbit'"
docker rm -f rabbit
docker run -d --name rabbit -p 5672:$RABBIT_PORT rabbitmq:3 && \
    echo "Rabbit server starting"
