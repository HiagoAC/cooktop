FROM python:3.13.0a1-alpine3.18
LABEL org.opencontainers.image.authors="Hiago <https://github.com/HiagoAC>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# Install Rust/Cargo (pydantic/django-ninja dependencies)
RUN apk --no-cache add curl && \
    apk add --no-cache cargo && \
    curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSfy | sh
ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

USER django-user