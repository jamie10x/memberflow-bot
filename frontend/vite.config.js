// frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import legacy from '@vitejs/plugin-legacy' // <-- 1. IMPORT THE PLUGIN

export default defineConfig({
    plugins: [
        react(),
        legacy({ // <-- 2. ADD THE PLUGIN CONFIGURATION
            targets: ['defaults', 'not IE 11'],
        }),
    ],
    // Your server config for local development is fine, no changes needed here.
    server: {
        host: '0.0.0.0',
        port: 5173,
        hmr: {
            host: 'localhost',
        },
        // This is a local setting, you'll need to update it if ngrok changes
        allowedHosts: ['c55919e87a0e.ngrok-free.app']
    },
})