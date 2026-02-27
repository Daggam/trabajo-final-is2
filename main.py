from fastapi import FastAPI
import os
import platform

app = FastAPI(
    title="API de Configuración",
    description="API REST para consulta de versión, configuración y estado del sistema",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "service": SERVICE_NAME,
        "description": "API de información de versión y configuración",
        "endpoints": [
            "/health",
            "/version",
            "/config",
            "/build",
            "/runtime",
            "/docs"
        ]
    }