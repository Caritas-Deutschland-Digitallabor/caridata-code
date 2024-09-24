FROM python:3.11 AS base

ENV POETRY_VERSION=1.8.3
ARG ENVIRONMENT=DEVELOPMENT

RUN pip install poetry==$POETRY_VERSION
RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev

COPY ./src /api
COPY  ./pyproject.toml /api

FROM python:3.11-slim as deploy

COPY --from=base /api /api
COPY --from=base /usr/local/bin /usr/local/bin
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
WORKDIR /api
