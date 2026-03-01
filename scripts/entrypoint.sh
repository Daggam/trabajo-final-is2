#!/bin/bash
export BASE_IMAGE="python:3.12-slim-trixie";

export BUILD_TIME=$(cat build_time.txt);

export APP_ENV="production"

export PORT="8000"

uv run uvicorn main:app --host 0.0.0.0 --port $PORT;