from fastapi import FastAPI

app = FastAPI(
    title="API de Configuración",
    description="API REST para consulta de versión, configuración y estado del sistema",
    version="1.0.0"
)

@app.get("/")
def prueba():
    return "Hola mundo"