FROM python:3.11-slim as build

RUN apt-get update && \
    apt-get upgrade -y \
    && apt-get install -y \
        curl \
        build-essential \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH /root/.local/bin:$PATH

RUN python -m venv /venv --copies
ENV PATH /venv/bin:$PATH

RUN mkdir /app
COPY poetry.lock pyproject.toml distilbert-base-uncased-finetuned-sst2 /app/
WORKDIR /app
RUN . /venv/bin/activate && poetry install --only main

FROM python:3.11-slim as deploy
RUN apt-get update && \
    apt-get upgrade -y \
    && apt-get install -y curl

COPY --from=build /venv /venv
COPY . /app

ENV PATH /venv/bin:$PATH
WORKDIR /app

HEALTHCHECK --interval=10s --timeout=3s \
    CMD curl -X GET "http://localhost:8000/health" || exit 1 

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
