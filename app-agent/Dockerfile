FROM python:3.7-slim

ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random 
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_DEFAULT_TIMEOUT 100
ENV POETRY_VERSION 1.0.0

# Install and setup poetry
RUN pip install -U pip \
    && apt-get update \
    && apt install -y curl netcat \
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.in-project false
RUN poetry install --no-interaction

ENV FLASK_APP app.py

COPY ./app_agent/ /app/

# run entrypoint.sh
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
