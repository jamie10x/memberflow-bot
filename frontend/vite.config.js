// frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        // This is the configuration you need to add
        // The host must be '0.0.0.0' for the containerized app to be reachable
        host: '0.0.0.0',
        port: 5173,
        // Add your ngrok domain to the list of allowed hosts
        hmr: {
            host: 'localhost',
        },
        // add your ngrok domain to the list of allowed hosts
        allowedHosts: ['https://memberflow-bot.onrender.com']
    },
})