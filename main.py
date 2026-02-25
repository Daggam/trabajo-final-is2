from fastapi import FastAPI
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