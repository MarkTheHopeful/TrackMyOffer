import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import * as path from 'path';

export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current directory
  const env = loadEnv(mode, process.cwd(), '');

  // Derive API base URL from env for development convenience, with sane defaults
  const apiHost = env.VITE_API_HOST || 'localhost';
  const apiPort = env.VITE_API_PORT || '3001';
  const fullApiUrl = env.VITE_FULL_API_URL;
  const apiBaseUrl = fullApiUrl || `http://${apiHost}:${apiPort}`;

  return {
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
      __API_BASE_URL__: JSON.stringify(apiBaseUrl),
    },
    server: {
      allowedHosts: ["trackmyoffer.onrender.com", "6ce54fc456a94f19a7ee22900dbbf76f.constructor.pro"],
      host: env.VITE_DEV_HOST || '127.0.0.1',
      port: parseInt(env.VITE_DEV_PORT || "5173")
    },
    preview: {
      allowedHosts: ["trackmyoffer.onrender.com", "6ce54fc456a94f19a7ee22900dbbf76f.constructor.pro"],
    }
  };
});
