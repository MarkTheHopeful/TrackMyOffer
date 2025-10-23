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

## Architecture

Base: React 18 + TypeScript, build via Vite with alias @ on src; Tailwind CSS for design, clsx+tailwind-merge for class merging; lucide-react icons; ESLint/TS configured in repo (WebInterface/package.json:6-35, WebInterface/vite.config.ts:5-27, WebInterface/tailwind.config.js:1-38, WebInterface/src/lib/utils.ts:1-6).

Entry point: WebInterface/src/main.tsx:1-10 mounts <App/> to #root;

WebInterface/src/App.tsx:21-198 manages authorization and view switching via local ActiveView, renders side navigation and content blocks (CV builder, job match, cover letter, etc.).

Navigation/components: reused UI elements (for example, Button) are in components/ui, business features are in components/*; navigation is set by the Navigation component, which switches ActiveView (WebInterface/src/components/navigation.tsx:31-89, WebInterface/src/components/ui/button.tsx:1-33).

Launch: from the root of the cd WebInterface front, then pnpm install and pnpm dev; pnpm build builds production, pnpm preview raises the local preview (commands are described in WebInterface/package.json:6-10).

Backend integration: all HTTP requests are centralized in WebInterface/src/api/backend.ts:8-301, the URL database is taken from env (VITE_API_HOST, VITE_API_PORT, VITE_FULL_API_URL), requests come with credentials: 'include' and cover authorization (/auth/status, /login, /logout) and feature API (/features/v0/...).

Integration with the rest of the parts: the front accesses the backend (BackEnd folder) and the Feature Provider service through a single API gate; when logged in, the redirect goes to /login, and profile/resume data is pulled up through REST endpoints that return typed structures (ProfileData, Experience, CV_Markdown, ReviewResult in WebInterface/src/api/*.ts).