from fastapi import FastAPI
import platform
from settings import *

app = FastAPI(
    title="API de Configuración",
    description="API REST para consulta de versión, configuración y estado del sistema",
    version="1.0.0"
)


@app.get("/")
def prueba():
    return "Hola mundo"

@app.get("/config")
def config():
    return {
        "app_env": APP_ENV,
        "port": PORT
    }

@app.get("/version")
def version():
    return {
        "service_name":SERVICE_NAME,
        "app_version": app.version,
        "python_version": platform.python_version(),
        "environment":"docker"
    }

@app.get("/build")
def build():
    return {
        "build_time": BUILD_TIME,
        "base_image": BASE_IMAGE
    }


