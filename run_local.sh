#!/bin/bash

trap "kill 0" SIGINT SIGTERM

echo "Create directory to store logs..."
mkdir -p logs

echo "Running feature provider..."
cd FeaturesProvider && ./run.sh 2> ../logs/feat.err > ../logs/feat.out &

echo "Running backend at localhost:8080 and feature provider at 127.0.0.1:8000..."
cd BackEnd && PORT=8080 PROVIDER_HOST=127.0.0.1 PROVIDER_PORT=8000 ./gradlew run 2> ../logs/backend.err > ../logs/backend.out &

echo "Running web server at localhost:5000 with backend at localhost:8080..."
cd WebInterface && VITE_DEV_HOST=localhost VITE_DEV_PORT=5000 VITE_API_HOST=localhost VITE_API_PORT=8080 npm run dev 2> ../logs/web.err > ../logs/web.out &

wait
