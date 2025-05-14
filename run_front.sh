#!/bin/bash

# Start all backend services via docker compose (except the web frontend)
docker compose up -d --build backend featuresprovider features_db

# Start the frontend manually
cd WebInterface
pnpm install
# Build the app first
pnpm build
# Run preview server with same settings as Dockerfile
VITE_DEV_HOST=0.0.0.0 VITE_DEV_PORT=3000 VITE_API_HOST=localhost VITE_API_PORT=3001 pnpm dev