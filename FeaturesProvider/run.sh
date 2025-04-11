#!/bin/bash
set -e

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker to run the database."
    echo "You can download it from https://www.docker.com/get-started/"
    exit 1
fi

# Start the database container
echo "Starting the database container..."
cd database
if docker-compose ps | grep -q "profiles_db.*Up"; then
    echo "Database container is already running."
else
    docker-compose up -d
    echo "Waiting for database to initialize..."
    sleep 5  # Give the database some time to initialize
fi
cd ..

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Run the application
echo "Starting the Features Provider API..."
uvicorn main:app --host 0.0.0.0 --port 8000

# Deactivate virtual environment (will only run if the app is stopped)
deactivate 