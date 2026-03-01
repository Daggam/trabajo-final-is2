#!/bin/bash
docker build --no-cache --build-arg START_TIME=$(date +%s) -t tfis2:latest ../;
docker run -it -p 8000:8000 tfis2:latest;