import os

SERVICE_NAME = "api-configuracion"
BUILD_TIME = os.getenv("BUILD_TIME", "unknown")
BASE_IMAGE = os.getenv("BASE_IMAGE", "python:3.12-slim")
