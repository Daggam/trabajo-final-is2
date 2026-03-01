# FastAPI + Docker: Contenerización de una REST API.

## Índice
- [Introducción](#introducción)
- [Desarrollo práctico]()
- [Beneficios]()
- [Desafios y consideraciones](#desafíos-y-consideraciones)
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
* Al trabajar con una aplicación web es necesario exponerla a través de un puerto en el localhost. Si se lleva esta aplicación a un contenedor, no es accesible a través del localhost porque ahora el localhost del usuario es distinto al que da acceso a la aplicación (localhost del contenedor).

* Los contenedores se comportan como máquinas aisladas de la principal. Esto hace que los puertos del contenedor sean independientes de los puertos de la máquina principal.

Para solucionar estas dos cuestiones, es necesario:
1. Crear el contenedor mapeando el puerto 8000 del mismo al puerto 8000 de la máquina principal.
2. Hacer que la aplicación dentro del contenedor se ejecute en el host 0.0.0.0.

Con esto, ya es posible acceder a la aplicación dentro del contenedor desde el localhost de la máquina principal.

### Consideraciones

Al trabajar con este proyecto, consideramos lo siguiente.

#### ¿Que vamos a contenerizar?

Al contenerizar una aplicación debemos tener en cuenta como y que vamos a contenerizar. Si nuestro proyecto tuviese una base de datos, el problema se complejizaria más, ya que sería ideal que tengamos migraciones de bases de datos para tener trazabilidad y consistencia en la base de datos, o si tenemos algo simple podriamos tener un archivo .sql que inicialice la base de datos. Y en este caso hipotetico, nuestra REST API dependería de la base de datos, por lo que, por comodidad, sería ideal optar por levantar contenedores utilizando un archivo docker-compose.yaml.

En nuestro caso era una aplicación backend pequeña que utiliza un administrador de proyectos (uv) el cual tenía una imagen propia, por lo que la utilizamos de base para crear la nuestra. Optamos por simplificar el problema.

### ¿Que estrategias de ramificación utilizamos?

Cuando se trabaja en equipo utilizando un VCS como git que permite crear ramas de manera eficiente, podemos aprovechar esta caracteristica y desarrollar o utilizar estrategias de ramificación para una experiencia de desarrollo más productiva.
Nuestra estrategia se baso estrictamente en:

- Cada colaborador, cuando decida realizar algún cambio al proyecto, deberá crear una rama utilizando la siguiente convención:

    - feature/nombre-feature: En caso de que se quiera agregar una nueva funcionalidad al sistema. (crear endpoints, crear imagen docker, algo que dote de funcionalidad al sistema)
    - bugfix/nombre-bugfix: En caso de que se quiera solucionar un bug.
    - docs/nombre-docs: En caso de que se quiera agregar/modificar documentación al sistema.

- Cada colaborador trabaja en su rama.
- Una vez se termine de trabajar en la rama (cumplió su proposito) se realiza un merge a main y se notifica al equipo.