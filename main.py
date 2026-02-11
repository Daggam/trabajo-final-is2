from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def prueba():
    return "Hola mundo"