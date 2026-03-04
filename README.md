<h1 align=center><b>FastAPI + Docker: Contenerización de una REST API.</b></h1>

<h2 align=center><b>Integrantes</b></h2>
<br>
<p align=center><b>Adad, Juan Augusto</b></p>
<p align=center><b>Gimenez, Maria Victoria</b></p>
<p align=center><b>Lescano Stisman, Mikael</b></p>
<p align=center><b>Villa, Benjamin</b></p>

## Índice
- [Introducción](#introducción)
- [Desarrollo práctico](#desarrollo-técnico)
- [Beneficios](#beneficios)
- [Desafios y consideraciones](#desafíos-y-consideraciones)
- [Conclusión](#conclusión)
- [Referencias](#referencias)

## Introducción

En el desarrollo de software moderno, la gestión de configuración es un aspecto fundamental para garantizar la trazabilidad, reproducibilidad y consistencia de los sistemas. 

Las aplicaciones web requieren una correcta administración de versiones, dependencias y entornos de ejecución. En este trabajo se presenta una experiencia práctica utilizando FastAPI para la implementación de una API REST, uv para la gestión de dependencias y Docker para la construcción de un entorno reproducible.

El objetivo es demostrar cómo estas herramientas permiten construir y ejecutar un sistema de manera controlada y verificable.

## Desarrollo Técnico
### Estructura del proyecto
    trabajo-final-is2/
    ├── scripts/
    |   ├── build_and_run.sh
    |   └── entrypoint.sh
    ├── main.py
    ├── settings.py
    ├── pyproject.toml
    ├── uv.lock
    ├── Dockerfile
    ├── .gitignore
    └── .dockerignore
   
#### Implementación de los endpoints
- `/`: El endpoint `/` devuelve un pequeño objeto JSON con metadatos del servicio. Se utiliza como “pantalla de bienvenida” o índice de la API durante el desarrollo. El contenido del JSON se construye a partir de la constante **SERVICE_NAME** en **settings.py** y lista las rutas más relevantes disponibles.
- `/build`: Expone información relacionada con la construcción del sistema, incluyendo variables de entorno definidas durante el proceso de build.
- `/runtime:` El endpoint `/runtime` ofrece información del sistema en donde se corre la aplicación: sistema operativo, versión del SO, distribución, usuario, pid, uso de CPU, uso de memoria, tiempo de inicio y fecha de inicio.
- `/config`: Devuelve la configuración base del sistema, incluyendo el entorno de ejecución y el puerto configurado.
- `/version`: Proporciona información técnica del servicio, incluyendo el nombre, versión de la app, versión de Python y el entorno de despliegue.
- `/health`: El endpoint permite verificar que el servicio se encuentra en ejecución y respondiendo correctamente. Actua como un mecanismo básico de monitoreo, facilitando la detección rápida de fallas y la validación del estado del sistema.
  
---

### Gestión de dependencias con uv
Las dependencias del proyecto se gestionan mediante uv, utilizando los archivos `pyproject.toml` y `uv.lock`. 
El archivo `uv.lock` garantiza la instalación exacta de versiones, permitiendo reproducibilidad del entorno.

---

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

---

### Alternativas de incorporación de `uv` en el contenedor

Cuando queremos utilizar `uv` en un contenedor, hay varias caminos que podemos tomar. Cada uno tiene sus ventajas y desventajas dependiendo de si buscamos simplificar las cosas, tener máximo rendimiento, o solo que funcione rápido.

Las opciones más practicas son:



#### Opción 1: Usar la imagen oficial de `uv` como base

Es la forma más directa. En lugar de arrancar con Python y agregar `uv` después, directamente usamos la imagen que `uv` mantiene con todo preconfigurado.
Se utiliza cuando se trabaja localmente y se quiere algo más simple, por ejemplo, cuando el equipo es chico y no les importa una imagen más grande.

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

ARG START_TIME

WORKDIR /app

COPY main.py settings.py pyproject.toml uv.lock .python-version ./scripts/entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

ENV UV_NO_DEV=1

RUN uv sync --locked;

RUN BUILD_TIME=$(( $(date +%s) - $START_TIME)) && echo $BUILD_TIME > ./build_time.txt

ENV BASE_IMAGE=ghcr.io/astral-sh/uv:python3.12-trixie-slim

ENTRYPOINT ["./entrypoint.sh" ]
```


**Ventajas:**
- Muy fácil de entender, es prácticamente una copia
- Menos cosas que pueden salir mal
- Todo viene preconfigurado

**Desventajas:**
- La imagen final es más pesada
- Menos control sobre qué exactamente incluís en el contenedor



#### Opción 2: Instalar `uv` con `pip`

La forma tradicional de hacerlo. Usamos Python como base y simplemente instalamos `uv` como cualquier otro paquete.
Se usa, por ejemplo, si querés la forma más estándar y familiar; cuando trabajás con otros que siempre usan `pip`.

```dockerfile
FROM python:3.12-slim-trixie

ARG START_TIME

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY main.py settings.py pyproject.toml uv.lock .python-version ./scripts/entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

ENV UV_NO_DEV=1

RUN uv sync --locked;

RUN BUILD_TIME=$(( $(date +%s) - $START_TIME)) && echo $BUILD_TIME > ./build_time.txt

ENV BASE_IMAGE=python:3.12-slim-trixie

ENTRYPOINT ["./entrypoint.sh" ]
```


**Ventajas:**
- Es lo que la mayoría conoce, muy familiar
- Funciona en prácticamente cualquier lado
- Fácil de mantener

**Desventajas:**
- `uv` como paquete pip no es tan rápido como el binario compilado
- Un poco menos elegante que las otras opciones



#### Opción 3: Lo que estamos usando (Multi-stage build)

Esta es la que ya tenemos. Copiamos el binario compilado de `uv` desde su imagen oficial, pero mantenemos Python slim como base. Es un equilibrio entre eficiencia y control.
Lo elegimos porque la imagen final es lo más pequeña posible, por lo tanto, `uv` corre al máximo rendimiento (binario compilado) y además, tenemos control total de qué va en la imagen.

```dockerfile
FROM python:3.12-slim-trixie

ARG START_TIME

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY main.py settings.py pyproject.toml uv.lock .python-version ./scripts/entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

ENV UV_NO_DEV=1

RUN uv sync --locked;

RUN BUILD_TIME=$(( $(date +%s) - $START_TIME)) && echo $BUILD_TIME > ./build_time.txt

ENV BASE_IMAGE=python:3.12-slim-trixie

ENTRYPOINT ["./entrypoint.sh" ]

```


**Ventajas:**
- Contenedores más pequeños y rápidos en producción
- Máximo rendimiento
- Aprovecha lo mejor de ambos mundos

**Desventajas:**
- El Dockerfile es un poco más complejo si recién empezás con Docker
- Requiere entender qué es un "multi-stage build"

---


### Ejecución del sistema
Para ejecutar el sistema tenes dos posibilidades, sin el dockerfile o con el dockerfile.
Con el docker file, podes utilizar el script que esta en la carpeta 

    scripts/build_and_run.sh
    
Para ejecutar el script simplemente debes hacer:

    chmod +x ./script/build_and_run.sh
    ./build_and_run.sh

Es necesario correr el script en un interprete de bash, powershell no tenemos.

## Beneficios

Este proyecto de API REST hecho con **FastAPI** y contenerización mediante **Docker** aporta múltiples ventajas:

### Beneficios Técnicos
- **Alto rendimiento**: FastAPI ofrece gran velocidad y soporte para concurrencia.
- **Modularidad y claridad**: Endpoints definidos de manera sencilla y organizada, facilitando el mantenimiento.

### Beneficios Operativos
- **Monitoreo integrado**: Endpoints de estado y configuración permiten verificar rápidamente la salud del servidor.
- **Transparencia**: Exposición de información clave (versión, puerto, tiempo de ejecución, endpoints disponibles).
- **Escalabilidad**: Fácil replicación y despliegue en múltiples instancias gracias a Docker.

### Beneficios para el Desarrollo
- **Pruebas simplificadas**: Endpoints de configuración y estado facilitan la validación en desarrollo y despliegue.
- **Documentación**: FastAPI genera documentación interactiva (Swagger/OpenAPI).
- **Integración continua**: Compatible con pipelines de CI/CD, reduciendo errores y tiempos de entrega.

### Beneficios Organizacionales
- **Estandarización**: Forma uniforme de consultar información del servidor en distintos entornos.
- **Reducción de costos**: Menos tiempo invertido en configuraciones manuales y resolución de problemas.

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

#### ¿Que estrategias de ramificación utilizamos?

Cuando se trabaja en equipo utilizando un VCS como git que permite crear ramas de manera eficiente, podemos aprovechar esta caracteristica y desarrollar o utilizar estrategias de ramificación para una experiencia de desarrollo más productiva.
Nuestra estrategia se baso estrictamente en:

- Cada colaborador, cuando decida realizar algún cambio al proyecto, deberá crear una rama utilizando la siguiente convención:

    - `feature/nombre-feature`: En caso de que se quiera agregar una nueva funcionalidad al sistema. (crear endpoints, crear imagen docker, algo que dote de funcionalidad al sistema)
    - `bugfix/nombre-bugfix`: En caso de que se quiera solucionar un bug.
    - `docs/nombre-docs`: En caso de que se quiera agregar/modificar documentación al sistema.

- Cada colaborador trabaja en su rama.
- Una vez se termine de trabajar en la rama (cumplió su proposito) se realiza un merge a main y se notifica al equipo.

#### Convenciones de commit

Para el desarrollo de este proyecto utilizamos de varias convenciones (estrategias de branching, la utilización de un gestor de proyectos, un VCS), entre ellas utilizamos una llamada **Conventional Commits**. Hacemos uso de esta para una mejor legibilidad y consistencia entre commits. Dejamos en la sección de [referencias](#referencias) el enlace que especifica esta convención.


## Conclusión

Con este proyecto aprendimos:

- El contenerizar las aplicaciones nos ayuda a eliminar los problemas causados por las diferencias entre sistemas operativos y/o versiones de librerias globales. Cada desarrollador levanta exactamente el mismo entorno de ejecución, permitiendonos así la reproducibilidad del entorno, un comportamiento predecible de la aplicación que parte desde el desarrollo hasta producción.

- Trabajar en equipo utilizando un VCS como git, implica utilizar una estrategia de ramificación que permite trabajar en múltiples funcionalidades, correcciones y minimización de conflictos en el código.

- La utilización de uv como gestor de proyectos nos da de una mejor experiencia de desarrollo. Unifica la gestión de paquetes, entornos virtuales y versiones de python en una sola herramienta que es extremadamente rápida. La capacidad que tiene para generar lockfiles se complementa con Docker, garantizándonos las instalaciones rápidas y seguras.

Finalmente, podemos concluir que la utilización de estas herramientas en la ingenieria de software nos provee de una mejor reproducibilidad del entorno que finalmente nos lleva a una mejor experiencia de desarrollo.

## Referencias

- [uv](https://docs.astral.sh/uv/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://docs.docker.com/reference/)
- [Estrategias de ramificacion](https://medium.com/@abhay.pixolo/naming-conventions-for-git-branches-a-cheatsheet-8549feca2534)
- [Conventional Commits](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13)
- [Git Pro](https://git-scm.com/book/en/v2)
- [Contenerizar uv](https://docs.astral.sh/uv/getting-started/installation/#docker)
