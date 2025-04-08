#!/bin/bash

API_KEY=xxx

trap "kill 0" SIGINT SIGTERM

echo "Create directory to store logs..."
mkdir -p logs

echo "Running feature provider..."
cd FeaturesProvider && API_KEY=$API_KEY uvicorn main:app --reload 2> ../logs/feat.err > ../logs/feat.out &

echo "Running backend at localhost:8081 and feature provider at 127.0.0.1:8000..."
cd BackEnd && PORT=8081 PROVIDER_HOST=127.0.0.1 PROVIDER_PORT=8000 ./gradlew run 2> ../logs/backend.err > ../logs/backend.out &

echo "Running web server with backend at localhost:8081..."
cd WebInterface && VITE_API_HOST=localhost VITE_API_PORT=8081 npm run dev 2> ../logs/web.err > ../logs/web.out &

wait