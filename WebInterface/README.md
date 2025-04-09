# TrackMyOffer

A modern application for tracking job applications, creating CVs and managing job offers.

## Features

- Tailored CV creation
- CV review and feedback
- Cover letter generator
- Backend connectivity demo

## Setup

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