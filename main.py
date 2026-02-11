from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def prueba():
    return "Hola mundo"


@app.get("/runtime")
def runtime():
    ## memory usage
    ## CPU usage
    ## Uptime
    ## Execution Details
    ## Pratform/Env Details