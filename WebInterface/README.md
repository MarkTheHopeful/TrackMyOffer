# TrackMyOffer

A modern application for tracking job applications, creating CVs and managing job offers.

## Features

- Tailored CV creation
- CV review and feedback
- Cover letter generator
- Backend connectivity demo

## Setup

### Docker

The easiest way to run the application is using Docker:

1. Build the Docker image:
   ```bash
   docker build -t web-interface .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5173:5173 web-interface
   ```

You can customize the host, port, and API connection using environment variables:
   ```bash
   docker run -p 3000:3000 -e VITE_DEV_PORT=3000 -e VITE_DEV_HOST=0.0.0.0 -e VITE_API_HOST=backend-service -e VITE_API_PORT=8080 web-interface
   ```

### Manual Setup

1. Clone the repository
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm run dev
   ```

## Backend Configuration

The frontend connects to a backend API. Configure the connection in the `.env` file:

```
VITE_API_HOST=localhost
VITE_API_PORT=8080
```

The API endpoints include:
- `/v0/hello` - Basic health check endpoint
- `/features/v0/hello` - Features API endpoint 
