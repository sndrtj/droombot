FROM python:3.10-slim

ENV POETRY_HOME=/etc/poetry
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app

## Install dependencies for installing poetry
RUN apt-get update && apt-get install curl -y

#USER python
# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy things over
COPY src/ src/
COPY README.md poetry.lock pyproject.toml scripts/entrypoint.sh ./
RUN chmod +x ./entrypoint.sh

## Install python dependencies
RUN $POETRY_HOME/venv/bin/poetry install --only main

ENTRYPOINT ["./entrypoint.sh"]
