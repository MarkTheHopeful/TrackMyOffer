# Build stage
FROM node:20-slim AS build

# Install pnpm
RUN npm install -g pnpm

ARG VITE_CONFIG=vite.config.prod.ts

# Set working directory
WORKDIR /app

# Copy package.json and pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install dev

# Copy the rest of the application
COPY . .

# Build the application with production Vite config
RUN pnpm build --config ${VITE_CONFIG}

# Production stage
FROM node:20

# Accept build arg for which Vite config was used and reuse it here to provide config for preview
ARG VITE_CONFIG=vite.config.prod.ts

# Install pnpm and vite
RUN npm install -g pnpm vite typescript

# Set working directory
WORKDIR /app

# Copy built assets from the build stage
COPY --from=build /app/dist ./dist
COPY --from=build /app/package.json ./
COPY --from=build /app/pnpm-lock.yaml ./
COPY --from=build /app/tsconfig.json ./tsconfig.json
COPY --from=build /app/tsconfig.node.json ./tsconfig.node.json
COPY --from=build /app/tsconfig.app.json ./tsconfig.app.json
COPY --from=build /app/${VITE_CONFIG} ./vite.config.ts

RUN pnpm install

# Expose the fixed preview port
EXPOSE 3000

# Run the application
CMD exec pnpm preview --host 0.0.0.0 --port 3000
