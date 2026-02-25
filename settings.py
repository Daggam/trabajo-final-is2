import os

SERVICE_NAME = "api-configuracion"

APP_ENV = os.getenv("APP_ENV","production")
PORT = int(os.getenv("PORT",5000))