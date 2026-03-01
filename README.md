# FastAPI + Docker: Contenerización de una REST API.

## Índice
- [Introducción](#introducción)
- [Desarrollo práctico]()
- [Beneficios]()
- [Desafios y consideraciones]()
- [Conclusión]()
- [Referencias]()

## Introducción

En el desarrollo de software moderno, la gestión de configuración es un aspecto fundamental para garantizar la trazabilidad, reproducibilidad y consistencia de los sistemas. 

Las aplicaciones web requieren una correcta administración de versiones, dependencias y entornos de ejecución. En este trabajo se presenta una experiencia práctica utilizando FastAPI para la implementación de una API REST, uv para la gestión de dependencias y Docker para la construcción de un entorno reproducible.

El objetivo es demostrar cómo estas herramientas permiten construir y ejecutar un sistema de manera controlada y verificable.

## Desarrollo Técnico
### Estructura del proyecto
    trabajo-final-is2/
    ├── main.py
    ├── settings.py
    ├── pyproject.toml
    ├── uv.lock
    └── Dockerfile
   
### Implementación de los endpoints
- `/`: El endpoint `/` devuelve un pequeño objeto JSON con metadatos del servicio. Se utiliza como “pantalla de bienvenida” o índice de la API durante el desarrollo. El contenido del JSON se construye a partir de la constante **SERVICE_NAME** en **settings.py** y lista las rutas más relevantes disponibles.
- `/build`: El endpoint `/build` expone información relacionada con la construcción del sistema, incluyendo variables de entorno definidas durante el proceso de build.
- `/runtime:` El endpoint `/runtime` ofrece información del sistema en donde se corre la aplicación: sistema operativo, versión del SO, distribución, usuario, pid, uso de CPU, uso de memoria, tiempo de inicio y fecha de inicio.
- `/health`: El endpoint `/health` permite verificar que el servicio se encuentra en ejecución y respondiendo correctamente. Actua como un mecanismo básico de monitoreo, facilitando la detección rápida de fallas y la validación del estado del sistema.

### Gestión de dependencias con uv

### Contenerización con Docker

Para garantizar un entorno de ejecución consistente y reproducible, se definió un `Dockerfile` que describe la imagen base, las dependencias y el proceso de construcción del servicio.

Se utiliza como base:

    FROM python:3.12-slim-trixie

Las dependencias se instalan mediante uv, utilizando el archivo uv.lock para asegurar versiones exactas:

    RUN uv sync --locked
Durante la construcción del contenedor se calcula dinámicamente el tiempo de build, el cual es utilizado por el endpoint /build:

    ARG START_TIME
    RUN BUILD_TIME=$(( $(date +%s) - $START_TIME)) && echo $BUILD_TIME >.build_time.txt
Se define un script entrypoint.sh como punto de entrada del contenedor:

    ENTRYPOINT ["./entrypoint.sh"]

Este script encapsula la lógica de arranque del servicio y permite, si fuera necesario, realizar configuraciones previas antes de iniciar la aplicación.
El uso de un entrypoint separado mejora la modularidad y facilita futuras extensiones.


### Ejecución del sistema
    uv run uvicorn main:app --reload --port 5000
Como se levanta la API:

    uv run uvicorn main:app --reload --port 5000
La imagen se construye con: 

    docker build -t api-configuracion .
    docker run -p 5000:5000 api-configuracion
