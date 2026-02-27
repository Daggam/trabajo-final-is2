import os

SERVICE_NAME = "api-configuracion"
APP_VERSION = "1.0.0"

BUILD_TIME = os.getenv("BUILD_TIME", "unknown")
BASE_IMAGE = os.getenv("BASE_IMAGE", "python:3.12-slim")
