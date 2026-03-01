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
- `/build`: El endpoint `/build` expone información relacionada con la construcción del sistema, incluyendo variables de entorno definidas durante el proceso de build.
- `/health`: El endpoint `/health` permite verificar que el servicio se encuentra en ejecución y respondiendo correctamente. Actua como un mecanismo básico de monitoreo, facilitando la detección rápida de fallas y la validación del estado del sistema.

### Gestión de dependencias con uv
Las dependencias del proyecto se gestionan mediante uv, utilizando los archivos pyproject.toml y uv.lock. 
El archivo uv.lock garantiza la instalación exacta de versiones, permitiendo reproducibilidad del entorno.
### Ejecución del sistema

----Los últimos dos apartados son sugerencias


## Desafíos y consideraciones

### Desafíos

El trabajo en paralelo de diferentes miembros del equipo es un desafío para nosotros. Para tener un registro de las versiones del proyecto y poder trabajar de forma aislada, decidimos trabajar como contribuyentes de un mismo repositorio (no un fork), y crear ramas por cada componente. A demás, una persona trabaja en una sola rama, y al finalizar su componente, hace un "merge" de la misma a la rama **main**. Así, basta con hacer un pull del repositorio para tener una versión actualizada.

Tuvimos desafíos al hacer uso de Docker para la contenerización:
* 


Al trabajar entre muchas personas, es necesario llevar un registro de las versiones de los paquetes que se usan, 