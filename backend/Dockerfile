FROM python:3.12-slim-bookworm
LABEL org.opencontainers.image.authors="Hiago <https://github.com/HiagoAC>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# Install requirements' dependencies:
# Rust/Cargo --> pydantic/django-ninja dependencies
#RUN apt-get update && \
#    apt-get install -y curl && \
#    apt-get install -y cargo && \
#    curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSfy | sh
#ENV PATH="/root/.cargo/bin:${PATH}"

ARG DEV=false
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    useradd --system django-user

USER django-user