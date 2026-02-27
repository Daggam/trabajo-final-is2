from fastapi import FastAPI
import platform


app = FastAPI(
    title="API de Configuración",
    description="API REST para consulta de versión, configuración y estado del sistema",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/")
def prueba():
    return "Hola mundo"
