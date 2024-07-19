FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY poetry.lock .

COPY pyproject.toml .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install --upgrade pip

RUN pip install --upgrade pip && pip install poetry

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.12-slim as runner

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

WORKDIR /usr

COPY --from=builder /usr/src/app/wheels /wheels

COPY --from=builder /usr/src/app/requirements.txt .

RUN pip install --no-cache /wheels/*

WORKDIR /usr/src

COPY weather ./weather
COPY .env .
COPY city.json .

WORKDIR /usr/src/weather