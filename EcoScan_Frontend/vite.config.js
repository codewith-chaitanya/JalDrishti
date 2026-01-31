import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  
  // 1. FIXED: Path Aliasing
  // Allows you to use '@' instead of long relative paths
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },

  // 2. FIXED: Development Server Stability
  server: {
    port: 3000, // Keeps your port consistent for the Backend CORS policy
    strictPort: true,
    host: true, // Allows access from your local network (mobile testing)
  },

  // 3. FIXED: Build Optimization (Loophole Fix)
  build: {
    outDir: 'dist',
    sourcemap: false, // Set to true only for debugging production crashes
    rollupOptions: {
      output: {
        // Manual Chunking: Separates heavy libraries into their own files
        // This makes your site load significantly faster
        manualChunks: {
          vendor: ['react', 'react-dom'],
          charts: ['recharts'],
          maps: ['leaflet', 'react-leaflet'],
        },
      },
    },
    // Prevent small assets from being base64 encoded (keeps bundle clean)
    assetsInlineLimit: 4096,
  },
})