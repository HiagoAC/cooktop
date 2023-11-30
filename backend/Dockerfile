FROM python:3.13.0a1-alpine3.18
LABEL org.opencontainers.image.authors="Hiago <https://github.com/HiagoAC>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY .requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    useradd django-user

USER django-user