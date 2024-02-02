FROM node:21-bookworm-slim
LABEL org.opencontainers.image.authors="Hiago <https://github.com/HiagoAC>"

COPY app/package.json app/package.json

WORKDIR /app
EXPOSE 5173

RUN npm update && \
    npm install -g vite@latest && \
    npm install

COPY ./app /app