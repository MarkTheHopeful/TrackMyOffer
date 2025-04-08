import {defineConfig} from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        host: process.env.VITE_DEV_HOST || 'localhost',  // Default to localhost
        port: Number(process.env.VITE_DEV_PORT) || 3000, // Default to 3000
    },
})
