import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import * as path from 'path';

// Production Vite config used inside Docker builds
// Sets API base URL to the values that were previously provided via Docker ENV
const API_BASE_URL = 'https://610818a381f047fd918900aad498e2c7.constructor.pro';

export default defineConfig(() => ({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    },
  },
  define: {
    __API_BASE_URL__: JSON.stringify(API_BASE_URL),
  },
  server: {
    // Not used in production, but kept for parity
    host: '127.0.0.1',
    port: 5173,
  },
  preview: {
    allowedHosts: [
      'trackmyoffer.onrender.com',
      '6ce54fc456a94f19a7ee22900dbbf76f.constructor.pro',
    ],
  },
}));
