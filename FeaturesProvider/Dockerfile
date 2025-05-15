FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

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
