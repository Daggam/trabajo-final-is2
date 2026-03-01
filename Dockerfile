FROM python:3.12-slim-trixie

ARG START_TIME

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY main.py settings.py pyproject.toml uv.lock .python-version ./scripts/entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

ENV UV_NO_DEV=1

RUN uv sync --locked;

RUN BUILD_TIME=$(( $(date +%s) - $START_TIME)) && echo $BUILD_TIME > ./build_time.txt

ENTRYPOINT ["./entrypoint.sh" ]

