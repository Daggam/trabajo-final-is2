# FastAPI + Docker: Contenerización de una REST API.

## Índice
- [Introducción](#introducción)
- [Desarrollo práctico](#desarrollo-técnico)
- [Beneficios](#beneficios)
- [Desafios y consideraciones]()
- [Conclusión](#conclusión)
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
- `/health`: El endpoint `/health` permite verificar que el servicio se encuentra en ejecución y respondiendo correctamente. Actua como un mecanismo básico de monitoreo, facilitando la detección rápida de fallas y la validación del estado del sistema.

### Gestión de dependencias con uv
Las dependencias del proyecto se gestionan mediante uv, utilizando los archivos pyproject.toml y uv.lock. 
El archivo uv.lock garantiza la instalación exacta de versiones, permitiendo reproducibilidad del entorno.

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
Para ejecutar el sistema tenes dos posibilidades, sin el dockerfile o con el dockerfile.
Con el docker file, podes utilizar el script que esta en la carpeta 

    scripts/build_and_run.sh
    
Para ejecutar el script simplemente debes hacer:

    chmod +x ./script/build_and_run.sh
    ./build_and_run.sh

Es necesario correr el script en un interprete de bash, powershell no tenemos.

## Beneficios

Este proyecto de API REST con **FastAPI** y despliegue mediante **Docker** aporta múltiples ventajas tanto técnicas como operativas:

### Beneficios Técnicos
- **Alto rendimiento**: FastAPI ofrece gran velocidad y soporte para concurrencia.
- **Despliegue consistente**: Docker garantiza que la aplicación se ejecute de forma idéntica en cualquier entorno.
- **Modularidad y claridad**: Endpoints definidos de manera sencilla y organizada, facilitando el mantenimiento.

### Beneficios Operativos
- **Monitoreo integrado**: Endpoints de estado y configuración permiten verificar rápidamente la salud del servidor.
- **Transparencia**: Exposición de información clave (versión, puerto, tiempo de ejecución, endpoints disponibles).
- **Escalabilidad**: Fácil replicación y despliegue en múltiples instancias gracias a Docker.

### Beneficios para el Desarrollo
- **Pruebas simplificadas**: Endpoints de configuración y estado facilitan la validación en desarrollo y despliegue.
- **Documentación automática**: FastAPI genera documentación interactiva (Swagger/OpenAPI).
- **Integración continua**: Compatible con pipelines de CI/CD, reduciendo errores y tiempos de entrega.

### Beneficios Organizacionales
- **Estandarización**: Forma uniforme de consultar información del servidor en distintos entornos.
- **Reducción de costos**: Menos tiempo invertido en configuraciones manuales y resolución de problemas.
- **Confiabilidad**: La combinación de FastAPI y Docker asegura estabilidad y reproducibilidad en producción.

## Conclusión

Con este proyecto aprendimos:

- El contenerizar las aplicaciones nos ayuda a eliminar los problemas causados por las diferencias entre sistemas operativos y/o versiones de librerias globales. Cada desarrollador levanta exactamente el mismo entorno de ejecución, permitiendonos así la reproducibilidad del entorno, un comportamiento predecible de la aplicación que parte desde el desarrollo hasta producción.

- Trabajar en equipo utilizando un VCS como git, implica utilizar una estrategia de ramificación que permite trabajar en múltiples funcionalidades, correcciones y minimización de conflictos en el código.

- La utilización de uv como gestor de proyectos nos da de una mejor experiencia de desarrollo. Unifica la gestión de paquetes, entornos virtuales y versiones de python en una sola herramienta que es extremadamente rápida. La capacidad que tiene para generar lockfiles se complementa con Docker, garantizándonos las instalaciones rápidas y seguras.

Finalmente, podemos concluir que la utilización de estas herramientas en la ingenieria de software nos provee de una mejor reproducibilidad del entorno que finalmente nos lleva a una mejor experiencia de desarrollo.
