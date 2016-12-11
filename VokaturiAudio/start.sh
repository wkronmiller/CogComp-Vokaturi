#!/bin/bash
source ../Configuration/env.sh
cd lib && \
    ./main.py localhost $RABBIT_PORT & \
    cd -
