FROM node:21-bookworm-slim
LABEL org.opencontainers.image.authors="Hiago <https://github.com/HiagoAC>"

COPY app/package.json app/package.json

WORKDIR /app
EXPOSE 5173

RUN npm update && \
    npm install --ignore-scripts -g vite@latest && \
    npm install --ignore-scripts && \
    useradd --system nonroot && \
    mkdir -p /home/nonroot && \
    chmod -R 755 /home/nonroot && \
    chown -R nonroot:nonroot /home/nonroot

COPY ./app /app

USER nonroot