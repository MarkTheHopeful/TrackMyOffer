import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: process.env.VITE_DEV_HOST ?? '127.0.0.1',
    port: parseInt(process.env.VITE_DEV_PORT ?? "5173")
  },
  preview: {
    allowedHosts: ["trackmyoffer.onrender.com"]
  }
});