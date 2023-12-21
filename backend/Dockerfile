FROM python:3.12-slim-bookworm
LABEL org.opencontainers.image.authors="Hiago <https://github.com/HiagoAC>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN apt-get update && \
    # Pillow dependenciens
    apt-get install -y libjpeg-dev zlib1g-dev && \ 
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    useradd --system django-user && \
    mkdir -p /vol/web/media && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

COPY ./app /app

USER django-user