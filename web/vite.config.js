import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: '0.0.0.0',  // Listen on all network interfaces
    port: 5173 ,
    watch: {
      usePolling: true,  // Necessary in Docker to ensure file changes are detected
    },       
  },
  plugins: [react()],
})
