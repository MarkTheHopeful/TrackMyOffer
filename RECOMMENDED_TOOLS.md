# Recommended Tools for working with Project 

## Web Interface 

### Manual project setup and run

Web part of the project exploits Node.js Javascript runtime environment and npm package manager, installation instructions can be found [here](https://nodejs.org/en/download/).

When having `node` and `npm` user can configure Web Interface in the following way:

1. Install dependencies:
```
npm install
```
2. Start the development server:
```
npm run dev
```

### Docker 
Alternatively, Web Interface includes a Dockerfile that allows you to build and run the application in a Docker container.
Installation instructions for docker can be found on the official [page](https://docs.docker.com/engine/install/?utm_source=chatgpt.com).

#### Building the Docker Image

To build the Docker image, run the following command from the WebInterface directory:

```
docker build -t web-interface .
```

#### Running the Docker Container

To run the Docker container with default settings:

```
docker run -p 5173:5173 web-interface
```

#### Environment Variables

You can override the default settings by providing environment variables:

```
docker run -p 3000:3000 -e VITE_DEV_PORT=3000 -e VITE_DEV_HOST=0.0.0.0 -e VITE_API_HOST=backend-service -e VITE_API_PORT=8080 web-interface
```

## Feature Provider

### Manual project setup and run
1. Install [python](https://www.python.org/downloads/) of version >= 3.12
2. Setup `API_KEY` (key for https://openrouter.ai/) in the `.env` file
3. Run the application using the provided script:
```
./run.sh
```
The script will automatically:

* Create a virtual environment
* Install all required dependencies
* Start the server on port 8000

### Docker 
Alternatively, Features Provider part includes a Dockerfile that allows you to build and run the application in a Docker container.
Installation instructions for docker can be found on the official [page](https://docs.docker.com/engine/install/?utm_source=chatgpt.com).

#### Building the Docker Image

To build the Docker image, run the following command from the FeaturesProvider directory:

```
docker build -t features-provider .
```

#### Running the Docker Container

To run the Docker container with default settings:

```
docker run -p 8000:8000 features-provider
```

#### Environment Variables

You can override the default settings by providing environment variables:

```
docker run -p 9000:9000 -e PORT=9000 -e HOST=0.0.0.0 -e API_KEY=your-api-key features-provider
```

### Running Tests
1. Ensure you have the virtual environment activated
2. Run ```pytest```

### Running Database
1. Make sure you've installed Docker
2. Run ```cd database```
3. Run ```docker compose up -d``` or ```docker-compose up -d```

The database will be accessible at:
  * Host: localhost
  * Port: 5432
  * Database: features_db
  * Username: features_user
  * Password: features_password

## Back End

### Manual project setup and run
This part is implemented as Kotlin gradle project, therefore to work with it you need:
* JDK. Installation guides for different platforms can be found [here](https://docs.oracle.com/en/java/javase/21/install/overview-jdk-installation.html#GUID-8677A77F-231A-40F7-98B9-1FD0B48C346A__INSTALLINGTHEJDKANDJREONLINUX-E04E90B9).

You run project with `./gradlew run` for Linux/Macos, `gradlew.bat run` for Windows.
Optionally, you can specify deployment port and host, as well as host and port of the feature provider (below are defaults) via env: `PORT=8080 HOST=0.0.0.0 PROVIDER_PORT=8000 PROVIDER_HOST=0.0.0.0 ./gradlew run`. 

### Docker 
Alternatively, Back End part includes a Dockerfile that allows you to build and run the application in a Docker container.
Installation instructions for docker can be found on the official [page](https://docs.docker.com/engine/install/?utm_source=chatgpt.com).

#### Building the Docker Image

To build the Docker image, run the following command from the BackEnd directory:

```
docker build -t trackmyoffer-backend .
```

#### Running the Docker Container

To run the Docker container with default settings:

```
docker run -p 8080:8080 trackmyoffer-backend
```

#### Environment Variables

You can override the default settings by providing environment variables:

```
docker run -p 9090:9090 -e PORT=9090 -e HOST=0.0.0.0 -e PROVIDER_PORT=8081 -e PROVIDER_HOST=features-provider trackmyoffer-backend
```

Available environment variables:
- `PORT`: The port on which the server will listen (default: 8080)
- `HOST`: The host address to bind to (default: 0.0.0.0)
- `PROVIDER_PORT`: The port of the features provider service (default: 8081)
- `PROVIDER_HOST`: The host of the features provider service (default: 0.0.0.0)
