from fastapi import FastAPI
import time
import platform
import datetime
import psutil
import os
from settings import *

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


@app.get("/runtime")
def runtime():
    now = time.time()
    proc = psutil.Process()
    vm = psutil.virtual_memory()
    pm = proc.memory_info()

    data = {
        "memory": {
            "system": {
                "total": vm.total,
                "available": vm.available,
                "used": vm.used,
                "percent": vm.percent,
            },
            "process": {
                "rss": pm.rss,
                "vms": pm.vms,
                "percent": proc.memory_percent(),
            },
        },
        "cpu": {
            "cpu_percent": psutil.cpu_percent(interval=0.2),
        },
        "uptime": {
            "system_uptime_seconds": now - psutil.boot_time(),
            "process_uptime_seconds": now - proc.create_time(),
            "process_start_time": datetime.datetime.fromtimestamp(proc.create_time()).isoformat(),
        },
        "execution": {
            "pid": proc.pid,
            "ppid": proc.ppid(),
            "username": proc.username(),
            "threads": proc.num_threads(),
        },
        "platform": {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "timestamp": datetime.datetime.fromtimestamp(now).isoformat(),
    }

    return data