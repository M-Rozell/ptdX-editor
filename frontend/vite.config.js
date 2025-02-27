import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
  define: {
    'process.env': {},
  },
  build: {
    outDir: 'dist',
  },
  resolve: {
    alias: {
      'fs': false,  // Prevents Vite from trying to bundle `fs`
    }},
});
