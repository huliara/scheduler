FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


RUN apt update \
    && apt install --no-install-recommends -y tzdata gcc libc-dev libffi-dev python3-dev\
    && apt clean


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /usr/src/api

RUN --mount=type=cache,target=/root/.cache/uv \
--mount=type=bind,source=./api/uv.lock,target=uv.lock \
--mount=type=bind,source=./api/pyproject.toml,target=pyproject.toml \
uv sync --frozen --no-install-project
