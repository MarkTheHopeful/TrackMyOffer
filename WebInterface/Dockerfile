# Build stage
FROM node:20-slim AS build

# Install pnpm
RUN npm install -g pnpm

# Set working directory
WORKDIR /app

# Copy package.json and pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install dev

# Copy the rest of the application
COPY . .

# Build the application
RUN pnpm build

# Production stage
FROM node:20-slim

# Install pnpm and vite
RUN npm install -g pnpm vite

# Set working directory
WORKDIR /app

# Copy built assets from the build stage
COPY --from=build /app/dist ./dist
COPY --from=build /app/package.json ./
COPY --from=build /app/pnpm-lock.yaml ./
COPY --from=build /app/vite.config.ts ./

# Install only production dependencies
RUN pnpm install dev

# Set environment variables with defaults
ENV VITE_DEV_HOST=0.0.0.0
ENV VITE_DEV_PORT=5173
ENV VITE_API_HOST=localhost
ENV VITE_API_PORT=3001

# Expose the port
EXPOSE $VITE_DEV_PORT

# Run the application
CMD exec pnpm preview --host ${VITE_DEV_HOST} --port ${VITE_DEV_PORT}
