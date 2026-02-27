from fastapi import FastAPI
import platform
from settings import (
    BUILD_TIME,
    BASE_IMAGE
)

app = FastAPI(
    title="API de Configuración",
    description="API REST para consulta de versión, configuración y estado del sistema",
    version="1.0.0"
)

@app.get("/build")
def build():
    return {
        "build_time": BUILD_TIME,
        "base_image": BASE_IMAGE
    }

