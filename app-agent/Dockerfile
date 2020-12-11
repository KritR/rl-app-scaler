FROM python:3.8-slim

ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random 
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_DEFAULT_TIMEOUT 100

# Install and setup poetry
RUN pip3 install Flask

COPY ./app_agent/ /app/

# run entrypoint.sh
ENTRYPOINT ["python", "/app/app.py"]
