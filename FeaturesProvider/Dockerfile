FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget gnupg unzip ca-certificates \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 \
    libcairo2 libcups2 libdbus-1-3  \
    libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libxss1 libxtst6 libu2f-udev libvulkan1 \
    chromium firefox-esr \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN playwright install

COPY . .

ARG A_HOST=0.0.0.0
ARG A_PORT=4002
ARG A_DB_HOST=0.0.0.0
ARG A_DB_PORT=5432
ARG A_DB_PASSWORD=features_password
ARG A_API_KEY=soska_nerealka

ENV HOST=$A_HOST
ENV PORT=$A_PORT
ENV DB_HOST=$A_DB_HOST
ENV DB_PORT=$A_DB_PORT
ENV DB_PASSWORD=$A_DB_PASSWORD
ENV API_KEY=$A_API_KEY

EXPOSE $PORT

CMD exec uvicorn main:app --host ${HOST} --port ${PORT}
