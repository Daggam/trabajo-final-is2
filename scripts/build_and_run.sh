#!/bin/bash
#EL SCRIPT DEBE EJECUTARSE EN LA CARPETA DEL PROYECTO
DOCKERFILE_F=$1
if [[ -z $1 ]]; then
    DOCKERFILE_F="Dockerfile"
fi
docker build -f $DOCKERFILE_F --no-cache --build-arg START_TIME=$(date +%s) -t tfis2:latest .;
docker run -it -p 8000:8000 tfis2:latest;